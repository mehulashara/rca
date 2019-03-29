#!/usr/bin/python
import subprocess
import sys

#def hypervisor():
hypervisor = sys.argv[1:]
str=''.join((str(e) for e in hypervisor))
if str.lower() == "vmware" or str.lower() == "acropolis" or str.lower() == "hyperv":
	print ("--------------- Running RCA script ---------------")
else:
	print ("Invalid input. Exiting ...")
	sys.exit(0)

HOST=subprocess.Popen("hostname -I | awk {'print $1'}", shell=True, stdout=subprocess.PIPE).stdout.read()
# Ports are handled in ~/.ssh/config since we use OpenSSH
COMMAND="uptime -p; date;"

ssh = subprocess.Popen(["ssh", "%s" % HOST, COMMAND],shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
result = ssh.stdout.readlines()
if result == []:
    error = ssh.stderr.readlines()
    print >>sys.stderr, "ERROR: %s" % error
else:
    print result

print ("!!!!!!!!!! ncli alert history duration=1 !!!!!!!!!!")
print subprocess.Popen("ncli alert history duration=1", shell=True, stdout=subprocess.PIPE).stdout.read()

print ("!!!!!!!!!! ncli alert ls max-alerts=20 !!!!!!!!!!")
print subprocess.Popen("ncli alert ls max-alerts=20", shell=True, stdout=subprocess.PIPE).stdout.read()

print ("!!!!!!!!!! hostssh 'uptime -p; date' !!!!!!!!!!")
print subprocess.Popen("hostssh 'uptime -p; date'", shell=True, stdout=subprocess.PIPE).stdout.read()

print ("!!!!!!!!!! hostssh '/ipmitool sel time get' !!!!!!!!!!")
print subprocess.Popen("hostssh '/ipmitool sel time get'", shell=True, stdout=subprocess.PIPE).stdout.read()

#print subprocess.Popen("hostname -I | awk {'print $1'}", shell=True, stdout=subprocess.PIPE).stdout.read()

print subprocess.call('__allssh', shell=True)
