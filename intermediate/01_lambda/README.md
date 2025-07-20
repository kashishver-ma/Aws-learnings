# Serverless Email System - Complete Project Guide

## ✅ Project Goal

**Build a simple serverless system that sends emails using AWS SES via API Gateway and Lambda, testable through Postman or a frontend.**

## 🔧 Full Step-by-Step Breakdown

### ✅ Step 1: Create a Lambda Function (Python) to Send Email

**What you did:**

- Created an AWS Lambda function in Python
- Wrote code to send emails using **Amazon SES** (Simple Email Service)
- Installed and used `boto3` (AWS SDK for Python)

**How it works:**

- Lambda receives a JSON input (like `{ "subject": "Hi", "message": "Hello" }`)
- It formats that into an email
- It sends the email using your verified SES sender

**Status:** ✅ Tested successfully from Lambda console

### ✅ Step 2: Verify Email in SES Sandbox

**What you did:**

- Verified your sender and receiver emails inside SES (sandbox mode only allows verified addresses)

**Why this matters:**

- In **sandbox mode**, SES only sends to **verified** email addresses
- This is a security step to avoid spam abuse

### ✅ Step 3: Test Lambda with Sample Payload

**What you did:**

- Created a test event in Lambda console with:

```json
{
  "body": "{\"subject\": \"Test\", \"message\": \"Hello from Lambda!\"}"
}
```

**What happened:**

- Lambda successfully parsed the input, called SES, and you received an email

### ✅ Step 4: Create an API Gateway to Expose Lambda

**What you did:**

- Created a new **HTTP API** using API Gateway
- Connected it to your Lambda function
- Defined route `POST /send-email`
- Deployed it and got an **Invoke URL** like:

```bash
https://abc123.execute-api.region.amazonaws.com/send-email
```

**Why this matters:**

- This gives you a **public HTTP endpoint** to call your Lambda function
- Now anyone (Postman, website, frontend app) can trigger the email flow

### ✅ Step 5: Test API Using Postman

**What you did:**

- Made a `POST` request in Postman with JSON body:

```json
{
  "subject": "From Postman",
  "message": "This email was sent using API Gateway + Lambda + SES!"
}
```

**What happened:**

- Postman → API Gateway → Lambda → SES → Email Delivered ✅

## ✅ System Summary Diagram

# with ses

Lambda ← (Tested Directly)
|
└── Sends Email via SES

```
[Postman / Frontend]
        ↓ (POST JSON)
    API Gateway (HTTP API)
        ↓
    AWS Lambda (Python)
        ↓
    Amazon SES (Verified Email)
        ↓
    Your Inbox 📬
```

## 🔍 Summary: What You've Built

| Component       | Role                                                         |
| --------------- | ------------------------------------------------------------ |
| **SES**         | Sends the actual email. You verified emails in sandbox mode. |
| **Lambda**      | Receives input and calls SES using Python (`boto3`).         |
| **API Gateway** | Gives a public URL to call Lambda using HTTP POST.           |
| **Postman**     | Used to test the public API with real data.                  |

## 🎯 Key Benefits of This Architecture

- **Serverless**: No servers to manage, pay only for usage
- **Scalable**: Automatically handles traffic spikes
- **Secure**: AWS IAM controls access to SES
- **Simple**: Clean API interface for frontend integration
- **Cost-effective**: Very cheap for low to moderate email volumes

## 🚀 Next Steps (Optional Enhancements)

1. **Move out of SES Sandbox** - Request production access to send to any email
2. **Add Email Templates** - Create reusable HTML email templates
3. **Add Error Handling** - Better error responses and logging
4. **Frontend Integration** - Build a simple web form
5. **Rate Limiting** - Add throttling to prevent abuse
6. **Email Validation** - Validate email formats before sending

## 📋 Testing Checklist

- [x] Lambda function created and configured
- [x] SES email addresses verified
- [x] Lambda tested with sample payload
- [x] API Gateway created and deployed
- [x] End-to-end test via Postman successful
- [x] Email received in inbox

**Project Status: Complete and Functional! 🎉**

