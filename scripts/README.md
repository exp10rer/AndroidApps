# Scripts

## Ec2InstanceList.py

Uses boto3 python library. To install run:

*pip install boto3*

Initial Config:
If you have the AWS CLI installed, then you can use it to configure your credentials file:

*aws configure*

Alternatively, you can create the credential file yourself. By default, its location is at ~/.aws/credentials:

[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY

Once you have setup the credentials run this script to get the image list:

*python Ec2InstanceList.py*


