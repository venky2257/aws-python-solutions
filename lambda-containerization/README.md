# Lambda Containerization

This module demonstrates how to package and deploy an AWS Lambda function using Docker containers instead of Lambda layers.

## ✅ Why Use Containers?
- Avoid repeated layer maintenance during Python version upgrades
- Bundle all dependencies directly with code
- Greater control over runtime and packages

---

## 📁 Files

```bash
lambda-containerization/
├── app.py             # Lambda handler function
├── Dockerfile         # Defines the container runtime environment
├── requirements.txt   # Python dependencies
└── README.md          # This file
```

---

## 🧪 Use Case
A simple Lambda function that:
- Triggers on an S3 file upload
- Reads the JSON file
- Validates the format
- Renames and copies it to another prefix using an epoch timestamp

Also demonstrates use of a Python package (`python-dateutil`) from `requirements.txt`

---

## 🚀 Deployment Steps

### 1. Build the Docker Image
```bash
docker build -t ceo-diag-test-json-lambda .
```

### 2. Tag the Image (e.g., `v1`, folder name, or commit hash)
```bash
docker tag ceo-diag-test-json-lambda:latest <account-id>.dkr.ecr.<region>.amazonaws.com/<repository-name>:v1
```

### 3. Login to ECR
```bash
aws ecr get-login-password --region <region> --profile <aws-profile> | docker login --username AWS --password-stdin <account-id>.dkr.ecr.<region>.amazonaws.com
```

### 4. Push to ECR
```bash
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/<repository-name>:v1
```

### 5. Create Lambda from AWS Console
- Go to **Lambda > Create function**
- Select **Container image** as deployment method
- Use the full image URI from ECR (step 4)
- Choose or create an **Execution Role** with ECR read permissions:
  - `ecr:GetDownloadUrlForLayer`
  - `ecr:BatchGetImage`
  - `ecr:GetAuthorizationToken`
  - `ecr:BatchCheckLayerAvailability`

---

## 🔐 Required IAM Policies

### 🔸 Lambda Execution Role
This role is used *by Lambda to pull container images from ECR*:

```json
{
  "Effect": "Allow",
  "Action": [
    "ecr:GetDownloadUrlForLayer",
    "ecr:BatchGetImage",
    "ecr:GetAuthorizationToken",
    "ecr:BatchCheckLayerAvailability"
  ],
  "Resource": "arn:aws:ecr:<region>:<account-id>:repository/ceo-diag-test-*"
}
```

Also, if the Lambda function interacts with S3:

```json
{
  "Effect": "Allow",
  "Action": [
    "s3:GetObject",
    "s3:PutObject"
  ],
  "Resource": [
    "arn:aws:s3:::ceo-diag-test-*/incoming/*",
    "arn:aws:s3:::ceo-diag-test-*/validated/*"
  ]
}
```

### 🔸 Developer/Admin Role (to push to ECR)
The IAM user/role who runs `docker push` must have:

```json
{
  "Effect": "Allow",
  "Action": [
    "ecr:GetAuthorizationToken",
    "ecr:BatchCheckLayerAvailability",
    "ecr:CompleteLayerUpload",
    "ecr:InitiateLayerUpload",
    "ecr:PutImage",
    "ecr:UploadLayerPart"
  ],
  "Resource": "arn:aws:ecr:<region>:<account-id>:repository/ceo-diag-test-*"
}
```

---

## 📌 Notes
- Works even if your local Python version differs (container isolates it)
- The image used: `public.ecr.aws/lambda/python:3.12`
- Example trigger: S3 file upload → Lambda processes → stores result with epoch timestamp

---