# Serverless Email System - Complete Project Guide

## ✅ Project Goal

**Build a simple serverless system that sends emails using AWS SES via API Gateway and Lambda, testable through Postman or a frontend.**

## 🔧 Full Step-by-Step Breakdown

### ✅ Step 1: Create a Lambda Function (Python) to Send Email

**What you did:**

- Created an AWS Lambda function in Python
- Wrote code to send emails using **Amazon SES** (Simple Email Service)
- Installed and used `boto3` (AWS SDK for Python)

**How it works:**

- Lambda receives a JSON input (like `{ "subject": "Hi", "message": "Hello" }`)
- It formats that into an email
- It sends the email using your verified SES sender

**Status:** ✅ Tested successfully from Lambda console

### ✅ Step 2: Verify Email in SES Sandbox

**What you did:**

- Verified your sender and receiver emails inside SES (sandbox mode only allows verified addresses)

**Why this matters:**

- In **sandbox mode**, SES only sends to **verified** email addresses
- This is a security step to avoid spam abuse

### ✅ Step 3: Test Lambda with Sample Payload

**What you did:**

- Created a test event in Lambda console with:

```json
{
  "body": "{\"subject\": \"Test\", \"message\": \"Hello from Lambda!\"}"
}
```

**What happened:**

- Lambda successfully parsed the input, called SES, and you received an email

### ✅ Step 4: Create an API Gateway to Expose Lambda

**What you did:**

- Created a new **HTTP API** using API Gateway
- Connected it to your Lambda function
- Defined route `POST /send-email`
- Deployed it and got an **Invoke URL** like:

```bash
https://abc123.execute-api.region.amazonaws.com/send-email
```

**Why this matters:**

- This gives you a **public HTTP endpoint** to call your Lambda function
- Now anyone (Postman, website, frontend app) can trigger the email flow

### ✅ Step 5: Test API Using Postman

**What you did:**

- Made a `POST` request in Postman with JSON body:

```json
{
  "subject": "From Postman",
  "message": "This email was sent using API Gateway + Lambda + SES!"
}
```

**What happened:**

- Postman → API Gateway → Lambda → SES → Email Delivered ✅

## ✅ System Summary Diagram

```
[Postman / Frontend]
        ↓ (POST JSON)
    API Gateway (HTTP API)
        ↓
    AWS Lambda (Python)
        ↓
    Amazon SES (Verified Email)
        ↓
    Your Inbox 📬
```

## 🔍 Summary: What You've Built

| Component       | Role                                                         |
| --------------- | ------------------------------------------------------------ |
| **SES**         | Sends the actual email. You verified emails in sandbox mode. |
| **Lambda**      | Receives input and calls SES using Python (`boto3`).         |
| **API Gateway** | Gives a public URL to call Lambda using HTTP POST.           |
| **Postman**     | Used to test the public API with real data.                  |

## 🎯 Key Benefits of This Architecture

- **Serverless**: No servers to manage, pay only for usage
- **Scalable**: Automatically handles traffic spikes
- **Secure**: AWS IAM controls access to SES
- **Simple**: Clean API interface for frontend integration
- **Cost-effective**: Very cheap for low to moderate email volumes

## 🚀 Next Steps (Optional Enhancements)

1. **Move out of SES Sandbox** - Request production access to send to any email
2. **Add Email Templates** - Create reusable HTML email templates
3. **Add Error Handling** - Better error responses and logging
4. **Frontend Integration** - Build a simple web form
5. **Rate Limiting** - Add throttling to prevent abuse
6. **Email Validation** - Validate email formats before sending

## 📋 Testing Checklist

- [x] Lambda function created and configured
- [x] SES email addresses verified
- [x] Lambda tested with sample payload
- [x] API Gateway created and deployed
- [x] End-to-end test via Postman successful
- [x] Email received in inbox

**Project Status: Complete and Functional! 🎉**

## 🧠 What You Learned

### ✅ Core Components & Flow:

