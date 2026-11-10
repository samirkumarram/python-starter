
from pathlib import Path

OUTPUT_DIR = Path("rag_lab/documents")

policies = [
    ("Leave Policy", "Employees receive 20 days of paid leave annually. Leave requests must be submitted to the manager at least 3 working days in advance.", "Emergency leave can be approved by the HR manager."),

    ("Work From Home Policy", "Employees can work from home up to 2 days per week. Requests must be approved by the reporting manager.", "Employees handling restricted office equipment must work from the office."),

    ("Data Security Policy", "Employees must use strong passwords with at least 12 characters. Passwords must be changed every 90 days.", "Security administrators can enforce immediate password resets."),

    ("Password Policy", "Passwords must contain uppercase letters, lowercase letters, numbers and special characters. Password sharing is prohibited.", "Temporary passwords must be changed at first login."),

    ("Employee Attendance Policy", "Employees must complete 8 working hours daily. Attendance must be recorded using the official attendance system.", "Approved business travel is exempt from office check-in."),

    ("Remote Access Policy", "Remote access is permitted only through the company VPN. Multi-factor authentication is mandatory.", "IT administrators may temporarily disable access during security incidents."),

    ("Email Usage Policy", "Company email accounts must be used for official communication. Employees must not share confidential information through personal email.", "HR-approved external communication is permitted."),

    ("Device Usage Policy", "Company laptops must use approved antivirus software and automatic screen locking. Employees must not install unauthorized applications.", "IT support can approve software installations."),

    ("Incident Reporting Policy", "Employees must report security incidents to the IT security team within 30 minutes of discovery.", "Critical incidents must be escalated immediately to the security manager."),

    ("Data Retention Policy", "Customer transaction records must be retained for 7 years. Access to archived records requires authorization.", "Legal holds can extend the retention period."),

    ("Customer Privacy Policy", "Customer personal information must only be accessed for legitimate business purposes. Unauthorized disclosure is prohibited.", "Disclosure required by law must be approved by the legal team."),

    ("Access Control Policy", "Employees receive access based on their job responsibilities. Managers must review access permissions every 6 months.", "Emergency access requires security team approval."),

    ("Backup Policy", "Critical business databases must be backed up daily. Backup copies must be stored in a separate secure location.", "IT administrators must verify backup restoration every quarter."),

    ("Business Continuity Policy", "Critical business applications must be restored within 4 hours of a major outage. The disaster recovery plan must be tested annually.", "The business continuity manager can declare a disaster."),

    ("Software Development Policy", "All production code changes require peer review and automated testing. Direct changes to production systems are prohibited.", "Emergency fixes require approval from the engineering manager."),

    ("Vendor Management Policy", "All vendors must pass security assessment before accessing company systems. Vendor agreements must define data protection responsibilities.", "High-risk vendors require additional security reviews."),

    ("Expense Reimbursement Policy", "Employees can claim approved business travel expenses within 30 days. Receipts are required for expenses above 500 rupees.", "Exceptions require finance department approval."),

    ("Training Policy", "Employees must complete mandatory security awareness training every year. Training completion is tracked by HR.", "New employees must complete training within 30 days of joining."),

    ("Mobile Device Policy", "Employees accessing company data on mobile devices must enable device encryption and screen locking.", "Lost or stolen devices must be reported to IT within 1 hour."),

    ("Employee Exit Policy", "Employees leaving the company must return company assets on their last working day. IT must revoke system access within 24 hours of departure.", "HR can request immediate access revocation.")
]

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

for index, (title, rule, exception) in enumerate(policies, start=1):
    content = f"""
Policy ID: POL-{index:03}
Policy Name: {title}

Purpose:
This document defines the organization's {title.lower()}.

Policy Rules:
{rule}

Exceptions:
{exception}

Responsibility:
The relevant department is responsible for implementing
and monitoring this policy.

Review:
This policy must be reviewed annually.
"""

    file_path = OUTPUT_DIR / f"policy_{index:02}.txt"
    file_path.write_text(content.strip(), encoding="utf-8")

print(f"Generated {len(policies)} policy documents.")
