## ec2deploy

# Table of contents
[About](#about)

[Installation](#installation)

[Running the script](#running-the-script)

[How it works](#how-it-works)

# About
This is to help Windows users deploy code to EC2, however it should work with Unix (Mac OS X) as well.

# Installation
1. Have [AWS account](http://aws.amazon.com/) set up. This code works with free tier, but you'll still need to input payment information.
2. This free script assumes you've already run EC2 at least once (it uses the default VPC and subnet from previous set up). If you are making a new VPC and subnet from scratch, head over to [samchaaa++](https://samchaaa.substack.com/) for the premium code.
3. Install [AWS CLI](https://aws.amazon.com/cli/). [Direct download (for Windows).](https://awscli.amazonaws.com/AWSCLIV2.msi)
4. Configure AWS CLI. [Quickstart](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)
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

# Running the script
1. Navigate to repo in cmd
2. `python ec2deploy.py`
3. That's it!

# How it works
How it works here.
