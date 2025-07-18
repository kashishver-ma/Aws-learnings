# Task 3: Create IAM User and Role

## Objective

Understand AWS Identity and Access Management (IAM) basics by creating users and roles, assigning permissions, and verifying access.

---

## Steps

### 1. Create an IAM User

- **Navigate to IAM Console:**  
   Go to the [AWS IAM Console](https://console.aws.amazon.com/iam/).
- **Create User:**
  - Click **Users** > **Add users**.
  - Enter a username (e.g., `aws-learner`).
  - Select **Programmatic access**.
- **Set Permissions:**
  - Attach existing policies directly.
  - Choose `AmazonS3ReadOnlyAccess` for basic S3 read permissions.
- **Review and Create:**
  - Review settings and create the user.
  - Download or copy the access key and secret key.

---

### 2. Create an IAM Role for EC2

- **Navigate to Roles:**  
   In the IAM Console, click **Roles** > **Create role**.
- **Select Trusted Entity:**
  - Choose **AWS service**.
  - Select **EC2**.
- **Attach Permissions:**
  - Attach `AmazonS3ReadOnlyAccess` or a custom policy.
- **Name and Create Role:**
  - Give the role a name (e.g., `EC2S3ReadOnlyRole`).
  - Create the role.

---

### 3. Launch EC2 Instance and Attach Role

- Go to the [EC2 Console](https://console.aws.amazon.com/ec2/).
- Launch a new EC2 instance.
- In the **Configure Instance** step, select the IAM role created above.
- Complete the launch process.

---

### 4. Verify Access Using AWS CLI

- SSH into the EC2 instance.
- Run the following command to list S3 buckets:
  ```sh
  aws s3 ls
  ```
- If configured correctly, you should see the list of accessible S3 buckets.

---

## GitHub Documentation

- **Folder:** `beginner/03-iam-user-role`
- **Files:**
  - `README.md` — This guide
  - `policy.json` — Example IAM policy
  - `ec2-role-test.md` — Steps to test EC2 role permissions

---

## References

- [AWS IAM Documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)
- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/index.html)
- [AWS CLI Documentation](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html)

## # Login as IAM

aws configure --profile iam-user

# Login as Root

aws configure --profile root-account

# Use IAM

aws s3 ls --profile iam-user

# Use Root

aws ec2 describe-instances --profile root-account

# Check who's logged in

aws sts get-caller-identity --profile iam-user

# Set default to IAM

aws configure

# Remove IAM profile

aws configure set aws_access_key_id "" --profile iam-user
aws configure set aws_secret_access_key "" --profile iam-user

# Fully logout all

del %USERPROFILE%\.aws\credentials
del %USERPROFILE%\.aws\config

| What You Want                      | Command                                          |
| ---------------------------------- | ------------------------------------------------ |
| 👤 Who am I currently logged in as | `aws sts get-caller-identity`                    |
| 🧾 What profiles do I have saved   | `cat %USERPROFILE%\.aws\credentials`             |
| 🔍 Check a specific profile's user | `aws sts get-caller-identity --profile iam-user` |

## examples

aws iam create-user --user-name iam-sample
{
"User": {
"Path": "/",
"UserName": "iam-sample",
"UserId": "**\*\*\*\***",
"Arn": "arn:aws:iam::\*\*\*\*":user/iam-sample",
"CreateDate": "2025-07-18T16:57:40Z"
}
}

### add user and attach policy to it

aws iam attach-user-policy

--user-name iam-sample --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess

PS C:\Users\Dell\OneDrive\Desktop\aws> aws iam create-access-key --user-name iam-sample  
{
"AccessKey": {
"UserName": "iam-sample",
"AccessKeyId": "**\***",
"Status": "Active",
"SecretAccessKey": "\*\*\*\*++ntICo+q5XF8CiiR5kNN",
"CreateDate": "2025-07-18T17:02:17Z"
}

}

### 🔹 Step 2: Create IAM Role for EC2 with Same Permissions

Create Trust Policy file:
Save this as trust-policy.json:

json
{
"Version": "2012-10-17",
"Statement": [
{
"Effect": "Allow",
"Principal": {
"Service": "ec2.amazonaws.com"
},
"Action": "sts:AssumeRole"
}
]
}

### Create Role:

aws iam create-role \
 --role-name EC2S3ReadOnlyRole \
 --assume-role-policy-document file://trust-policy.json

Attach S3 ReadOnlyAccess to Role:

aws iam attach-role-policy \
 --role-name EC2S3ReadOnlyRole \
 --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess

### 🔹 Step 3: Create Instance Profile and Add Role

aws iam create-instance-profile \
 --instance-profile-name EC2S3ReadOnlyProfile

aws iam add-role-to-instance-profile \
 --instance-profile-name EC2S3ReadOnlyProfile \
 --role-name EC2S3ReadOnlyRole

### 🔹 Step 4: Launch EC2 Instance and Attach Role

aws ec2 run-instances \
 --image-id ami-xxxxxxxxxxxxxxx \ # use valid Amazon Linux AMI ID
--count 1 \
 --instance-type t2.micro \
 --key-name your-key-name \
 --subnet-id subnet-xxxxxxxxxxxxx \
 --security-group-ids sg-xxxxxxxxxxxx \
 --iam-instance-profile Name=EC2S3ReadOnlyProfile \
 --region your-region

### 🔹 Step 5: Verify Access Inside EC2

SSH into EC2:

ssh -i your-key.pem ec2-user@<public-ip>

Check IAM Role is Attached:

curl http://169.254.169.254/latest/meta-data/iam/info

Confirm S3 Read Access:

aws s3 ls
If everything is configured correctly, it will list S3 buckets 🎉
