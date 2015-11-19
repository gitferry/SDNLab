'''
Coursera:
- Software Defined Networking (SDN) course
-- Module 3 Programming Assignment

Professor: Nick Feamster
Teaching Assistant: Muhammad Shahbaz
'''

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import irange, dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import CPULimitedHost
from mininet.link import TCLink

class CustomTopo(Topo):
    "Simple Data Center Topology"

    "linkopts - (1:core, 2:aggregation, 3: edge) parameters"
    "fanout - number of child switch per parent switch"
    def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)

        self.fonout = fanout

        # Add core switch
        cs_switch = self.addSwitch('cs%s' % 1)

        # Add aggregation switches
        for i in irange(1, fanout):
            as_switch = self.addSwitch('as%s' % i)
            self.addLink(as_switch, cs_switch, **linkopts1)
            as_parent_switch = as_switch
 
            # Add edge switches
            for j in irange(1, fanout):
                es_num = i * fanout - 2 + j
                es_switch = self.addSwitch('es%s' % es_num, **linkopts2)
                self.addLink(es_switch, as_parent_switch)
                es_parent_switch = es_switch
 
                # Add hosts
                for k in irange(1, fanout):
                    host_num = es_num * fanout - 2 + k
                    host = self.addHost('h%s' % host_num, cpu=.5/fanout)
                    self.addLink(host, es_parent_switch, **linkopts3)
 
def perTest():
    "Specify performance parameters for the links"
    # Between core and aggregation switches
    linkopts1 = dict(bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
    # Between aggregation and edge switches
    linkopts2 = dict(bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
    # Between edge switches and hosts
    linkopts3 = dict(bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)

    "Create and test a simple network"
    topo = CustomTopo(linkopts1=linkopts1, linkopts2=linkopts2, linkopts3=linkopts3, fanout=2)
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()

    print "Dumping host connections"
    dumpNodeConnections(net.hosts)

    print "Testing network connectivity"
    net.pingAll()

    print "Testing bandwidth between h1 with h2, h3 and h5"
    h1, h2 = net.get('h1', 'h2')
    net.iperf( ( h1, h2 ) )
    h1, h3 = net.get('h1', 'h3')
    net.iperf( ( h1, h3 ) )
    h1, h5 = net.get('h1', 'h5')
    net.iperf( ( h1, h5 ) )
    h1, h7 = net.get('h1', 'h7')
    net.iperf( ( h1, h7 ) )

    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    perTest()

# topos = { 'custom': ( lambda: CustomTopo() ) }
