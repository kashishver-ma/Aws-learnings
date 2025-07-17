# 🚀 AWS EC2 - Launch & SSH Connect Guide

This project demonstrates how to launch a basic EC2 instance on AWS and connect to it using SSH from your local machine.

---

## 🎯 Objective

- Launch an EC2 instance (Amazon Linux 2)
- Connect to the instance via SSH using a key pair

---

## 🪜 Step-by-Step Instructions

### ✅ 1. Launch EC2 Instance

1. Go to **AWS Console** → **EC2 Dashboard** → Click **"Launch Instance"**
2. Name the instance as you like.
3. Choose **Amazon Linux 2 AMI (x86_64)**
4. Choose instance type: `t2.micro` (free tier eligible)
5. Select or **create a new key pair** (e.g., `my-key.pem`)
6. Configure **Network settings**:
   - Allow **SSH (Port 22)** from your IP or `0.0.0.0/0` (for testing only)
7. Leave defaults or customize as needed
8. Click **Launch Instance**

---

### ✅ 2. Connect via SSH

Once the instance is in **"running"** state:

```bash
ssh -i "path/to/my-key.pem" ec2-user@<public-ip-address>
```

⚠️ Common Errors & Fixes
🔸 1. InvalidKeyPair.NotFound
Cause: Key name used in run-instances doesn't exist in selected region.
Fix: Create the key pair in that region:

bash
Copy
Edit
aws ec2 create-key-pair --key-name my-key --query "KeyMaterial" --output text > my-key.pem
🔸 2. Load key "...": invalid format
Cause: .pem file is corrupted or saved in incorrect format (e.g., HTML instead of raw text)
Fix:

Recreate key using AWS Console (RSA, .pem)

Ensure file starts with:

vbnet
Copy
Edit
-----BEGIN RSA PRIVATE KEY-----
🔸 3. Permission denied (publickey)
Cause: Key doesn’t match the instance’s assigned key pair
Fix:

Ensure the .pem file is the one selected while launching the instance

Terminate and re-launch instance if the key is lost

🔸 4. Connection timed out
Cause: SSH port (22) is blocked by security group
Fix:

Edit Security Group → Inbound rules → Add:

text
Copy
Edit
Type: SSH
Port: 22
Source: 0.0.0.0/0 (for testing) or your IP

###Some common cli commands:

#aws ec2 describe-instances
#aws ec2 start-instances --instance-ids i-12345678
#aws ec2 start-instances --instance-ids i-1234567890abcdef0 --region ap-south-1
#aws ec2 stop-instances --instance-ids i-1234567890abcdef0 --region ap-south-1
#aws ec2 describe-key-pairs --region ap-south-1

🔐 1. SSH into EC2 Instance
bash

ssh -i /path/to/your-key.pem ec2-user@<public-ip>
✅ Replace:

/path/to/your-key.pem with your actual PEM file path

<public-ip> with your instance’s public IPv4 address

👇 Examples

Amazon Linux 2 / RHEL:

bash

ssh -i "Downloads/my-key.pem" ec2-user@3.110.47.167

Ubuntu:

bash

ssh -i "Downloads/my-key.pem" ubuntu@3.110.47.167

⚠️ 2. Common SSH Errors & Fixes

Error Reason Fix
Permission denied (publickey) Wrong key, user, or IP Make sure key, user (e.g., ec2-user), and IP match
Load key ... invalid format Key file is corrupted or copied incorrectly Recreate the key properly using AWS CLI or console
Port 22: Connection timed out Port 22 not open in security group Edit inbound rules in security group and allow port 22 from 0.0.0.0/0
UNPROTECTED PRIVATE KEY FILE! Key file permissions too open Run chmod 400 your-key.pem (Linux/macOS only)
