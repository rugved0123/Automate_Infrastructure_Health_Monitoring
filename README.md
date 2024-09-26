# Automate_Infrastructure_Health_Monitoring



Objective: Develop a Python script or any of your choice programming language that
automates the monitoring of AWS infrastructure. The script should check the health of
specified AWS resources (e.g., EC2 instances, RDS databases) at regular intervals, log
the results, and send notifications if any service goes down.

Task Details:

1. Infrastructure Health Check:

Overview
This Python script automates the monitoring of AWS infrastructure, specifically EC2 instances and RDS databases. It checks the health status of specified resources at regular intervals, logs the results, and sends notifications via Slack if any service goes down

Prerequisites

Before running the script, ensure you have the following:

1. AWS Account: You must have access to an AWS account with the necessary permissions to describe EC2 and RDS instances.

2. AWS CLI: Install the AWS CLI and configure it with your credentials. You can set this up by running:aws configure

3. Python Environment: Ensure you have Python 3.x installed.

4. Required Libraries: Install the necessary Python packages. pip install boto3 requests

5. Slack Webhook URL: Set up a Slack webhook for notifications. 

Executing Script:

1. Update the slack_webhook_url with your actual Slack webhook URL.

2. Modify the send_email_notifications() function with your email credentials if you plan to use email notifications.

3. Log File Path: Ensure the directory where the log file (/var/logs/infra_healthcheck.log) is stored is writable by the script.

4. To run the script, open your terminal or command prompt and execute the following command:             python health_monitor.py
