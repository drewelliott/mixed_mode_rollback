from netmiko import ConnectHandler
from pygnmi.client import gNMIclient

SROS = {
    'device_type':'nokia_sros', 
    'host': 'clab-mix-sros', 
    'username': 'admin', 
    'password': 'admin'
}

GNMI_SROS = {
    'target' : ('clab-mix-sros', 57400),
    'username' : 'admin',
    'password' : 'admin',
    'insecure' : True
}

def create_rollback_point():
    ## create the rollback point in classic mode
    with ConnectHandler(**SROS) as c:
        output = c.send_command("//admin rollback save")
    print(f"Creating rollback save point:\n{output}")


def check_isis_adj():
    ## here we will get the isis adjacencies
    ## 
    ## note: this is very specific for this demo, 
    ## it is very brittle and should not be used
    ## this way in production
    with gNMIclient(**GNMI_SROS) as gc:
        results = gc.get(path=['/state/router/isis/interface/adjacency'])
    isis_adj = results['notification'][0]['update'][0]
    if 'oper-state' in isis_adj.keys():
        print(f"\n\nPRECHECK:\nISIS Adjacency Status: {isis_adj['val']['neighbor']['ipv4']} :: {isis_adj['val']['oper-state']}\n")
    else:
        print("\n\n!!WARNING!!\nISIS Adjacency DOWN\n\nBeginning automatic rollback.\n")
        rollback()


def perform_netconf_changes():
    ## we will simply be changing the level capability
    ## in isis to level 1, since the interfaces are set to
    ## level 2, this will cause the adjacency to drop
    ##
    ## This particular option is different in model-driven
    ## vs. classic cli which helps demonstrate the ability
    ## to use both interfaces in a single script
    ## 
    ## classic: 
    ##     *A:sros>config>router>isis# level-capability level-1
    ## model-driven:
    ##     /configure router "Base" isis level-capability 1
    data = [(
'configure/router[router-name=Base]',
{ 
    'isis':{
        'isis-instance':0,
        'level-capability':'1'
    }
}
)]
    with gNMIclient(**GNMI_SROS) as gc:
        results = gc.set(update=data)
    print(f"\nConfiguring ISIS level-capability:\n{results}\n")


def rollback():
    with ConnectHandler(**SROS) as c:
        output = c.send_command("//admin rollback revert latest-rb now")
    print(f"\n\n{output}")


def main():
    create_rollback_point()
    check_isis_adj()
    perform_netconf_changes()
    check_isis_adj()


if __name__ == "__main__":
    main()
