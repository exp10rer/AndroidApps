import boto3

# Debug y/n will print more statements
DBG = "N"
# HDRS n will not print any header statement, just data separated by ':' so that its easier to parse in excel
HDRS = "N"

# Parameters
EC2 = "ec2"
SPRTR = ";"
STOPPED_IP = "0.0.0.0"

# Instance states
RUNNING_ST = "running"
STOPPED_ST = "stopped"


def DbgPrint(message) :
    if (DBG == "Y"):
        print(message)

def getResource(service, region) :
    ec2Res = boto3.resource(service, region_name=region)
    return ec2Res

def getInstances(ec2Res, state) :
    DbgPrint("In getInstances : " + state)
    # Get instances based on the state-name filter
    instances = ec2Res.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': [state]}])

    DbgPrint("Got Instances")
    return instances

def printList(instList, state, region) :
    vmCount = 0
    outputStr = ""
    for instance in instList:
        vmCount = vmCount + 1
        # Only running instances have a valid public_ip_address, print 0.0.0.0 otherwise
        if state != RUNNING_ST:
            ipAddr = STOPPED_IP
        else:
            ipAddr = instance.public_ip_address

        # using 0 th index is risky, but I experimented a bit in the AWS console and found out that new
        # tags are added after the name tag. If names are not printing properly this is the first place to look.
        outputStr = outputStr + region + SPRTR + str(instance.tags[0]['Value']) + SPRTR + ipAddr\
                    + SPRTR + str(instance.instance_type) + SPRTR + state + SPRTR\
                    + str(instance.launch_time) + "\n"

    if HDRS == 'Y':
        print("There are " + str(vmCount) + " " + state + " VMs in AWS in the " + region + " region.")

    print(outputStr, end="")


if __name__ == "__main__":

    # Get the available region list first
    client = boto3.client(EC2)
    regions = client.describe_regions()['Regions']

    # For each region get the resource for accessing instances
    for region in regions:
        regName = region['RegionName']
        DbgPrint(regName)

        # Get the Ec2 resource from boto
        ec2Res = getResource(EC2, regName)

        # Print Running Instance List
        instList = getInstances(ec2Res, RUNNING_ST)
        printList(instList, RUNNING_ST, regName)

        # Print Stopped Instance List
        instList = getInstances(ec2Res, STOPPED_ST)
        printList(instList, STOPPED_ST, regName)

    DbgPrint("Exit")