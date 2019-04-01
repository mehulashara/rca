#!/usr/bin/python
#------------------------------------------------------------------------#
# File name: rca.py
# Author: Mehul Ashara  
# Email: mehul.ashara@nutanix.com
# Date created: 04/01/2019
# Date last modifed: 04/01/2019
# Python version: 2.7.5
# Purpose: This hypervisor agnostic script is to be run from CVM to simplify 
# RCA process for SREs. 
# Usage: rca.py >> /home/nutanix/tmp/rca_"$(date +"%Y-%m-%d_%H-%M").log"
#-------------------------------------------------------------------------#
import subprocess
import sys

def find_hypervisor():
	hypervisor=""
	try:
		hyper =subprocess.Popen("ncli ms ls | grep -i hypervisor | awk {'print $4'} | head -n 1", shell=True, stdout=subprocess.PIPE).stdout.read()
		hypervisor="".join((str(e) for e in hyper))
		print "--------------- Hypervisor detected",hypervisor[:-1],"---------------"

		if hypervisor[:-1].lower() == "vmware":
			hypervisor="vmware"
		elif hypervisor[:-1].lower() == "acropolis":
			hypervisor="acropolis"
		elif hypervisor[:-1].lower() == "hyperv":
			hypervisor="hyperv"
	except:
		print "-----------------Unknown Hypervisor ! AHV ! ESXi ! Hyper-V -------------"
		sys.exit()
	return hypervisor	

def rca_out(hypervisor):
	try: 
		if hypervisor == "vmware":
                        print "--------------- Running RCA script ---------------"
                        print "!!!!!!!!!! hostssh '/ipmitool sel time get' !!!!!!!!!!"
                        print subprocess.Popen("hostssh '/ipmitool sel time get'", shell=True, stdout=subprocess.PIPE).stdout.read()
                elif hypervisor == "acropolis":
                        print ("--------------- Running RCA script ---------------")
                        print ("!!!!!!!!!! hostssh 'ipmitool sel time get' !!!!!!!!!!")
                        print subprocess.Popen("hostssh 'ipmitool sel time get'", shell=True, stdout=subprocess.PIPE).stdout.read()
                elif hypervisor == "hyperv":
                        print ("--------------- Running RCA script ---------------")
                        print ("!!!!!!!!!! ""hostssh systeminfo | findstr Time"" !!!!!!!!!!")
                        print subprocess.Popen("hostssh 'systeminfo | findstr time'", shell=True, stdout=subprocess.PIPE).stdout.read()

		cvms=subprocess.Popen("svmips", shell=True, stdout=subprocess.PIPE).stdout.read()
		cvmx="".join((str(e) for e in cvms))
		cvms=cvmx.split(' ')
		print "!!!!!!!!!!!!!!!!!!!!! allssh 'uptime -p ; date' !!!!!!!!!!!!!!!!"
		for i in range(len(cvms)):
        		HOST=cvms[i]
