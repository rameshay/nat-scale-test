import boto3

def populate_iplist(ReservationsDict):
    IpList = []
    if ReservationsDict['ResponseMetadata']['HTTPStatusCode'] == 200:
        for resv in ReservationsDict['Reservations']:
            for inst in resv['Instances']:
                for ii in inst['NetworkInterfaces']:
                    for ips in ii['PrivateIpAddresses']:
                        IpList.append(ips['PrivateIpAddress'])
    return IpList


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

clientIpList = populate_iplist(ClientRespDict)
serverIpList = populate_iplist(ServerRespDict)

print "Client Ip List:", clientIpList , "total ", len(clientIpList)
print "Server Ip List:", serverIpList , "total ", len(serverIpList)
