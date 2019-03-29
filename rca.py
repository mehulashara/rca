#!/usr/bin/python
import subprocess
import sys

#def hypervisor():
hyper =subprocess.Popen("ncli ms ls | grep -i hypervisor | awk {'print $4'} | head -n 1", shell=True, stdout=subprocess.PIPE).stdout.read()
hypervisor="".join((str(e) for e in hyper))
print "--------------- Host detected",hypervisor[:-1],"---------------"

if hypervisor[:-1].lower() == "vmware":
        print "--------------- Running RCA script ---------------"
        print "!!!!!!!!!! hostssh '/ipmitool sel time get' !!!!!!!!!!"
        print subprocess.Popen("hostssh '/ipmitool sel time get'", shell=True, stdout=subprocess.PIPE).stdout.read()
elif hypervisor[:-1].lower() == "acropolis":
        print ("--------------- Running RCA script ---------------")
        print ("!!!!!!!!!! hostssh 'ipmitool sel time get' !!!!!!!!!!")
        print subprocess.Popen("hostssh 'ipmitool sel time get'", shell=True, stdout=subprocess.PIPE).stdout.read()
elif hypervisor[:-1].lower() == "hyperv":
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
                print result

print "!!!!!!!!!! hostssh 'uptime -p; date' !!!!!!!!!!!!"
print subprocess.Popen("hostssh 'uptime -p; date'", shell=True, stdout=subprocess.PIPE).stdout.read()

print "!!!!!!!!!! ncli alert history duration=1 !!!!!!!!!!"
print subprocess.Popen("ncli alert history duration=1", shell=True, stdout=subprocess.PIPE).stdout.read()

print "!!!!!!!!!! ncli alert ls max-alerts=20 !!!!!!!!!!!!"
print subprocess.Popen("ncli alert ls max-alerts=20", shell=True, stdout=subprocess.PIPE).stdout.read()
