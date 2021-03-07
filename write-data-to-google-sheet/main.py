import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import boto3
from _datetime import datetime

session = boto3.Session(profile_name='profilename')

# Create cloudwatch session
cloudwatch_client = session.client('cloudwatch')

# Create ec2 session
ec2_client = session.client('ec2')

# Create google sheet session
scope = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
]

file_name = 'client_key.json'
creds = ServiceAccountCredentials.from_json_keyfile_name(file_name, scope)
google_sheet_client = gspread.authorize(creds)

MatrixType = 'Maximum'

def getEC2PrivateIP(instanceid):
    if not instanceid.startswith("i-"):
        return 'Wrong instance id'
    response = ec2_client.describe_instances(
        InstanceIds = [instanceid]
    )
    if len(response['Reservations']) < 1:
        return 'Wrong instance id'

    if 'PrivateIpAddress' in response['Reservations'][0]['Instances'][0]:
        return response['Reservations'][0]['Instances'][0]['PrivateIpAddress']
    else:
        return 'No - IP'

def getEC2InstanceName(instanceid):
    if not instanceid.startswith("i-"):
        return 'Wrong instance id'
    response = ec2_client.describe_instances(
        InstanceIds = [instanceid]
    )
    if len(response['Reservations']) < 1:
        return 'Wrong instance id'

    for tag in response['Reservations'][0]['Instances'][0]['Tags']:
        if tag['Key'] == "Name":
            return tag["Value"]

    return "Not Found"


def getEC2InstanceType(instanceid):
    if not instanceid.startswith("i-"):
        return 'Wrong instance id'
    response = ec2_client.describe_instances(
        InstanceIds = [instanceid]
    )
    if len(response['Reservations']) < 1:
        return 'Wrong instance id'

    return response['Reservations'][0]['Instances'][0]['InstanceType']

def getEC2CpuMax(instanceid):
    response = cloudwatch_client.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': instanceid
            },
        ],
        StartTime=datetime(2021, 1, 1),
        EndTime=datetime(2021, 1, 14),
        Period=86400,
        Statistics=[MatrixType],
        Unit='Percent'
    )

    cpuUtilizationSummy = []
    for datapoint in response['Datapoints']:
        cpuUtilizationSummy.append(str(datapoint[MatrixType]).split(".")[0])

    return cpuUtilizationSummy


# Fetch the sheet
sheet = google_sheet_client.open("To-do list").worksheet('sheet1')
python_sheet = sheet.get_all_records()

output = []
for row in python_sheet:
    if row['Instance ID'] != "":
        instance_id = row['Instance ID'].strip(':')
        row['Instance ID'] = instance_id
        row["Private IP"] = getEC2PrivateIP(instance_id)
        row["Instance Name"] = (getEC2InstanceName(instance_id))
        row["Instance Type"] = (getEC2InstanceType(instance_id))
        #row["Max CPU Per hour"] = ",".join(getEC2CpuMax(instance_id))
        output.append(row)
        print(row)

records_df = pd.DataFrame.from_dict(output)
sheet = google_sheet_client.open("To-do list")
output = sheet.add_worksheet(rows=1000,cols=20,title='output')
#output = sheet.worksheet('test3')
output.insert_rows(records_df.values.tolist())
