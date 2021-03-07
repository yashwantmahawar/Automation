import json
import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context)
    
    # Create ec2 client object
    ec2Client = boto3.client("ec2")
    
    # Get all ec2 nonprod instance which have tag stopstart value true
    ec2 = ec2Client.describe_instances(
    Filters=[{'Name': 'tag:environment', 'Values': ["nonprod"]},
             {'Name': 'tag:stop-start-duration', 'Values': ["*"]}
             ])

    ids = []
    currtime = datetime.now()
    isttime = currtime + timedelta(hours=5,minutes=30)
    
    for instance in ec2["Reservations"]:
        
        i = instance["Instances"][0]
        
        if i["State"]["Name"].lower() == "stopped":
            id = i["InstanceId"]
            for tag in i["Tags"]:
                key = tag["Key"].lower()
                
                if key == "stop-start-duration":
                    starttime = datetime.strptime(tag["Value"].split("-")[1],"%H:%M:%S")
                    stoptime = datetime.strptime(tag["Value"].split("-")[0],"%H:%M:%S")
                    if stoptime.time() < starttime.time() and isttime.time() > starttime.time():
                        print("Starting instances")
                        ids.append(id)
                    elif stoptime.time() > starttime.time() and isttime.time() > starttime.time() and isttime.time() < stoptime.time():
                        print("Starting instances")
                        ids.append(id)
    
    print(ids)
    if len(ids) > 0:
        ec2Client.start_instances(InstanceIds=ids)

    return {
        'statusCode': 200,
        'body': json.dumps('Lambda executed completed')
    }
