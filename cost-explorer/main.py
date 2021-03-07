import boto3
import json
import argparse

parser = argparse.ArgumentParser("example: \npython example.py --start 2020-11-01 --end 2020-12-01 --team merchant_bpay --region ap-south-1 --metrics UnblendedCost\n"
                                 "python example.py --start 2020-11-01 --end 2020-12-01 --team merchant_bpay\n")

parser.add_argument("--start", help="start date, example 2020-11-01")
parser.add_argument("--end", help="end date, example 2020-11-01")
parser.add_argument("--team", help="techteam")
parser.add_argument("--region", help="aws region, default set to ap-south-1")
parser.add_argument("--metrics", help="which metrics are returned in query, default is UnblendedCost. Allowd values are [AmortizedCost, BlendedCost, NetAmortizedCost, NetUnblendedCost, NormalizedUsageAmount, UnblendedCost, UsageQuantity]")
args = parser.parse_args()

startDate = args.start
endDate = args.end
team = args.team
metrics = args.metrics
region = args.region

if metrics is None:
    metrics = "UnblendedCost"
if region is None:
    region = "ap-south-1"

#session = boto3.Session(profile_name='awsprofilename')
#ceClient = session.client('ce')

ceClient = boto3.client('ce')

responses = ceClient.get_cost_and_usage(
    TimePeriod={
        'Start': args.start,
        'End': args.end
    },
    Metrics=[metrics],
    Granularity='MONTHLY',
    Filter={
        "And": [
            {
                "Tags": {
                    "Key": "techteam",
                    "Values": [team]
                }
            },
            {
                "Dimensions": {
                    "Key": "REGION",
                    "Values": [region],
                    "MatchOptions": ["EQUALS"]
                }
            }
        ]
    }
)
total = 0.0

resultsByTime = json.loads(json.dumps(responses))

for result in resultsByTime["ResultsByTime"]:
    total = total + float(result["Total"]["UnblendedCost"]["Amount"])

print(responses)
print(total)
