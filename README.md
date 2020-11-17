<!-- # Table of contents
[About](#about)
[Installation](#installation)
[Running the script](#running-the-script)
[How it works](#how-it-works) -->

# About
This script deploys code to EC2 in a single step, as simply as possible. It is written with Windows users in mind, but should work for Unix (Mac OS X) as well (not yet tested). Full explanation in [this Medium article.](/)

**What the script does not do is manage your cloud infrastructure.** It is just a one-off script to get your code in the cloud and running, ASAP. In order to terminate or manage your resources, you will need to do that manually or write your own script. For higher level ways to automate your cloud infrastructure, look into [Ansible](https://www.ansible.com/), [Terraform](https://www.terraform.io/), or [pyinfra](https://pyinfra.com/).

# Installation
1. Have [AWS account](http://aws.amazon.com/) set up. This code works with free tier, but you'll still need to input payment information.
2. This free script assumes you've already run EC2 at least once (it uses the default VPC and subnet from previous set up). 
**Note:** If you are making a new VPC and subnet from scratch, head over to [samchaaa++](https://samchaaa.substack.com/) for the premium code.
3. Install [AWS CLI](https://aws.amazon.com/cli/). 
[Direct download (for Windows).](https://awscli.amazonaws.com/AWSCLIV2.msi)
4. Configure AWS CLI. 
[Quickstart](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)
```$ aws configure
AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Default region name [None]: us-west-2
Default output format [None]: json
```
5. Install paramiko
`pip install paramiko`
6. Clone repo
`git clone https://github.com/samchaaa/ec2deploy.git`
7. The default code in upload is a bitcoin moving average crossover algorithm for Coinbase Pro [(explanation here)](https://samchaaa.medium.com/implement-this-simple-btc-usd-trend-following-algorithm-today-using-coinbase-pro-api-and-python-4c40998307ed). Replace credentials with your own, or replace the entire folder /upload contents with your own. Specify which .py file you want EC2 to run with `to_execute` (line 35).

# Running the script
1. Navigate to repo in cmd
2. `python ec2deploy.py`
3. That's it!

# How it works
The script uses the python library `subprocess` to make calls to AWS CLI in python.

It gets your default VPC, the subnet associated with that VPC, creates a new security group, generates a new key pair, then starts an EC2 instance.

Then using the python library `paramiko` the script connects to your ec2 instance (once it finishes starting up) and transfers your code to EC2.

Finally, the script unzips and runs your code in a detached screen before closing the connection.

# Additional support
Subscribe to my [Substack](https://samchaaa.substack.com/) for additional code (including creating fresh VPC, fresh substack, and quitting your python process on EC2) and future extensions.
