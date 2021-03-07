import boto3

def lambda_handler(event, context):
    
    ec2Client = boto3.client("ec2")
    instances = event["detail"]["responseElements"]["instancesSet"]["items"]
    
    
    for instance in instances:
        
        id = instance["instanceId"]
        
        ec2 = ec2Client.describe_instances(
            InstanceIds=[id]
        )
    
        volumeid = ec2["Reservations"][0]["Instances"][0]["BlockDeviceMappings"][0]["Ebs"]["VolumeId"]
    
        volume_details = ec2Client.describe_volumes(
            VolumeIds=[volumeid]
        )
    
        type = volume_details["Volumes"][0]["VolumeType"]
    
        if type.lower() == "gp2":
            
            print("Change volume type")
            ec2Client.modify_volume(
                VolumeId=volumeid,
                VolumeType="gp3"
            )
