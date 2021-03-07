# Convert gp2 to gp3 for all new instances

## Description
This lambda will convert gp2 to gp3 for all newly launched instances in the account.

### Cloud watch Event Pattern
```
{
  "source": [
    "aws.ec2"
  ],
  "detail-type": [
    "AWS API Call via CloudTrail"
  ],
  "detail": {
    "eventSource": [
      "ec2.amazonaws.com"
    ],
    "eventName": [
      "RunInstances"
    ]
  }
}
```

### Iam policy
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
            "ec2:ModifyVolume",
            "ec2:Describe*"
            ],
            "Resource": "*"
        }
    ]
}
```