| Component           | Purpose                                                                |
| ------------------- | ---------------------------------------------------------------------- |
| **Lambda (Python)** | Executes your email logic (subject/message → SES)                      |
| **Amazon SES**      | Sends the actual email (works only with verified addresses in sandbox) |
| **API Gateway**     | Creates a public-facing endpoint to invoke your Lambda                 |
| **CloudWatch Logs** | Helps debug Lambda executions                                          |
| **Postman / HTML**  | Tests API functionality via POST requests                              |

### 🔧 Key Concepts Used:

- Creating Lambda functions
- Using `boto3` to send SES email
- Parsing JSON body from API Gateway
- Debugging using CloudWatch
- Deploying and linking Lambda to API Gateway
- Sending test emails using verified SES email

## 🪲 Problems You Faced (and Solved!)

| 🧩 Issue                                     | 💡 Solution                                                                                                                                                                                                             |
| -------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ❌ `KeyError: 'body'` in Lambda              | Because the **test event in Lambda console** didn't include the `body` key. ✅ Fixed by testing **via API Gateway** (Postman).                                                                                          |
| ❌ "Domain is not valid" in SES              | You tried to verify an **email ID as a domain** (like `itskashishverma@gmail.com`) — SES needs either: a domain (like `example.com`) **or** verify the **email address**. ✅ You verified the email instead.            |
| ❌ Couldn't find API URL                     | You were looking for the URL immediately after API creation. ✅ Fixed by adding **route**, deploying stage, then getting the **full invoke URL**: `https://{api_id}.execute-api.{region}.amazonaws.com/{stage}/{route}` |
| ❌ Email response came, but logs not visible | Because you had **no print/log statements** in Lambda. ✅ Solved by adding `print()` to trace execution.                                                                                                                |
| ❌ Unsure if Lambda was triggered via API    | ✅ Confirmed by checking **latest CloudWatch logs** and verifying logs matched Postman hit time.                                                                                                                        |
| ❌ Unsure if SES was working in sandbox      | ✅ Confirmed by using **same sender and receiver email**, which was verified.                                                                                                                                           |

## 📦 Final Working Setup

**Lambda Function:**

- Receives JSON body → `subject`, `message`
- Uses `boto3` to send email via SES
- Returns success JSON

**API Gateway:**

- POST endpoint setup
- Integrated with Lambda
- Used by Postman (or HTML form)

**SES:**

- In sandbox
- Verified sender & receiver
- Able to send emails

**CloudWatch:**

- Logs Lambda executions and errors
- Used for full trace/debugging

## 🛠️ Optional Next Steps (Based on What You Built)

| Feature                       | Why You Might Add It                                      |
| ----------------------------- | --------------------------------------------------------- |
| 🧾 **HTML email support**     | For styled email messages                                 |
| 🌍 **Frontend form**          | Public user contact submission                            |
| 🔑 **API Key or Auth**        | To secure the endpoint                                    |
| 🔓 **Move SES to Production** | To send emails to **anyone**, not just verified addresses |
| 🧹 **Input validation**       | To block spam / empty requests                            |
| 📬 **Email template engine**  | Dynamic email formatting                                  |

# Serverless Email System - Complete Project Guide

## ✅ Project Goal

**Build a simple serverless system that sends emails using AWS SES via API Gateway and Lambda, testable through Postman or a frontend.**

## 🔧 Full Step-by-Step Breakdown

### ✅ Step 1: Create a Lambda Function (Python) to Send Email

**What you did:**

- Created an AWS Lambda function in Python
- Wrote code to send emails using **Amazon SES** (Simple Email Service)
- Installed and used `boto3` (AWS SDK for Python)

**How it works:**

- Lambda receives a JSON input (like `{ "subject": "Hi", "message": "Hello" }`)
- It formats that into an email
- It sends the email using your verified SES sender

**Status:** ✅ Tested successfully from Lambda console

### ✅ Step 2: Verify Email in SES Sandbox

**What you did:**

- Verified your sender and receiver emails inside SES (sandbox mode only allows verified addresses)

**Why this matters:**

- In **sandbox mode**, SES only sends to **verified** email addresses
- This is a security step to avoid spam abuse

