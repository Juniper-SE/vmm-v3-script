# output of sunbeam cluster list

    ubuntu@node1:~$ sunbeam cluster list
                        openstack-machines
    ┏━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┓
    ┃ Node       ┃ Cluster ┃ Machine ┃ Compute ┃ Control ┃ Storage ┃
    ┡━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━┩
    │ 10.3.200.1 │         │ running │ active  │ active  │ active  │
    │ node2      │ ONLINE  │ running │ active  │ active  │ active  │
    │ node3      │ ONLINE  │ running │ active  │ active  │ active  │
    │ node4      │ ONLINE  │ running │ active  │         │ active  │
    └────────────┴─────────┴─────────┴─────────┴─────────┴─────────┘
    ubuntu@node1:~$ sunbeam cluster resize
    Resize complete.
    ubuntu@node1:~$ sunbeam cluster list
                        openstack-machines
    ┏━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┓
    ┃ Node       ┃ Cluster ┃ Machine ┃ Compute ┃ Control ┃ Storage ┃
    ┡━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━┩
    │ 10.3.200.1 │         │ running │ active  │ active  │ blocked │
    │ node2      │ ONLINE  │ running │ active  │ active  │ active  │
    │ node3      │ ONLINE  │ running │ active  │ active  │ active  │
    │ node4      │ ONLINE  │ running │ active  │         │ active  │
    └────────────┴─────────┴─────────┴─────────┴─────────┴─────────┘
