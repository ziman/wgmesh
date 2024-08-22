# wgmesh

Like tailscale but without the junk.

## topology

1. hub server: used only for coordination, untrusted, needs public ip address
2. node: connects to the hub to obtain the public addresses of other nodes
3. node connects to other nodes directly using the public addresses
   obtained from the hub
4. the hub is untrusted, access control is performed by each node separately
5. no central config file; use something like `cdist` or `puppet` to config each node

## usage

1. run wireguard + `wgmesh-hub` on the hub machine
2. open the hub port in the wg interface on the hub machine
3. run wireguard on the actual nodes and have it connect to the hub.
   You need normal wireguard config files, you just don't need the `Endpoint`
   fields (except for the hub node). `Endpoint` fields will be filled in
   at runtime by `wgmesh-update.py`.
4. the connection to the hub is used only to get information about other nodes
5. Run `wgmesh-update.py` periodically on each node. This will obtain other nodes'
   public addresses from the hub and set them in the local wg config.
6. Now the nodes can (hopefully) talk to one another.
7. Since the hub is untrusted, nodes should also firewall the wg connection to the hub.
   Or not. Up to your threat model. A good compromise could be leaving port 22 open
   to have relayed ssh access if p2p edges are broken and firewall everything else.

## related work

* [meshub](https://github.com/ziman/meshub) is a roll-your-own version of this
  kind of VPN from the era before wireguard.

* see [meshub#related-projects](https://github.com/ziman/meshub?tab=readme-ov-file#related-projects)
  for other related work
