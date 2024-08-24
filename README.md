# wgmesh

Run wgmesh on top of an existing wireguard configuration
and it'll update `Endpoint` parameters automatically as they change.
That's all it does.

## topology

1. hub server: used only for coordination, untrusted, needs public ip address
2. a malicious hub should only be able to cause DoS
3. node: connects to the hub to obtain the public addresses of other nodes
4. a node connects to other nodes directly using the public addresses
   obtained from the hub
5. the hub is untrusted, access control is performed by each node separately
6. no central config file; use something like `cdist` or `puppet` to config each node

## usage

1. run wireguard + `wgmesh-hub` on the hub machine
2. open the hub port in the wg interface on the hub machine
3. run wireguard on the actual nodes and have it make wg tunnels to the hub.
   You need normal wireguard config files, just the `Endpoint` fields
   of edge nodes will be filled in at runtime by `wgmesh-update.py`.
4. wgmesh uses the connection to the hub only to get information about other nodes
5. Run `wgmesh-update.py` periodically on each node. This will obtain other nodes'
   public addresses from the hub and set them in the local wg config.
6. Now the nodes can (hopefully) talk to one another.
7. Since the hub is untrusted, nodes should also probably firewall the wg connection
   to the hub.
   Or not. Up to your threat model. A good compromise could be leaving port 22 open
   to have relayed ssh access if p2p edges are broken and firewall everything else.

## related work

* [meshub](https://github.com/ziman/meshub) is a roll-your-own version of this
  kind of VPN from the era before wireguard.

* see [meshub#related-projects](https://github.com/ziman/meshub?tab=readme-ov-file#related-projects)
  for other related work
