import json
import os
from urllib.parse import urlencode
from urllib.request import Request, urlopen

def lambda_handler(event, context):
    
    print(event)
    
    # Replace with slack token
    token = "XXXXXXXXXXXXXXXXXXX"

    details = []
    sg_id = event["detail"]["requestParameters"]["groupId"]
    user = event["detail"]['userIdentity']["principalId"].split(":")[1]
    rule_type = ""
    if "egress" in str(event["detail"]["eventName"]).lower():
        rule_type = "egress"
    else:
        rule_type = "ingress"
    for e in event["detail"]["requestParameters"]["ipPermissions"]["items"]:

        if "items" in e["ipRanges"] and e["ipRanges"]["items"][0]["cidrIp"] == "0.0.0.0/0":
            details.append({
                "sg-id": sg_id,
                "port": e["fromPort"],
                "user": user,
                "cidr": e["ipRanges"]["items"][0]["cidrIp"],
                "type": rule_type
            })
        elif "items" in e["ipv6Ranges"] and e["ipv6Ranges"]["items"][0]["cidrIpv6"] == "::/0":
            details.append({
                "sg-id": sg_id,
                "port": e["fromPort"],
                "user": user,
                "cidr": e["ipv6Ranges"]["items"][0]["cidrIpv6"],
                "type": rule_type
            })
    print(details)
    attachments = []
    for detail in details:
        attachments.append({
            "color": "danger",
            "text": "*`" + str(detail["port"])+" open for public`*",
            "fields": [
                {
                    "title": "User",
                    "value": detail["user"],
                    "short": "false"
                },
                {
                    "title": "Port",
                    "value": str(detail["port"]),
                    "short": "true"
                },
                {
                    "title": "Sg-Id",
                    "value": "<https://ap-south-1.console.aws.amazon.com/ec2/v2/home?region=ap-south-1#SecurityGroups:search="+detail["sg-id"]+"|"+detail["sg-id"]+">",
                    "short": "true"
                },
                {
                    "title": "Type",
                    "value": detail["type"],
                    "short": "true"
                },
                {
                    "title": "CIDR",
                    "value": detail["cidr"],
                    "short": "true"
                }
            ]
        }) 
    alert_data = {
                        "attachments": attachments
                    }
    print(alert_data)
    webhook_url = 'https://hooks.slack.com/services/'+token
    request = Request(
            webhook_url,
            data=json.dumps(alert_data).encode(),
            headers={'Content-Type': 'application/json'}
        )
    response = urlopen(request)
    print(response.getcode())
    print (response.read().decode())
    print(detail)

    return {
            'statusCode': response.getcode(),
            'body': response.read().decode()
    }
