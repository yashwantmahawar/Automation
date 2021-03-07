import boto3
import pandas as pd

session = boto3.Session(profile_name='profilename')
elbClient = session.client("elbv2")
ec2Client = session.client("ec2")

lbs = elbClient.describe_load_balancers()["LoadBalancers"]

tgs = elbClient.describe_target_groups()["TargetGroups"]

details = []

for lb in lbs:
    details.append({
        "lb_arn" : lb["LoadBalancerArn"],
        "lb_name": lb["LoadBalancerName"],
        "LBAvailabilityZones" : [zone["ZoneName"] for zone in lb["AvailabilityZones"]]
        })

for tg in tgs:
    for lb in details:
        for lb_in_tg in tg["LoadBalancerArns"]:
            if  lb["lb_arn"] == lb_in_tg:
                lb.update({"tg_arn":tg["TargetGroupArn"]})
                lb.update({"tg_name":tg["TargetGroupName"]})

for lb in details:
    healths = elbClient.describe_target_health(
        TargetGroupArn = lb["tg_arn"]
    )
    lb["instance"] = []
    for health in healths["TargetHealthDescriptions"]:
        instance_id = health["Target"]["Id"]
        if instance_id.startswith("i-"):
            i = ec2Client.describe_instances(
                InstanceIds = [instance_id]
            )
            lb["instance"].append({instance_id : i["Reservations"][0]["Instances"][0]["Placement"]["AvailabilityZone"]})

#print(tgs[0])

df = pd.json_normalize(details)
df.to_csv('output.csv', index=False, encoding='utf-8')
