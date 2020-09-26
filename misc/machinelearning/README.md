# MachineLearning

Don't you love making cloud GPUs go brrr. 
To help you train your machine learning models on the EMZMachine8000 we have designed a specialized hypervisor to multiplex our GPU across virtual machines!

Test our hypervisor today!
```bash
$ nc misc.game.alcapwnctf.in 32100
```

## Hypervisor

However, we are in beta right now and our hypervisor can only run two VMs concurrently!

```ascii
                Physical Address Space
                    | -- Hypervisor -- | -- Control Program -- | --    Your VM   -- |
                    |<--- 64 bytes --->|<---   1024 bytes  --->|<--- 1024 bytes --->|
                                            ^
    |-----|                                 |
    | GPU | ---------------------------------
    |-----|
    RTX3090

    Hypervisor boots up installs itself into physical memory,
    Launches the VMs and returns the result back to you!
```

To improve performance, everything is parallelized and done concurrently. Hope there are no race conditions!

- Each VM gets 1024 bytes of memory only!
- The control program acquires and manages the physical resources in the system.
- Thanks to Direct PCIe Device assignment, virtual machines can make use of the RTX3090 available in our cloud.

The GPU is really powerful!

The hypervisor area stores **sensitive information** \*wink\* \*wink\*. 
