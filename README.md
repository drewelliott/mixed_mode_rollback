# Rollback demo using mixed management mode in SROS

### In this demo, we will be using a simple [containerlab](https://containerlab.dev) topology with two containers. The DUT will be an SROS container operating in [mixed management mode.](https://documentation.nokia.com/sr/23-10-2/books/system-management/model-driven-management-interfaces.html#ai9exj5x4z) The other container will be running SR Linux.

### When the topology is launched, it will come up with a single link between the two devices. We will have an iBGP session running between the two devices' loopbacks, the IGP will be ISIS.

### For the rollback test, we will be changing the ISIS configuration causing the ISIS adjacency to fail, which will trigger the iBGP session to fail.

### We will finally use the rollback point to revert the changes, allowing ISIS and iBGP to restore.

# Lab Steps

### Step 1: Launching the demo

Make sure to have the latest [containerlab](https://containerlab.dev) installed. 

> you can check this with `sudo clab version upgrade`

Deploy the lab topology with the `-c` switch - this will always make sure that the lab is loaded from scratch, if you leave that off, it will load whatever the last state was from the configuration artifacts

`sudo clab deploy -t topo.yml -c`

When the topology finishes booting, you will have the following starting state. 

>Note that `sros` will be running in `mixed-mode`.

```

  1.1.1.1/32                    2.2.2.2/32
 ┌──────────┐                  ┌──────────┐
 │          │   12.12.12.0/31  │          │  
 │  sros    ├──────────────────┤   srl    │
 │          │.0              .1│          │
 │          │                  │ agg:12/8 │
 └──────────┘                  └──────────┘
                ISIS: 49.0001
                iBGP: 65001
```