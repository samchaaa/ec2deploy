
# Start, upload code, and run in 5 steps (for Windows).

# Assumes you already have AWS account set up with the basics. Helps if you've created an instance before manually.

# Download AWS CLI first: https://aws.amazon.com/cli/
    # Direct link: https://awscli.amazonaws.com/AWSCLIV2.msi
    
# Configure: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html
    # $ aws configure
    # AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
    # AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
    # Default region name [None]: us-west-2
    # Default output format [None]: json

# Install paramiko
    # !pip install paramiko

import json
import time
import os
import shutil
import sys
from subprocess import check_output
from datetime import datetime
from dateutil.parser import *
import paramiko

region = 'us-east-1'
image = 'ami-0947d2ba12ee1ff75' # Free tier Amazon Linux 2 AMI
fname = 'upload'
path = os.getcwd() + '/' + fname

# Name of file inside of upload to execute
to_execute = 'btc_algo.py'

# Set key name here
key_name = str(int(time.time()))

# Zip upload folder
zip_path = shutil.make_archive(fname, 'zip', fname)
zip_fname = fname + '.zip'

# Inner folder of upload (to run later)
inner = os.listdir(fname)[0]

def aws_cli(command):
    output = check_output(
        command,
        shell=True
    )
    if output != b'':
        output = json.loads(output)
        return output
    
# Get default VPC
output = aws_cli('aws ec2 describe-vpcs --filter "Name=isDefault,Values=true"')
print(output)
vpc = output['Vpcs'][0]['VpcId']

# Get subnet for default VPC
output = aws_cli('aws ec2 describe-subnets --filter "Name=vpc-id,Values={}"'.format(vpc))
print(output)
subnet = output['Subnets'][0]['SubnetId']

# Make new security group
# Note: needs to belong to proper network (same as subnet)
output = aws_cli("aws ec2 create-security-group --vpc-id {} --group-name {} --description {}".format(vpc, key_name, key_name))
print(output)
sg = output['GroupId']

# Edit inbound rules
output = aws_cli('aws ec2 authorize-security-group-ingress --group-id {} --protocol tcp --port 22 --cidr 0.0.0.0/0'.format(sg))

# Create key
output = aws_cli("aws ec2 create-key-pair --key-name {} --output text > {}.pem".format(key_name, key_name))

# The key is generating with fingerprint up front, which confuses paramiko (later in script)
key_str = open('{}.pem'.format(key_name), 'r').read()

# Have to remove the fingerprint up front for some reason
with open('{}.pem'.format(key_name), 'w') as w:
    w.write(key_str[key_str.index('-----'):])
key_str = open('{}.pem'.format(key_name), 'r').read()
print(key_str)

# Runs EC2
output = aws_cli("aws ec2 run-instances --image-id {} --count 1 --instance-type t2.micro --key-name {} --security-group-ids {} --subnet-id {}".format(image, key_name, sg, subnet))
print(output)
inst = output['Instances'][0]['InstanceId']

# Wait until status checks complete
while True:
    output = aws_cli('aws ec2 describe-instance-status --instance-id {}'.format(inst))
    if len(output['InstanceStatuses']):
        if output['InstanceStatuses'][0]['InstanceStatus']['Status'] == 'initializing':
            print('initializing, waiting 10 seconds...')
            time.sleep(10)
        else:
            print(output)
            break
    else:
        print('waiting 10 seconds...')
        time.sleep(10)

# Get public DNS
output = aws_cli('aws ec2 describe-instances --instance-id {}'.format(inst))
print(output)
dns = output['Reservations'][0]['Instances'][0]['PublicDnsName']

# Initialize SSHClient w/paramiko
k = paramiko.RSAKey.from_private_key_file(
    "{}.pem".format(key_name)
)
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# SSHClient connect is the most finicky part, if you miss anything from above \
# (mismatched regions, no automatically assigned IP addresses, no inbound rules for security group), \
# this will fail to connect.
c.connect(hostname=dns, username="ec2-user", pkey=k)
sftp = c.open_sftp()

# Upload zip file
upload = sftp.put(
    zip_path,
    '/home/ec2-user/' + zip_fname
)

# .read() will read until EOF, causing the script to run forever
# use .shutdown_write() and sys to close the channel before reading
def exec_shutdown_write(c, command):
    stdin, stdout, stderr = c.exec_command(command)
    stdout.channel.shutdown_write()
    return sys.stdout.write(str(stdout.read()))

# Unzip
exec_shutdown_write(c, 'unzip -o ' + fname)

# Check if upload complete
exec_shutdown_write(c, 'ls')

# Install numpy
exec_shutdown_write(c, 'sudo yum -y install numpy')

# Start python script in detached screen
exec_shutdown_write(c, 'screen -d -m -S test python {}/{}'.format(inner, to_execute))

# Check screen is detached
exec_shutdown_write(c, 'screen -ls')

# Check python is running
exec_shutdown_write(c, 'ps -aux | grep python')

c.close()