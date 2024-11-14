
#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    controller = net.addController('c0', controller=RemoteController, ip='192.168.2.47', port=6633)

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, failMode='standalone')
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch, failMode='standalone')
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch, failMode='standalone')

    info( '*** Add routers\n')
    r4 = net.addHost('r4', cls=Node, ip='0.0.0.0')
    r4.cmd('sysctl -w net.ipv4.ip_forward=1')
    r5 = net.addHost('r5', cls=Node, ip='0.0.0.0')
    r5.cmd('sysctl -w net.ipv4.ip_forward=1')
    r6 = net.addHost('r6', cls=Node, ip='0.0.0.0')
    r6.cmd('sysctl -w net.ipv4.ip_forward=1')

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)

    # Additional hosts for each switch
    h4 = net.addHost('h4', cls=Host, ip='10.0.1.1', defaultRoute=None)
    h5 = net.addHost('h5', cls=Host, ip='10.0.2.1', defaultRoute=None)
    h6 = net.addHost('h6', cls=Host, ip='10.0.3.1', defaultRoute=None)

    info( '*** Add links\n')
    net.addLink(h1, s1)
    net.addLink(h2, s2)
    net.addLink(h3, s3)

    net.addLink(s1, r4)
    net.addLink(s2, r5)
    net.addLink(s3, r6)
    net.addLink(r4, r5)
    net.addLink(r5, r6)

    # Additional links to connect each new host to a switch
    net.addLink(h4, s1)
    net.addLink(h5, s2)
    net.addLink(h6, s3)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([controller])
    net.get('s2').start([controller])
    net.get('s3').start([controller])

    info( '*** Post configure switches and hosts\n')

    info( '*** Assign IP addresses to router interfaces and hosts\n')
    h1.cmd('ifconfig h1-eth0 192.168.1.10/24')
    h1.cmd('route add default gw 192.168.1.1')
    h4.cmd('ifconfig h4-eth0 192.168.1.11/24')
    h4.cmd('route add default gw 192.168.1.1')

    h2.cmd('ifconfig h2-eth0 192.168.2.10/24')
    h2.cmd('route add default gw 192.168.2.1')
    h5.cmd('ifconfig h5-eth0 192.168.2.11/24')
    h5.cmd('route add default gw 192.168.2.1')

    h3.cmd('ifconfig h3-eth0 192.168.3.10/24')
    h3.cmd('route add default gw 192.168.3.1')
    h6.cmd('ifconfig h6-eth0 192.168.3.11/24')
    h6.cmd('route add default gw 192.168.3.1')

    r4.cmd('ifconfig r4-eth0 192.168.1.1/24 up')
    r4.cmd('ifconfig r4-eth1 192.168.10.1/24 up')

    r5.cmd('ifconfig r5-eth0 192.168.2.1/24 up')
    r5.cmd('ifconfig r5-eth1 192.168.10.2/24 up')
    r5.cmd('ifconfig r5-eth2 192.168.20.1/24 up')

    r6.cmd('ifconfig r6-eth0 192.168.3.1/24 up')
    r6.cmd('ifconfig r6-eth1 192.168.20.2/24 up')

    r4.cmd('route add -net 192.168.2.0/24 gw 192.168.10.2')
    r4.cmd('route add -net 192.168.3.0/24 gw 192.168.10.2')
    r4.cmd('route add -net 192.168.20.0/24 gw 192.168.10.2')

    r5.cmd('route add -net 192.168.1.0/24 gw 192.168.10.1')
    r5.cmd('route add -net 192.168.3.0/24 gw 192.168.20.2')

    r6.cmd('route add -net 192.168.1.0/24 gw 192.168.20.1')
    r6.cmd('route add -net 192.168.2.0/24 gw 192.168.20.1')
    r6.cmd('route add -net 192.168.10.0/24 gw 192.168.20.1')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()






