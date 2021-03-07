# Ec2 Stop Start Instance

## Description

This lambda function will be used to start and stop the instance on time basis defined in the tags.


# How to use this lambda

### Step 1: Create a cloudwatch alert rule with below cron value

Rule Name - start-ec2-instance</br>
Rule Scheduled Cron Expression -  `35 * ? * mon-fri *`

Rule Name - stop-ec2-instance</br>
Rule Scheduled Cron Expression- `35 * ? * mon-fri *`