# Ports are handled in ~/.ssh/config since we use OpenSSH
        	COMMAND="uptime -p; date;"
        	ssh = subprocess.Popen(["ssh", "%s" % HOST, COMMAND],shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        	result = ssh.stdout.readlines()
        	if result == []:
                	error = ssh.stderr.readlines()
                	print >>sys.stderr, "ERROR: %s" % error
        	else:
                	print cvms[i]
                	for i in range(len(result)):
				print result[i]

		print "!!!!!!!!!! hostssh 'uptime -p; date' !!!!!!!!!!!!"
		print subprocess.Popen("hostssh 'uptime -p; date'", shell=True, stdout=subprocess.PIPE).stdout.read()

		print "!!!!!!!!!! ncli alert history duration=1 !!!!!!!!!!"
		print subprocess.Popen("ncli alert history duration=1", shell=True, stdout=subprocess.PIPE).stdout.read()

		print "!!!!!!!!!! ncli alert ls max-alerts=20 !!!!!!!!!!!!"
		print subprocess.Popen("ncli alert ls max-alerts=20", shell=True, stdout=subprocess.PIPE).stdout.read()

		print "!!!!!!!!!! allssh 'ls -lrth ~/data/logs/*FATAL'; date !!!!!!!!!"
		for i in range(len(cvms)):
        		HOST=cvms[i]
# Ports are handled in ~/.ssh/config since we use OpenSSH
        	COMMAND="ls -lrth ~/data/logs/*FATAL;date"
        	ssh = subprocess.Popen(["ssh", "%s" % HOST, COMMAND],shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        	result = ssh.stdout.readlines()
        	if result == []:
                	error = ssh.stderr.readlines()
                	print >>sys.stderr, "ERROR: %s" % error
        	else:
                	print "................................... CVM "+ cvms[i] +" ..............................."
                	for i in range(len(result)):
                        	print result[i]

		print "-------------------------- Cluster details, status and FT status ----------------------------"

		print "!!!!!!!!!!!!!!! CVM IPs: svmips !!!!!!!!!!!!!!!!!!!!!!"
		print subprocess.Popen("svmips", shell=True, stdout=subprocess.PIPE).stdout.read()

		print "!!!!!!!!!!!!!!! Host IPs: hostips !!!!!!!!!!!!!!!!!!!!"
		print subprocess.Popen("hostips", shell=True, stdout=subprocess.PIPE).stdout.read()

		print "!!!!!!!!!!!!!!! Cluster Info: ncli cluster info !!!!!!!!!!!!!!!"
		print subprocess.Popen("ncli cluster info", shell=True, stdout=subprocess.PIPE).stdout.read()

		print "!!!!!!!!!!!!!!! Host Info: ncli host ls !!!!!!!!!!!!!!!!!!!"
		print subprocess.Popen("ncli host ls", shell=True, stdout=subprocess.PIPE).stdout.read()

		print "!!!!!!!!!!!!!!! NCLI MS LS: ncli ms ls !!!!!!!!!!!!!!!!!!!"
		print subprocess.Popen("ncli ms ls", shell=True, stdout=subprocess.PIPE).stdout.read()

		print "!!!!!!!!!!!!!!! NCC version: ncc --version !!!!!!!!!!!!!!!"
		print subprocess.Popen("ncc --version", shell=True, stdout=subprocess.PIPE).stdout.read()

		print "!!!!!!!!!!! Cluster status: cluster status | grep -v UP !!!!!!!!!!!!!!!!"
		print subprocess.Popen("cluster status | grep -v UP", shell=True, stdout=subprocess.PIPE).stdout.read()

		print "!!!!!!!!!!!!!!!! Cluster metadata: nodetool -h 0 ring !!!!!!!!!!!!!!!!!!!!!!!!"
		print subprocess.Popen("nodetool -h 0 ring", shell=True, stdout=subprocess.PIPE).stdout.read()

		print "!!!!!!!!!!!!!!!! Cluster data resiliency: ncli cluster get-domain-fault-tolerance-status type=node !!!!!!!!!!!!!!!!!"
		print subprocess.Popen("ncli cluster get-domain-fault-tolerance-status type=node", shell=True, stdout=subprocess.PIPE).stdout.read()

		print "!!!!!!!!!! Curator Jobs History: links http://0:2010 -dump !!!!!!!!!!!!"
		print subprocess.Popen("links http://0:2010 -dump", shell=True, stdout=subprocess.PIPE).stdout.read()

		print "!!!!!!!!!! NCC health check: ncc health_checks run_all !!!!!!!!!!"
		print subprocess.Popen("ncc health_checks run_all", shell=True, stdout=subprocess.PIPE).stdout.read()

	except:
		print "-------------------- Uhh! Something went wrong , are you sure you are running this from CVM? ---------------"
		sys.exit()

def main():
	hypervisor = find_hypervisor()
	rca_out(hypervisor)

if __name__ == "__main__":
	main()
