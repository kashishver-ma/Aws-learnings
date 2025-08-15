## 3 tier-architecture

# Calculator Web App - 3-Tier Cloud Architecture

## Project Overview

This project is a **Calculator Web Application** hosted on AWS using a **3-tier architecture**:

- **Frontend:** Static HTML/CSS/JS hosted on **AWS S3**
- **Backend:** Flask/Spring Boot API hosted on **AWS EC2**
- **Database:** MySQL/PostgreSQL hosted on **AWS RDS**

The system allows users to input two numbers and select an operation; the backend computes the result and stores it in the database.

---

## Architecture Diagram

```
[User Browser] --> (HTTP) --> [S3 Frontend]
                                    |
                                    | AJAX POST /calculate
                                    v
                            [EC2 Backend] --> (SQL Query) --> [RDS Database]
                                    |
                                    | Response
                                    v
                            [User Browser]
```

- **Frontend:** Publicly accessible via S3 static website endpoint.
- **Backend:** Accessible only to frontend; EC2 security group controls traffic.
- **Database:** Private, accessible only from EC2; stores calculation history.

---

## Setup Instructions

### 1. Local Development

**Frontend:**

- Develop HTML/CSS/JS locally.
- Test with `index.html`.
- AJAX calls should point to local backend:

```javascript
fetch("http://localhost:5000/calculate", {...})
```

**Backend:**

- Develop Flask/Spring Boot API locally.
- Test endpoints with Postman.
- Connect to local database for testing.

**Database:**

- Create calculations table: `num1`, `num2`, `operation`, `result`, `timestamp`.

### 2. AWS Deployment

#### Frontend on S3

1. Create S3 bucket: `calc-frontend`.
2. Enable Static Website Hosting → set `index.html` as entry point.
3. Upload all frontend files.
4. Apply bucket policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadAccess",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::calc-frontend/*"
    }
  ]
}
```

5. Disable Block Public Access.
6. Access via S3 static website endpoint:
   ```
   http://calc-frontend.s3-website.<region>.amazonaws.com
   ```

#### Backend on EC2

1. Launch EC2 instance with your preferred OS.
2. Configure Security Group Inbound Rules:

| Protocol | Port      | Source                      |
| -------- | --------- | --------------------------- |
| HTTP     | 80        | 0.0.0.0/0                   |
| TCP      | 5000/8080 | S3 or public IP for testing |
| SSH      | 22        | Your IP                     |

3. SSH into EC2 → install dependencies → deploy backend code.
4. Ensure backend listens on `0.0.0.0`.
5. Update backend to connect to RDS database.

#### Database on RDS

1. Launch RDS instance (MySQL/PostgreSQL).
2. Security Group Inbound Rule:

| Protocol | Port | Source             |
| -------- | ---- | ------------------ |
| MySQL    | 3306 | EC2 Security Group |

3. Update backend with RDS endpoint, username, password.

⚠️ **Do not make RDS public; use EC2 as a secure access point.**

### 3. Connecting Frontend → Backend → RDS

1. User loads frontend from S3.
2. Frontend sends AJAX POST request to EC2 backend.
3. Backend validates request, computes result.
4. Backend stores result in RDS.
5. Backend responds → frontend displays result.

---

## Common Errors & Fixes

| Error                           | Cause                                   | Solution                                                 |
| ------------------------------- | --------------------------------------- | -------------------------------------------------------- |
| 403 Forbidden                   | S3 not public or Block Public Access ON | Apply correct bucket policy, disable Block Public Access |
| Invalid Resource                | Wrong ARN in bucket policy              | Use `"arn:aws:s3:::calc-frontend/*"`                     |
| CORS errors                     | AJAX request from different origin      | Enable CORS in backend (`CORS(app, origins=["S3 URL"])`) |
| Backend unreachable             | EC2 SG blocked port                     | Open required ports (5000/8080) in SG                    |
| DB connection failed            | RDS SG blocked EC2                      | Allow EC2 SG in RDS inbound, use correct endpoint        |
| Workbench cannot connect to RDS | RDS private, no public access           | Use SSH tunnel via EC2 or backend API                    |

---

## Security Best Practices

- **S3 Frontend:** Public read only; use CloudFront + HTTPS for production.
- **EC2 Backend:** Restrict inbound ports; keep OS & software updated; enable HTTPS.
- **RDS Database:** Private subnet; inbound only from EC2; strong credentials & SSL.
- **IAM:** Minimal privileges; enable CloudTrail for logging.

---

## Testing & Verification

1. Open S3 static website endpoint → frontend loads.
2. Perform calculations → results stored in RDS via backend.
3. Monitor CloudWatch logs for errors.
4. Verify EC2 Security Group and RDS Security Group restrict access properly.

---

## Optional Enhancements

- Add CloudFront for CDN + HTTPS.
- Enable CloudWatch alarms for backend or database monitoring.
- Use Lambda functions for backend scaling (optional).

---

## ✅ Result

- Publicly accessible frontend on S3.
- Secure backend on EC2.
- Private, secure RDS database.
- Fully functional 3-tier architecture web app on AWS.
