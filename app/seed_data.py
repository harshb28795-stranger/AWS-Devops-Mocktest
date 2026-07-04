"""
Seed data for the AWS DevOps Professional Mock Test Lab.

This module inserts the six quiz categories and 30 original practice
questions the first time the application starts. If data already
exists, seeding is skipped so restarting the app never creates
duplicate rows.
"""

from app import db
from app.models import Category, Question

# ---------------------------------------------------------------------------
# Categories
# ---------------------------------------------------------------------------
CATEGORIES = [
    {
        "name": "SDLC Automation",
        "description": "CI/CD pipelines, build automation, and deployment strategies.",
    },
    {
        "name": "Configuration Management",
        "description": "Infrastructure as code, fleet management, and environment consistency.",
    },
    {
        "name": "Monitoring & Logging",
        "description": "Observability, metrics, alarms, and centralized logging.",
    },
    {
        "name": "Incident & Event Response",
        "description": "Automated remediation, event-driven operations, and troubleshooting.",
    },
    {
        "name": "High Availability",
        "description": "Fault tolerance, scalability, and disaster recovery design.",
    },
    {
        "name": "Security & Compliance",
        "description": "Identity, encryption, auditing, and governance controls.",
    },
]

# ---------------------------------------------------------------------------
# Questions
# Each dict maps to one Question row. "category" refers to the Category name
# above so we can look up the correct category_id at seed time.
# ---------------------------------------------------------------------------
QUESTIONS = [
    # ---------------------- SDLC Automation (5) ----------------------
    {
        "category": "SDLC Automation",
        "question_text": (
            "A team wants CodePipeline to automatically roll back a deployment "
            "if newly deployed code causes an increase in HTTP 500 errors, "
            "without requiring a human to intervene. Which combination of "
            "services best achieves this?"
        ),
        "option_a": "CodeDeploy with a CloudWatch alarm configured for automatic rollback on alarm",
        "option_b": "CodeBuild with a manual approval action inserted before production",
        "option_c": "CodePipeline with an S3 event trigger that restarts the pipeline",
        "option_d": "CodeCommit branch protection rules combined with IAM policies",
        "correct_answer": "A",
        "explanation": (
            "CodeDeploy supports automatic rollback based on CloudWatch alarms. "
            "When an alarm tied to error-rate metrics enters ALARM state during "
            "or after a deployment, CodeDeploy stops the deployment and rolls "
            "back to the last known good revision automatically, requiring no "
            "manual action."
        ),
    },
    {
        "category": "SDLC Automation",
        "question_text": (
            "A DevOps engineer wants to deploy a new Lambda version gradually, "
            "shifting traffic from 10% to 100% over ten minutes, and to "
            "automatically abort the shift if a CloudWatch alarm triggers. "
            "Which CodeDeploy deployment configuration type supports this?"
        ),
        "option_a": "AllAtOnce",
        "option_b": "Canary or Linear deployment configuration for Lambda",
        "option_c": "Blue/Green deployment for EC2",
        "option_d": "In-place deployment for EC2",
        "correct_answer": "B",
        "explanation": (
            "CodeDeploy for Lambda supports Canary and Linear traffic-shifting "
            "configurations, which gradually move traffic to the new version "
            "over defined intervals and automatically roll back if a linked "
            "CloudWatch alarm fires."
        ),
    },
    {
        "category": "SDLC Automation",
        "question_text": (
            "Which CodeBuild feature allows build artifacts and dependencies "
            "from previous builds to be reused, significantly reducing build "
            "time for large projects?"
        ),
        "option_a": "Build badges",
        "option_b": "CodeBuild local caching or S3 caching",
        "option_c": "Source version overrides",
        "option_d": "Build environment compute type",
        "correct_answer": "B",
        "explanation": (
            "CodeBuild supports caching (local Docker layer cache, local "
            "source cache, or S3-based caching) so that dependencies such as "
            "npm or Maven packages don't need to be re-downloaded on every "
            "build, speeding up subsequent builds."
        ),
    },
    {
        "category": "SDLC Automation",
        "question_text": (
            "An organization runs a monorepo and wants CodePipeline to only "
            "trigger the microservice-specific pipeline stages when files "
            "under that microservice's directory change. What is the best "
            "approach?"
        ),
        "option_a": "Use one pipeline per repository only, monorepos are unsupported",
        "option_b": "Configure separate pipelines with CodeCommit trigger paths or CodeBuild path filters tied to each service folder",
        "option_c": "Always rebuild every microservice on any commit to keep it simple",
        "option_d": "Use CloudFormation StackSets to detect file changes",
        "correct_answer": "B",
        "explanation": (
            "Using path-based triggers (available through CodeCommit trigger "
            "configuration or custom Lambda-based Git diff checks in the "
            "pipeline) allows CodePipeline to only run stages relevant to the "
            "microservice folder that changed, avoiding unnecessary rebuilds "
            "in a monorepo."
        ),
    },
    {
        "category": "SDLC Automation",
        "question_text": (
            "A company wants to enforce that every CloudFormation change to "
            "production is reviewed before it modifies live resources. Which "
            "CloudFormation feature directly supports this workflow?"
        ),
        "option_a": "Stack policies",
        "option_b": "Change sets combined with a manual approval action in CodePipeline",
        "option_c": "Nested stacks",
        "option_d": "Drift detection",
        "correct_answer": "B",
        "explanation": (
            "A CloudFormation change set previews what will happen to "
            "resources before they are actually changed. Pairing this with a "
            "manual approval stage in CodePipeline lets a human review the "
            "change set output before the pipeline proceeds to execute it "
            "against production."
        ),
    },
    # ------------------- Configuration Management (5) -------------------
    {
        "category": "Configuration Management",
        "question_text": (
            "A DevOps team needs to ensure that 500 EC2 instances always have "
            "the latest security agent installed, and any instance found "
            "without it should be automatically remediated within minutes. "
            "Which AWS service combination fits best?"
        ),
        "option_a": "AWS Config rule with an automatic remediation action using Systems Manager Automation",
        "option_b": "CloudTrail with an S3 event notification",
        "option_c": "Manually SSH into each instance on a schedule",
        "option_d": "CloudFormation StackSets applied once per quarter",
        "correct_answer": "A",
        "explanation": (
            "AWS Config continuously evaluates resource configuration against "
            "rules. When paired with automatic remediation actions (backed by "
            "Systems Manager Automation documents), non-compliant instances "
            "can be corrected automatically and quickly, without waiting for "
            "a scheduled manual process."
        ),
    },
    {
        "category": "Configuration Management",
        "question_text": (
            "Which Systems Manager capability lets engineers group instances "
            "by tags and run the same shell script against all of them "
            "on demand, without needing SSH access or bastion hosts?"
        ),
        "option_a": "Systems Manager Run Command",
        "option_b": "Systems Manager Session Manager only",
        "option_c": "EC2 user data scripts",
        "option_d": "AWS OpsWorks Chef recipes",
        "correct_answer": "A",
        "explanation": (
            "Systems Manager Run Command executes commands or scripts across "
            "one or many managed instances (targeted by tags, resource "
            "groups, or instance IDs) without requiring SSH, bastion hosts, "
            "or opening inbound ports."
        ),
    },
    {
        "category": "Configuration Management",
        "question_text": (
            "A company uses OpsWorks for Chef Automate to manage its fleet. "
            "They want new instances to automatically converge to the "
            "desired configuration state at regular intervals, not just at "
            "launch. What accomplishes this in OpsWorks?"
        ),
        "option_a": "Chef Client periodic runs configured on the layer",
        "option_b": "A one-time setup recipe executed at instance boot only",
        "option_c": "CloudFormation UpdatePolicy",
        "option_d": "AWS Config conformance packs",
        "correct_answer": "A",
        "explanation": (
            "OpsWorks lets you configure the Chef Client to run periodically "
            "(in addition to lifecycle events like setup, configure, and "
            "deploy), ensuring the instance continuously converges to the "
            "desired state rather than being configured only once at launch."
        ),
    },
    {
        "category": "Configuration Management",
        "question_text": (
            "An engineer wants a single CloudFormation template to be "
            "deployed consistently across 15 AWS accounts and 3 regions, "
            "with centralized management of drift and updates. Which feature "
            "should be used?"
        ),
        "option_a": "CloudFormation nested stacks",
        "option_b": "CloudFormation StackSets",
        "option_c": "Separate manual deployments per account",
        "option_d": "AWS Config aggregators",
        "correct_answer": "B",
        "explanation": (
            "CloudFormation StackSets extend stacks to multiple accounts and "
            "regions with a single operation, allowing centralized creation, "
            "update, and deletion of stacks across an organization from one "
            "administrator account."
        ),
    },
    {
        "category": "Configuration Management",
        "question_text": (
            "Which approach best enforces that all newly launched EC2 "
            "instances in an account use an approved, hardened AMI, "
            "rejecting or flagging any instance launched from a non-approved "
            "image?"
        ),
        "option_a": "An AWS Config rule that checks the AMI ID against an approved list, with an SNS notification or automated termination for violations",
        "option_b": "Relying on developers to remember to pick the right AMI",
        "option_c": "EC2 instance metadata service configuration",
        "option_d": "A CloudFront origin access identity",
        "correct_answer": "A",
        "explanation": (
            "A custom or managed AWS Config rule can evaluate whether "
            "instances were launched from an approved AMI list. Non-compliant "
            "resources can trigger notifications or automated remediation "
            "(such as stopping or terminating the instance), enforcing "
            "governance without relying on manual processes."
        ),
    },
    # ------------------- Monitoring & Logging (5) -------------------
    {
        "category": "Monitoring & Logging",
        "question_text": (
            "A team needs to correlate application logs, trace data, and "
            "custom business metrics from a distributed microservices "
            "application running on ECS. Which combination of services "
            "provides the most complete observability?"
        ),
        "option_a": "CloudWatch Logs, CloudWatch Container Insights, and AWS X-Ray",
        "option_b": "S3 access logs only",
        "option_c": "VPC Flow Logs only",
        "option_d": "AWS Trusted Advisor",
        "correct_answer": "A",
        "explanation": (
            "CloudWatch Logs centralizes log data, Container Insights "
            "provides ECS-specific performance metrics, and X-Ray provides "
            "distributed tracing across microservices, together giving full "
            "visibility into logs, metrics, and request traces."
        ),
    },
    {
        "category": "Monitoring & Logging",
        "question_text": (
            "An application emits a custom metric that should trigger an "
            "alarm only if the metric breaches a threshold for 3 consecutive "
            "5-minute periods, to avoid alerting on brief spikes. How should "
            "the CloudWatch alarm be configured?"
        ),
        "option_a": "Set the period to 5 minutes and the evaluation periods (datapoints to alarm) to 3",
        "option_b": "Set the period to 15 minutes with 1 evaluation period",
        "option_c": "Use a composite alarm with no period settings",
        "option_d": "Enable detailed monitoring only",
        "correct_answer": "A",
        "explanation": (
            "Configuring the alarm's period to 5 minutes with an evaluation "
            "period (and datapoints-to-alarm) of 3 means the alarm only "
            "fires after the threshold is breached across 3 consecutive "
            "5-minute datapoints, filtering out short-lived spikes."
        ),
    },
    {
        "category": "Monitoring & Logging",
        "question_text": (
            "A company must retain VPC Flow Logs for 400 days for compliance "
            "but wants to minimize storage cost. What is the most "
            "cost-effective delivery and storage approach?"
        ),
        "option_a": "Deliver flow logs to S3 with a lifecycle policy transitioning objects to Glacier after a short period",
        "option_b": "Deliver flow logs only to CloudWatch Logs with no retention policy",
        "option_c": "Print flow logs to instance console output",
        "option_d": "Disable flow logs after 30 days",
        "correct_answer": "A",
        "explanation": (
            "Delivering VPC Flow Logs directly to S3 and applying a lifecycle "
            "policy to transition older logs to S3 Glacier (or Glacier Deep "
            "Archive) is far cheaper for long-term retention than keeping all "
            "data in CloudWatch Logs indefinitely."
        ),
    },
    {
        "category": "Monitoring & Logging",
        "question_text": (
            "Which CloudWatch feature allows an engineer to run SQL-like "
            "queries directly against log data to quickly find patterns "
            "such as error frequency by request ID, without exporting logs "
            "elsewhere?"
        ),
        "option_a": "CloudWatch Logs Insights",
        "option_b": "CloudWatch Events (EventBridge)",
        "option_c": "CloudWatch Synthetics",
        "option_d": "CloudWatch Dashboards only",
        "correct_answer": "A",
        "explanation": (
            "CloudWatch Logs Insights provides a purpose-built query language "
            "for interactively searching and analyzing log data stored in "
            "CloudWatch Logs, letting engineers filter, aggregate, and sort "
            "results such as error counts grouped by request ID."
        ),
    },
    {
        "category": "Monitoring & Logging",
        "question_text": (
            "A global company wants a single dashboard showing metrics "
            "aggregated from CloudWatch in multiple AWS accounts and "
            "regions. What should be configured to achieve this?"
        ),
        "option_a": "CloudWatch cross-account, cross-region dashboards using CloudWatch's monitoring account feature",
        "option_b": "One dashboard per account manually screen-shared",
        "option_c": "AWS Budgets console",
        "option_d": "CloudTrail Insights",
        "correct_answer": "A",
        "explanation": (
            "CloudWatch supports designating a monitoring account that can "
            "view metrics, alarms, and logs from linked source accounts "
            "across regions, enabling a single unified cross-account, "
            "cross-region dashboard."
        ),
    },
    # ---------------- Incident & Event Response (5) ----------------
    {
        "category": "Incident & Event Response",
        "question_text": (
            "An engineer wants an EC2 instance to be automatically rebooted "
            "whenever it fails an EC2 system status check, without any "
            "manual intervention. What is the simplest native solution?"
        ),
        "option_a": "A CloudWatch alarm on the StatusCheckFailed_System metric with an EC2 recover or reboot action",
        "option_b": "A cron job inside the instance that checks its own health",
        "option_c": "Manually monitoring the console and rebooting when needed",
        "option_d": "AWS Config custom rule with no remediation",
        "correct_answer": "A",
        "explanation": (
            "CloudWatch alarms can be configured with an EC2 action (reboot, "
            "recover, or terminate) tied to the StatusCheckFailed metrics. "
            "This automatically reboots or recovers the instance when a "
            "system status check fails, without human intervention."
        ),
    },
    {
        "category": "Incident & Event Response",
        "question_text": (
            "A security team wants to automatically isolate an EC2 instance "
            "(by changing its security group) the moment GuardDuty reports a "
            "high-severity finding for that instance. What is the best "
            "architecture?"
        ),
        "option_a": "EventBridge rule matching GuardDuty findings that triggers a Lambda function to modify the instance's security group",
        "option_b": "Manually reviewing the GuardDuty console every morning",
        "option_c": "CloudTrail Lake queries run weekly",
        "option_d": "AWS Trusted Advisor checks",
        "correct_answer": "A",
        "explanation": (
            "GuardDuty findings are published to EventBridge. An EventBridge "
            "rule can match on finding severity/type and invoke a Lambda "
            "function that automatically isolates the instance, achieving "
            "near real-time automated incident response."
        ),
    },
    {
        "category": "Incident & Event Response",
        "question_text": (
            "During an incident, an engineer needs to know exactly which IAM "
            "principal made a specific API call that deleted a production "
            "S3 bucket, and when. Which service provides this audit trail?"
        ),
        "option_a": "AWS CloudTrail",
        "option_b": "Amazon Inspector",
        "option_c": "AWS Trusted Advisor",
        "option_d": "Amazon Macie",
        "correct_answer": "A",
        "explanation": (
            "AWS CloudTrail records API calls made in an AWS account, "
            "including who made the call (IAM principal), the source IP, "
            "and the timestamp, making it the correct tool for after-the-fact "
            "incident investigation of API activity."
        ),
    },
    {
        "category": "Incident & Event Response",
        "question_text": (
            "A DevOps team wants Auto Scaling to automatically replace "
            "unhealthy instances behind an Application Load Balancer as soon "
            "as they fail target group health checks, without waiting for "
            "EC2-level status check failures. What should be enabled?"
        ),
        "option_a": "ELB health checks on the Auto Scaling group, in addition to EC2 status checks",
        "option_b": "Only EC2 status checks, since they cover all failure modes",
        "option_c": "Manual instance replacement via the console",
        "option_d": "Scheduled scaling actions only",
        "correct_answer": "A",
        "explanation": (
            "By default, Auto Scaling groups only use EC2 status checks. "
            "Enabling ELB health checks lets the Auto Scaling group also "
            "consider target group health check failures (such as an "
            "application returning errors) and replace unhealthy instances "
            "accordingly."
        ),
    },
    {
        "category": "Incident & Event Response",
        "question_text": (
            "A team wants to automatically create an incident ticket and "
            "notify the on-call engineer whenever a critical CloudWatch "
            "alarm transitions to ALARM state, outside of business hours. "
            "What is an effective serverless approach?"
        ),
        "option_a": "CloudWatch alarm publishes to an SNS topic, which triggers a Lambda function to create the ticket and send notifications",
        "option_b": "An engineer manually checks the CloudWatch console every hour",
        "option_c": "Store the alarm state in S3 and review it weekly",
        "option_d": "Disable the alarm outside business hours",
        "correct_answer": "A",
        "explanation": (
            "CloudWatch alarms can publish state changes to an SNS topic. "
            "Subscribing a Lambda function to that topic allows fully "
            "automated, serverless incident creation and on-call "
            "notification at any time of day."
        ),
    },
    # -------------------- High Availability (5) --------------------
    {
        "category": "High Availability",
        "question_text": (
            "A DevOps engineer must design a multi-AZ RDS deployment that "
            "can automatically fail over to a standby with minimal downtime "
            "if the primary database instance becomes unavailable. Which "
            "RDS feature provides this?"
        ),
        "option_a": "RDS Multi-AZ deployment with a synchronous standby replica",
        "option_b": "A manually created read replica in another region",
        "option_c": "RDS automated backups only",
        "option_d": "A single-AZ instance with frequent snapshots",
        "correct_answer": "A",
        "explanation": (
            "RDS Multi-AZ deployments maintain a synchronously replicated "
            "standby in a different Availability Zone. If the primary fails, "
            "RDS automatically fails over to the standby, typically updating "
            "the DNS endpoint so applications reconnect with minimal manual "
            "effort."
        ),
    },
    {
        "category": "High Availability",
        "question_text": (
            "An application must continue serving read traffic even if an "
            "entire AWS Region becomes unavailable. Which Aurora feature "
            "supports this requirement?"
        ),
        "option_a": "Aurora Global Database with a secondary region for cross-region disaster recovery",
        "option_b": "A single Aurora cluster with Multi-AZ only",
        "option_c": "RDS automated snapshots copied manually",
        "option_d": "Aurora Serverless in one region only",
        "correct_answer": "A",
        "explanation": (
            "Aurora Global Database replicates data to secondary AWS Regions "
            "with low latency, and the secondary region's read replicas can "
            "be promoted quickly during a regional disaster, enabling "
            "cross-region availability that Multi-AZ alone does not provide."
        ),
    },
    {
        "category": "High Availability",
        "question_text": (
            "A DevOps team wants an Auto Scaling group to distribute EC2 "
            "instances evenly across three Availability Zones and "
            "automatically replace any instance in an AZ that becomes "
            "impaired. Which configuration is required?"
        ),
        "option_a": "Configure the Auto Scaling group with subnets in all three AZs and enable health checks",
        "option_b": "Launch all instances manually in a single AZ for simplicity",
        "option_c": "Use a single subnet in one Availability Zone",
        "option_d": "Disable health checks to avoid unnecessary replacements",
        "correct_answer": "A",
        "explanation": (
            "An Auto Scaling group spreads instances across all subnets "
            "(and therefore AZs) it is configured with, and with health "
            "checks enabled, it automatically terminates and replaces "
            "instances in an impaired AZ, maintaining the desired capacity "
            "across the remaining healthy AZs."
        ),
    },
    {
        "category": "High Availability",
        "question_text": (
            "Which Route 53 routing policy is best suited to automatically "
            "stop sending traffic to an unhealthy regional endpoint and "
            "shift it to a healthy one in a different region, without "
            "manual DNS changes?"
        ),
        "option_a": "Failover routing policy with health checks",
        "option_b": "Simple routing policy",
        "option_c": "Weighted routing policy with equal weights",
        "option_d": "Geolocation routing policy",
        "correct_answer": "A",
        "explanation": (
            "Route 53 failover routing, combined with health checks against "
            "each endpoint, automatically routes traffic to a secondary "
            "endpoint when the primary is deemed unhealthy, without any "
            "manual DNS record changes."
        ),
    },
    {
        "category": "High Availability",
        "question_text": (
            "A DevOps engineer needs to test whether an application "
            "gracefully handles the sudden loss of an entire Availability "
            "Zone before a real outage happens. Which AWS-native approach "
            "supports controlled chaos/resilience testing?"
        ),
        "option_a": "AWS Fault Injection Service (FIS) to simulate AZ or resource failures in a controlled experiment",
        "option_b": "Waiting for a real outage to observe behavior",
        "option_c": "Manually deleting production resources without a plan",
        "option_d": "AWS Trusted Advisor cost checks",
        "correct_answer": "A",
        "explanation": (
            "AWS Fault Injection Service (FIS) lets teams run controlled "
            "chaos engineering experiments, such as simulating AZ "
            "impairment, instance termination, or network disruption, to "
            "validate resilience before a real failure occurs."
        ),
    },
    # ------------------- Security & Compliance (5) -------------------
    {
        "category": "Security & Compliance",
        "question_text": (
            "A company must ensure that all objects written to a specific S3 "
            "bucket are automatically encrypted with a customer-managed KMS "
            "key, rejecting any upload that does not specify encryption. How "
            "should this be enforced?"
        ),
        "option_a": "An S3 bucket policy that denies PutObject requests unless the correct KMS encryption header is present",
        "option_b": "Enabling versioning on the bucket",
        "option_c": "Relying on client applications to remember to encrypt",
        "option_d": "Enabling S3 Transfer Acceleration",
        "correct_answer": "A",
        "explanation": (
            "A bucket policy with a Deny statement conditioned on the "
            "s3:x-amz-server-side-encryption (and KMS key ID) request header "
            "enforces server-side encryption with a specific KMS key at the "
            "bucket level, rejecting non-compliant uploads regardless of "
            "client behavior."
        ),
    },
    {
        "category": "Security & Compliance",
        "question_text": (
            "A DevOps engineer needs to grant a CI/CD pipeline running on "
            "CodeBuild temporary, least-privilege access to deploy resources, "
            "without embedding long-lived access keys. What is the best "
            "practice?"
        ),
        "option_a": "Attach an IAM service role to the CodeBuild project with only the permissions needed",
        "option_b": "Hardcode an IAM user's access key and secret key in the buildspec file",
        "option_c": "Use the root account access keys for convenience",
        "option_d": "Share one broad admin IAM user across all pipelines",
        "correct_answer": "A",
        "explanation": (
            "CodeBuild projects assume an IAM service role that provides "
            "temporary credentials scoped to only the permissions required "
            "for the build/deploy tasks, following least privilege and "
            "avoiding the security risks of long-lived embedded access keys."
        ),
    },
    {
        "category": "Security & Compliance",
        "question_text": (
            "A company must continuously verify that no security group in "
            "any account allows unrestricted inbound SSH access (0.0.0.0/0 "
            "on port 22), and automatically remediate violations. Which "
            "service combination is most appropriate?"
        ),
        "option_a": "AWS Config managed rule 'restricted-ssh' with an automatic remediation action",
        "option_b": "Manually reviewing security groups once a year",
        "option_c": "Amazon Macie",
        "option_d": "AWS Certificate Manager",
        "correct_answer": "A",
        "explanation": (
            "AWS Config provides a managed rule that checks security groups "
            "for unrestricted SSH access. Pairing it with an automatic "
            "remediation action (for example, an SSM Automation document "
            "that revokes the offending rule) provides continuous detection "
            "and correction without manual review."
        ),
    },
    {
        "category": "Security & Compliance",
        "question_text": (
            "An organization wants centralized, account-wide guardrails so "
            "that member accounts in AWS Organizations cannot disable "
            "CloudTrail logging, even if an account administrator tries to. "
            "What should be used?"
        ),
        "option_a": "A Service Control Policy (SCP) that denies the cloudtrail:StopLogging and related actions",
        "option_b": "An IAM user policy applied only in the management account",
        "option_c": "A CloudWatch alarm that emails the admin after the fact",
        "option_d": "S3 bucket versioning on the CloudTrail log bucket",
        "correct_answer": "A",
        "explanation": (
            "Service Control Policies (SCPs) in AWS Organizations set "
            "permission guardrails that apply across member accounts, even "
            "overriding what account administrators can do. Denying actions "
            "like cloudtrail:StopLogging or cloudtrail:DeleteTrail at the "
            "SCP level prevents logging from being disabled organization-wide."
        ),
    },
    {
        "category": "Security & Compliance",
        "question_text": (
            "A compliance requirement states that all secrets (database "
            "passwords, API keys) used by applications must be automatically "
            "rotated on a schedule without application downtime. Which AWS "
            "service is purpose-built for this?"
        ),
        "option_a": "AWS Secrets Manager with automatic rotation configured",
        "option_b": "Storing secrets in plaintext environment variables",
        "option_c": "Hardcoding secrets in the application source code",
        "option_d": "Storing secrets in an unencrypted S3 bucket",
        "correct_answer": "A",
        "explanation": (
            "AWS Secrets Manager natively supports automatic, scheduled "
            "rotation of secrets (including built-in rotation for RDS, "
            "Redshift, and DocumentDB), updating the secret value while "
            "applications retrieve the current version at runtime, avoiding "
            "downtime from manual rotation."
        ),
    },
]


def seed_database():
    """Insert categories and questions if the database is currently empty.

    This function is safe to call every time the app starts: it checks
    for existing data first so restarting the app never duplicates rows.
    """

    # If categories already exist, assume seeding has already happened.
    if Category.query.first() is not None:
        return

    # Step 1: create all categories and keep a name -> object map for lookup.
    category_map = {}
    for cat in CATEGORIES:
        category = Category(name=cat["name"], description=cat["description"])
        db.session.add(category)
        category_map[cat["name"]] = category

    # Flush so categories get their primary keys before questions reference them.
    db.session.flush()

    # Step 2: create all questions, linking each to its category.
    for q in QUESTIONS:
        question = Question(
            category_id=category_map[q["category"]].id,
            question_text=q["question_text"],
            option_a=q["option_a"],
            option_b=q["option_b"],
            option_c=q["option_c"],
            option_d=q["option_d"],
            correct_answer=q["correct_answer"],
            explanation=q["explanation"],
        )
        db.session.add(question)

    db.session.commit()
    print(f"Seeded {len(CATEGORIES)} categories and {len(QUESTIONS)} questions.")
