from helpers import get_connection as gc
import argparse

c = gc("clab-mix-sros", "admin", "admin", 830)

def create_rollback_point():
    ## create the rollback point in classic mode
    pass

def check_isis_adj():
    ## here we will get the isis adjacencies
    ## 
    ## we will store them in a dictionary if it
    ## doesn't already exist, and if it does 
    ## already exist, we will compare - if there 
    ## are differences, we will rollback
    pass

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
    pass

def rollback():
    pass

def main():
    ## step 1: create a rollback point
    ## step 2: check isis adjacency
    ## step 2: perform the netconf changes
    ## step 3: check isis adjacency and report changes
    ## step 4: perform a rollback  
    pass

if __name__ == "__main__":
    main()