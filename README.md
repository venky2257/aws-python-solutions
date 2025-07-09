# AWS + Python Solutions Archive

This repository is a personal archive of practical AWS and Python-based solutions. It is designed to:

- 🛠️ Simplify development and deployment on AWS
- 🧠 Preserve reusable knowledge for future reference
- 🔁 Enable scalable and reusable cloud patterns

---

## 📁 Folder Overview

### 1. `lambda-containerization/`
Containerizing AWS Lambda functions to remove dependency on Lambda layers. This allows full control over the runtime environment, dependency packaging, and consistent deployment across Python versions.

### 2. `cloudwatch-alarms-dashboard/`
Scripts and configurations to create CloudWatch alarms and dashboards using Python or CloudFormation.

### 3. `s3-trigger-lambda/`
Sample code and automation to trigger Lambda functions on S3 events (e.g., file uploads), and handle data processing like validation, transformation, and file relocation.

### 4. `automation/`
Reusable automation scripts to:
- Build and push Docker images to ECR
- Tag and version Lambda containers
- Handle multi-environment workflows

---

## ✅ Prerequisites
- AWS CLI configured with profiles (e.g., `aws configure --profile <profile_name>`)
- Docker installed (Windows/Mac/Linux)
- Python 3.8+

---

## 📌 How to Use
Each folder contains:
- A self-contained use case
- Required source files (code, Dockerfile, infra scripts)
- Step-by-step instructions in `README.md`

---

## 📬 Contributions & Updates
This is a growing toolkit — more modules will be added over time.

Feel free to fork or adapt for your own learning or team onboarding.

---

## 👤 Maintained by
**Venkatesh Venky**

---

Let’s dive in → start with [`lambda-containerization`](./lambda-containerization/README.md)
