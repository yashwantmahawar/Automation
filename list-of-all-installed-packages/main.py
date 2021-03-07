####
# Install below packages
# pip install boto3 pandas
#
# Execute python main.tf
####

import boto3
import os

## Static variables
environment = "all"
user_name = "yashwant_26858"
aws_region = "ap-south-1"
## Replace package name which you want to search.
package_list = '[ ! -f /etc/redhat-release ] || rpm -qa | grep -i \'redhat\|rhel\|red hat\';' \
    '[ ! -f /etc/debian_version ] || dpkg -l | grep -i \'redhat\|rhel\|red hat\';'
installed_packages = ""
details = []

## AWS sessions
#session = boto3.Session(profile_name='profilename',region_name=aws_region)
session = boto3.Session(profile_name='profilename')
ec2Client = session.client("ec2")
sts = session.client('sts')

account_id = sts.get_caller_identity()["Account"]
instances = ec2Client.describe_instances()["Reservations"]

## Write to file
f = open("output.csv", "w")

## Adding headers
f.write("Account ID,Instance ID,Name,Private IP,Environment,State,Installed Packages\n")

# Logging
print("Total Instances - "+str(len(instances)))
count = 0

for instance in instances:
    i = instance["Instances"][0]
    name = ""
    env = ""

    ## For logging purpose
    count=count+1

    for tag in i["Tags"]:
        key = tag["Key"].lower()

        if key == "name":
            name = tag["Value"]

        if key == "environment":
            env = tag["Value"]


    print("["+str(count)+"/"+str(len(instances))+"]",i["PrivateIpAddress"], name, i["State"]["Name"])
    #print(i["PrivateIpAddress"], name, installed_packages)

    if i["State"]["Name"].lower() == "running" and environment.lower() == "all" or environment.lower() == env:
        command = "ssh -o StrictHostKeyChecking=no "+user_name+"@"+i["PrivateIpAddress"]+" \""+package_list+"\""
        stream = os.popen(command)
        stream_output = stream.read()
        installed_packages = " ".join(stream_output.split("\n"))
    else:
        print(i["PrivateIpAddress"], name,"skipping")

    if installed_packages == "":
        installed_packages = "N/A"

    f.write(account_id+","+i["InstanceId"]+","+name+","+i["PrivateIpAddress"]+","+env+","+i["State"]["Name"]+","+installed_packages+"\n")
    details.append({
        "Account Id": account_id,
        "Instance Id": i["InstanceId"],
        "Instance Name": name,
        "IP": i["PrivateIpAddress"],
        "Environment": env,
        "State": i["State"]["Name"],
        "Package Info": installed_packages
    })

f.close()
# print(details)