### ✅ Step 3: Test Lambda with Sample Payload

**What you did:**

- Created a test event in Lambda console with:

```json
{
  "body": "{\"subject\": \"Test\", \"message\": \"Hello from Lambda!\"}"
}
```

**What happened:**

- Lambda successfully parsed the input, called SES, and you received an email

### ✅ Step 4: Create an API Gateway to Expose Lambda

**What you did:**

- Created a new **HTTP API** using API Gateway
- Connected it to your Lambda function
- Defined route `POST /send-email`
- Deployed it and got an **Invoke URL** like:

```bash
https://abc123.execute-api.region.amazonaws.com/send-email
```

**Why this matters:**

- This gives you a **public HTTP endpoint** to call your Lambda function
- Now anyone (Postman, website, frontend app) can trigger the email flow

### ✅ Step 5: Test API Using Postman

**What you did:**

- Made a `POST` request in Postman with JSON body:

```json
{
  "subject": "From Postman",
  "message": "This email was sent using API Gateway + Lambda + SES!"
}
```

**What happened:**

- Postman → API Gateway → Lambda → SES → Email Delivered ✅

## ✅ System Summary Diagram

```
[Postman / Frontend]
        ↓ (POST JSON)
    API Gateway (HTTP API)
        ↓
    AWS Lambda (Python)
        ↓
    Amazon SES (Verified Email)
        ↓
    Your Inbox 📬
```

## 🔍 Summary: What You've Built

| Component       | Role                                                         |
| --------------- | ------------------------------------------------------------ |
| **SES**         | Sends the actual email. You verified emails in sandbox mode. |
| **Lambda**      | Receives input and calls SES using Python (`boto3`).         |
| **API Gateway** | Gives a public URL to call Lambda using HTTP POST.           |
| **Postman**     | Used to test the public API with real data.                  |

## 🎯 Key Benefits of This Architecture

- **Serverless**: No servers to manage, pay only for usage
- **Scalable**: Automatically handles traffic spikes
- **Secure**: AWS IAM controls access to SES
- **Simple**: Clean API interface for frontend integration
- **Cost-effective**: Very cheap for low to moderate email volumes

## 🚀 Next Steps (Optional Enhancements)

1. **Move out of SES Sandbox** - Request production access to send to any email
2. **Add Email Templates** - Create reusable HTML email templates
3. **Add Error Handling** - Better error responses and logging
4. **Frontend Integration** - Build a simple web form
5. **Rate Limiting** - Add throttling to prevent abuse
6. **Email Validation** - Validate email formats before sending

## 📋 Testing Checklist

- [x] Lambda function created and configured
- [x] SES email addresses verified
- [x] Lambda tested with sample payload
- [x] API Gateway created and deployed
- [x] End-to-end test via Postman successful
- [x] Email received in inbox

**Project Status: Complete and Functional! 🎉**

## 🧠 What You Learned

### ✅ Core Components & Flow:

| Component           | Purpose                                                                |
| ------------------- | ---------------------------------------------------------------------- |
| **Lambda (Python)** | Executes your email logic (subject/message → SES)                      |
| **Amazon SES**      | Sends the actual email (works only with verified addresses in sandbox) |
| **API Gateway**     | Creates a public-facing endpoint to invoke your Lambda                 |
| **CloudWatch Logs** | Helps debug Lambda executions                                          |
| **Postman / HTML**  | Tests API functionality via POST requests                              |

### 🔧 Key Concepts Used:

- Creating Lambda functions
- Using `boto3` to send SES email
- Parsing JSON body from API Gateway
- Debugging using CloudWatch
- Deploying and linking Lambda to API Gateway
- Sending test emails using verified SES email

## 🪲 Problems You Faced (and Solved!)

