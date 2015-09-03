from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSController
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel
import sys

switch_count = int(sys.argv[1])
host_count = int(sys.argv[2])

#assuming host_count is always greater tha switch_count
host_q = host_count/switch_count
host_r = host_count%switch_count

class MyTopo( Topo ):

	def __init__( self ):
		Topo.__init__( self )

		global host_r

		# Add switches
		switch_list=[]
		for i in range(switch_count):
			switch_name = 's'+str(int(i+1))
			switch_list.append(self.addSwitch(switch_name))
			

		# Linking switches	
		for i in range(len(switch_list)-1):
			self.addLink(switch_list[i],switch_list[i+1])


		# Add hosts
		host_list=[]
		for i in range(host_count):
			host_name = 'h'+str(int(i+1))
			host_list.append(self.addHost(host_name))

		# Linking hosts
		counter = 0
		for i in range(len(switch_list)):
			for j in range(host_q):
				if (counter+1)%2 == 1:
					# fixing BW = 1mbps for odd hosts
					self.addLink(host_list[counter],switch_list[i],bw=1)
				else:
					# fixing BW = 2mbps for even hosts
					self.addLink(host_list[counter],switch_list[i],bw=2)	
				counter+=1
			if host_r != 0:
				if (counter+1)%2 == 1:
					self.addLink(host_list[counter],switch_list[i],bw=1)
				else:
					self.addLink(host_list[counter],switch_list[i],bw=2)
				counter+=1
				host_r-=1


#topos = {'myTopo': ( lambda: MyTopo() )}
setLogLevel('info')
topo = MyTopo()
net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink, controller=OVSController)

# handling even/odd exception, even hosts should be able to ping even and similarly for odd hosts
counter = 1
for i in range(2,host_count+1,2):
	str1='h'
	str2='127.0.0.'
	str2=str2+str(counter)
	counter = counter+1
	str1=str1+str(i)
	host_ip = net.get(str1)
	host_ip.setIP(str2,24)
counter = 1
for i in range(2,host_count+1,2):
	str1='h'
	str2='192.168.0.'
	str2=str2+str(counter)
	counter = counter+1
	str1=str1+str(i)
	host_ip = net.get(str1)
	host_ip.setIP(str2,29)

print "starting network topology"	
net.start()

print "Dumping host connections"
dumpNodeConnections(net.hosts)

print "Testing network connectivity"
net.pingAll()
net.stop()
