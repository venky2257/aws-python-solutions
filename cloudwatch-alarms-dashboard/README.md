# CloudWatch Alarms and Dashboard for Lambda Monitoring

This module helps you set up CloudWatch Alarms and a Dashboard to monitor Lambda invocations using two key scenarios.

---

## ✅ Use Cases

### 1. **Dedicated Lambda Function Monitoring**
**Condition:** The Lambda function is expected to be invoked at least once every hour.
- **Metric:** `Invocations`
- **Alarm Logic:**
  - Period: 3600 seconds (1 hour)
  - Threshold: `Sum < 1`
  - Treat missing data as: `breaching`

### 2. **Generic Lambda Handling Multiple Jobs**
**Condition:** The Lambda logs must show the presence of a `jobType:<job>` entry at least once every hour.
- **Metric Source:** CloudWatch Logs Insight Query
- **Alarm Logic:**
  - Use a `metric filter` or `Logs Insight` scheduled query
  - Trigger if job-specific pattern not detected

---

## 📊 Dashboard
A CloudWatch Dashboard showing:
- Lambda Invocation count (per hour)
- Error count
- Log presence for each jobType (optional, if applicable)

---

## 🛠 Folder Structure
```bash
cloudwatch-alarms-dashboard/
├── alarms-lambda-invocations.yaml     # CFN template for basic Lambda alarm
├── alarms-log-query-jobtype.yaml      # CFN template using Logs Insight metric
├── dashboard.json                     # Sample CloudWatch dashboard definition
└── README.md
```

---

## 🚀 Automation with CloudFormation
- Use the included `alarms-lambda-invocations.yaml` to deploy invocation alarms
- Use `alarms-log-query-jobtype.yaml` to track job-specific log activity
- Deploy `dashboard.json` manually or via CLI:

```bash
aws cloudwatch put-dashboard \
  --dashboard-name LambdaMonitoring \
  --dashboard-body file://dashboard.json
```

---

## 🔐 IAM Requirements

The Lambda role should have permissions to emit custom metrics if used.
The CloudFormation stack role needs permissions to:
- `cloudwatch:PutMetricAlarm`
- `cloudwatch:PutDashboard`
- `logs:DescribeLogGroups`
- `logs:StartQuery`
- `logs:GetQueryResults`

---

## 📄 alarms-lambda-invocations.yaml (Scenario 1)
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: Alarm for a Lambda function not invoked in the last hour

Parameters:
  LambdaFunctionName:
    Type: String
    Description: Name of the Lambda function to monitor

Resources:
  LambdaInvocationAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub "Lambda-NoInvocation-${LambdaFunctionName}"
      Namespace: AWS/Lambda
      MetricName: Invocations
      Dimensions:
        - Name: FunctionName
          Value: !Ref LambdaFunctionName
      Statistic: Sum
      Period: 3600
      EvaluationPeriods: 1
      Threshold: 1
      ComparisonOperator: LessThanThreshold
      TreatMissingData: breaching
      AlarmDescription: !Sub "Triggers if ${LambdaFunctionName} is not invoked within 1 hour."
      ActionsEnabled: true
```