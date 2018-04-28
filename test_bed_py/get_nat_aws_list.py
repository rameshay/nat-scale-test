#
# This tool will return the client and server instances ip addresses
# This is handy when developing code and trying to run multiple ssh sessions
# Before running this command one should run the alias aws-configure which wil
# setup authentication with MFA
#


import boto3

def populate_iplist (ReservationsDict, publicIpAddressFlag):
    privIpList = []
    publicIpList = []
    if ReservationsDict['ResponseMetadata']['HTTPStatusCode'] == 200:
        for resv in ReservationsDict['Reservations']:
            for inst in resv['Instances']:
                # print inst['PrivateIpAddress']
                privIpList.append(inst['PrivateIpAddress'])
                if(publicIpAddressFlag):
                    # print inst['PublicIpAddress']
                    publicIpList.append(inst['PublicIpAddress'])
    if (publicIpAddressFlag):
        return privIpList, publicIpList
    else:
        return privIpList

import sys
def printf(format, *args):
    sys.stdout.write(format % args)

ec2 = boto3.client('ec2')
filterServer = [
    {
        'Name': 'tag-value',
        'Values': ['CLOJURE_SERVER']
    }
]
filterClient = [
    {
        'Name': 'tag-value',
        'Values': ['CLOJURE_CLIENT']
    }
]
ClientRespDict = ec2.describe_instances(Filters=filterClient)
ServerRespDict = ec2.describe_instances(Filters=filterServer)

ClientIpList = populate_iplist(ClientRespDict, False)
ServerIpListPriv, ServerIpListPublic = populate_iplist(ServerRespDict, True)


print "Client Ip List:"
for x in range(len(ClientIpList)):
    print ClientIpList[x]
print "total ", len(ClientIpList)

print "Server Ip private List:"
for x in range(len(ServerIpListPriv)):
    print ServerIpListPriv[x]
print "total ", len(ServerIpListPriv)

print "Server Ip public List:"
for x in range(len(ServerIpListPublic)):
    print "ssh ec2-user@", ClientIpList[x], "sudo echo \"",\
            ServerIpListPublic[x], " www.testnat.com\" >> /etc/hosts"
print "total ", len(ServerIpListPublic)
