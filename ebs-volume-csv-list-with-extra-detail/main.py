import boto3
import json
import csv

session = boto3.Session(profile_name='profilename')

# EBS client
ec2Client = session.client('ec2')
stsClient = session.client('sts')

accountId = ""
accountId = stsClient.get_caller_identity()['Account']

print(accountId)

allVolumes = ec2Client.describe_volumes()["Volumes"]

ebs_details_writer = ""
with open('ebs_details.csv', mode='w') as ebs_details:
    ebs_details_writer = csv.writer(ebs_details, delimiter=',', lineterminator='\n', quotechar='"', quoting=csv.QUOTE_MINIMAL)

for volume in allVolumes:
    ebs_details_writer.writerow([accountId, volume['VolumeId'], volume['Attachments']['InstanceId']])
