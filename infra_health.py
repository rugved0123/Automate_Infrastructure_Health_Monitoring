#  script created to Automate Infrastructure Health Monitoring

import boto3 
from datetime import datetime
import os
import json
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


session = boto3.Session(profile_name='rugved-aws2')

ec2 = session.resource('ec2')
rds_client = session.client('rds')


instances = []

#getting the list of all the instances running: 
def instance_list():
   instances = os.popen("aws ec2 describe-instances --profile rugved-aws2").read()
   instance_data = json.loads(instances)
   if 'Reservations' in instance_data:
      for reservation in instance_data['Reservations']:
         for instance in reservation['Instances']:
            InstanceId = instance['InstanceId']
            health_status = instance_health_status(InstanceId)
   rds_health_status()
            
         
#checking the health status of the instances:
def instance_health_status(InstanceId):
   response = ec2.meta.client.describe_instance_status(InstanceIds=[InstanceId])['InstanceStatuses']
   for data in range(len(response)):
      response_json = response[data]
      status = str(response[data])
      if 'InstanceStatus' in response_json and isinstance(response_json['InstanceStatus'], dict):
         instance_details = response_json['InstanceStatus'].get('Details', [])
         for detail in instance_details:
            if isinstance(detail, dict) and detail.get('Name') == 'reachability':
               instance_status_passed = detail.get('Status')
               if instance_status_passed == "passed":
                  # logging = log_health_status(status)
                  log_health_status(InstanceId, instance_status_passed)
               else:
                  send_slack_notifications(InstanceId)
                  
# Checking the health status of RDS instances
def rds_health_status():
    response = rds_client.describe_db_instances()
    for db_instance in response['DBInstances']:
        db_instance_id = db_instance['DBInstanceIdentifier']
        db_instance_status = db_instance['DBInstanceStatus']
        log_health_status(db_instance_id, db_instance_status)
        if db_instance_status != 'available':
            send_slack_notifications(db_instance_id)

#logging the health status of each service in a log file:
def log_health_status(InstanceId,status):
   timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   with open("/var/log/infra_healthcheck.log","a") as logfile:
      logfile.write(f"{timestamp} - Instance ID: {InstanceId}, Status: {status}\n")   


#sending status notifications over slack:
def send_slack_notifications(instance_id):
   slack_webhook_url = "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"
   slack_message = {
            "type": "home",
            "blocks": [
                {
                    "type": "divider"
                },
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "AWS_ALERT"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f'The instance {instance_id} seems to be down'
                        }

                    ]
                }
            ]
        }
   
   response = requests.post(slack_webhook_url, data=json.dumps(slack_message), headers={'Content-Type': 'application/json'})
   # Check for success or failure
   if response.status_code == 200:
      print("Notification sent successfully!")
   else:
      print(f"Failed to send notification. Status code: {response.status_code}, Response: {response.text}")

#sending status notifications over email:(only if needed)
def send_email_notifications():
   def send_email(subject, body, recipient_email):
    sender_email = 'your_email@gmail.com'  
    sender_password = 'your_email_password'  
    
    
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    
    
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject
    
    
    message.attach(MIMEText(body, 'plain'))  
    
    try:
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  
        server.login(sender_email, sender_password)  
        
        
        server.sendmail(sender_email, recipient_email, message.as_string())
        print(f'Email sent successfully to {recipient_email}')
        
    except Exception as e:
        print(f'Failed to send email. Error: {str(e)}')
        


# Start the instance health monitoring
if __name__ == "__main__":
    instance_list()

