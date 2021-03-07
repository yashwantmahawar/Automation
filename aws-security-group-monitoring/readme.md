# Security group monitoring for public port opening

## Description
Use this Lambda to get notified whenever anyone open the port for public.

# How to use this lambda

### Step 1: Create lambda
Create lambda function with lambda_function.py

### Step 2: Create cloudwatch alert rules with below event pattern
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
      "AuthorizeSecurityGroupIngress",
      "AuthorizeSecurityGroupEgress"
    ]
  }
}
```

### Step 3: Lambda role policy [Limited to nonprod only]
```
{
    "Version": "2012-10-17",
    "Statement": [
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