| 🧩 Issue                                     | 💡 Solution                                                                                                                                                                                                             |
| -------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ❌ `KeyError: 'body'` in Lambda              | Because the **test event in Lambda console** didn't include the `body` key. ✅ Fixed by testing **via API Gateway** (Postman).                                                                                          |
| ❌ "Domain is not valid" in SES              | You tried to verify an **email ID as a domain** (like `itskashishverma@gmail.com`) — SES needs either: a domain (like `example.com`) **or** verify the **email address**. ✅ You verified the email instead.            |
| ❌ Couldn't find API URL                     | You were looking for the URL immediately after API creation. ✅ Fixed by adding **route**, deploying stage, then getting the **full invoke URL**: `https://{api_id}.execute-api.{region}.amazonaws.com/{stage}/{route}` |
| ❌ Email response came, but logs not visible | Because you had **no print/log statements** in Lambda. ✅ Solved by adding `print()` to trace execution.                                                                                                                |
| ❌ Unsure if Lambda was triggered via API    | ✅ Confirmed by checking **latest CloudWatch logs** and verifying logs matched Postman hit time.                                                                                                                        |
| ❌ Unsure if SES was working in sandbox      | ✅ Confirmed by using **same sender and receiver email**, which was verified.                                                                                                                                           |

## 📦 Final Working Setup

**Lambda Function:**

- Receives JSON body → `subject`, `message`
- Uses `boto3` to send email via SES
- Returns success JSON

**API Gateway:**

- POST endpoint setup
- Integrated with Lambda
- Used by Postman (or HTML form)

**SES:**

- In sandbox
- Verified sender & receiver
- Able to send emails

**CloudWatch:**

- Logs Lambda executions and errors
- Used for full trace/debugging

## 🛠️ Optional Next Steps (Based on What You Built)

| Feature                       | Why You Might Add It                                      |
| ----------------------------- | --------------------------------------------------------- |
| 🧾 **HTML email support**     | For styled email messages                                 |
| 🌍 **Frontend form**          | Public user contact submission                            |
| 🔑 **API Key or Auth**        | To secure the endpoint                                    |
| 🔓 **Move SES to Production** | To send emails to **anyone**, not just verified addresses |
| 🧹 **Input validation**       | To block spam / empty requests                            |
| 📬 **Email template engine**  | Dynamic email formatting                                  |

## 🧹 Clean-Up Steps (Recommended)

### ✅ What to Delete

| Resource                          | 🔍 Why                                                                                      |
| --------------------------------- | ------------------------------------------------------------------------------------------- |
| **API Gateway**                   | You're billed per million requests/month (tiny usage = free, but best to remove if unused). |
| **Lambda Function**               | No cost when idle, but it's good hygiene to delete unused ones.                             |
| **CloudWatch Logs**               | Logs can accumulate and eventually cost ₹ (not much, but can grow).                         |
| **SES Verified Emails / Domains** | Not charged, but optional to clear.                                                         |
| **IAM Role for Lambda**           | If created specifically for this use case, delete if unused elsewhere.                      |

### 📍 Where to Find and Delete

1. **Delete API Gateway**

   - Go to **API Gateway**
   - Select your `contactAPI`
   - Choose **"Actions" → Delete**

2. **Delete Lambda Function**

   - Go to **AWS Lambda**
   - Select your email function
   - Click **"Actions" → Delete function**

3. **Delete CloudWatch Log Groups (Optional but Clean)**

   - Go to **CloudWatch → Log groups**
   - Find logs with `/aws/lambda/your-function-name`
   - Click **"Actions" → Delete log group**

4. **Delete SES Resources (Optional)**

   - Go to **SES Console**
   - Delete any **verified email addresses**
   - If domain verified (unlikely), delete it too

5. **Delete IAM Role (Only if Unused Elsewhere)**
   - Go to **IAM → Roles**
   - Look for roles like `lambda_basic_execution` or similar you created
   - Delete if it's not tied to any other Lambda

### 💸 About Costs

| Service             | Cost                                                          |
| ------------------- | ------------------------------------------------------------- |
| **Lambda**          | First 1 million requests/month = **Free**                     |
| **SES**             | Free to send 200 emails/day from EC2 or Lambda in **sandbox** |
| **API Gateway**     | Free up to 1M requests/month                                  |
| **CloudWatch Logs** | Small cost after 5GB/month                                    |
