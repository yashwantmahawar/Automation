# Ec2 Stop Start Instance

## Description

This lambda function will be used to start and stop the instance on time basis defined in the tags. It will start the instance on weekday only.

# How to use this lambda

### Step 1: Create lambda
Create two lambda functions with ec2-start.py and ec2-stop.py

### Step 2: Create cloudwatch alert rules with below cron value
Rule Name - start-ec2-instance</br>
Rule Scheduled Cron Expression -  `35 * ? * mon-fri *`</br>
Target - ec2-start lambda

Rule Name - stop-ec2-instance</br>
Rule Scheduled Cron Expression- `35 * ? * mon-saturday *`</br>
Target - ec2-stop lambda

### Step 3: Lambda role policy [Limited to nonprod only]
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "ec2:Describe*",
            "Resource": "*"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "ec2:StartInstances",
                "ec2:StopInstances"
            ],
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "aws:ResourceTag/environment": "nonprod"
                }
            }
        },
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:CreateLogGroup",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        }
    ]
}
```

### Add tags to the instance
Add tag `stop-start-duration` to the instance which you want to stop and start. Time format will be in 24 hrs IST.

##### example
```
1. stop-start-duation : 23:00:00-9:00:00
2. stop-start-duation : 1:00:00-9:00:00
```
Above example 1 value will stop the instance at 11 PM and start at 9 AM
Above example 2 value will stop the instance at 1 AM and start at 9 AM
