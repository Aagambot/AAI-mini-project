"""
Knowledge Base data: ~40 FAQ/policy entries covering billing, technical,
account, and general support categories.
Used to populate the Chroma vector store.
"""

KB_DOCUMENTS = [
    # ─── BILLING ────────────────────────────────────────────────────────────
    {
        "id": "billing_001",
        "category": "billing",
        "title": "How to view my invoice",
        "content": (
            "You can view and download all your invoices from the Billing section "
            "of your account dashboard. Navigate to Settings → Billing → Invoice History. "
            "Invoices are available in PDF format and are sent automatically to your "
            "registered email address on each billing date."
        ),
    },
    {
        "id": "billing_002",
        "category": "billing",
        "title": "Accepted payment methods",
        "content": (
            "We accept Visa, Mastercard, American Express, and PayPal. "
            "Bank transfers are available for annual enterprise plans. "
            "Prepaid or virtual cards may not be supported. "
            "All transactions are processed securely via Stripe."
        ),
    },
    {
        "id": "billing_003",
        "category": "billing",
        "title": "Refund policy",
        "content": (
            "We offer a 30-day money-back guarantee on all monthly plans. "
            "Annual plan refunds are prorated based on unused months. "
            "To request a refund, contact support with your order ID. "
            "Refunds are processed within 5-7 business days to the original payment method."
        ),
    },
    {
        "id": "billing_004",
        "category": "billing",
        "title": "How to cancel my subscription",
        "content": (
            "You can cancel your subscription at any time from Settings → Billing → Cancel Plan. "
            "Your access continues until the end of the current billing period. "
            "There are no cancellation fees. After cancellation your data is retained for 90 days."
        ),
    },
    {
        "id": "billing_005",
        "category": "billing",
        "title": "Failed payment and retry policy",
        "content": (
            "If a payment fails, we automatically retry on day 3, 7, and 14. "
            "You will receive an email notification after each failed attempt. "
            "You can update your payment method anytime in Settings → Billing. "
            "After three failed retries, your account is downgraded to the free tier."
        ),
    },
    {
        "id": "billing_006",
        "category": "billing",
        "title": "Upgrading or downgrading a plan",
        "content": (
            "You can upgrade or downgrade your plan at any time. "
            "Upgrades take effect immediately with prorated billing. "
            "Downgrades take effect at the start of the next billing cycle. "
            "You can change your plan under Settings → Billing → Change Plan."
        ),
    },
    {
        "id": "billing_007",
        "category": "billing",
        "title": "Tax and VAT information",
        "content": (
            "Prices shown are exclusive of VAT/GST unless otherwise stated. "
            "Applicable taxes are calculated at checkout based on your billing address. "
            "EU customers with a valid VAT number can add it in Settings → Billing → Tax Info "
            "to receive invoices without VAT."
        ),
    },
    {
        "id": "billing_008",
        "category": "billing",
        "title": "Enterprise billing and invoicing",
        "content": (
            "Enterprise plans support custom invoicing, purchase order numbers, and net-30 payment terms. "
            "Contact our sales team at sales@company.com for a custom quote. "
            "Enterprise accounts are managed by a dedicated account executive."
        ),
    },
    # ─── TECHNICAL ──────────────────────────────────────────────────────────
    {
        "id": "tech_001",
        "category": "technical",
        "title": "App won't load or is blank",
        "content": (
            "If the app shows a blank screen or fails to load, try the following: "
            "1) Hard-refresh the page (Ctrl+Shift+R on Windows, Cmd+Shift+R on Mac). "
            "2) Clear browser cache and cookies. "
            "3) Disable browser extensions. "
            "4) Try a different browser or incognito mode. "
            "5) Check our status page at status.company.com for ongoing incidents."
        ),
    },
    {
        "id": "tech_002",
        "category": "technical",
        "title": "API rate limits and quotas",
        "content": (
            "Free plans are limited to 100 API calls per minute and 10,000 per day. "
            "Pro plans allow 1,000 calls per minute. Enterprise plans have custom limits. "
            "Rate limit headers (X-RateLimit-Remaining, X-RateLimit-Reset) are included in every API response. "
            "Exceeding the limit returns HTTP 429 Too Many Requests."
        ),
    },
    {
        "id": "tech_003",
        "category": "technical",
        "title": "Integration with third-party tools",
        "content": (
            "We support native integrations with Slack, GitHub, Jira, and Zapier. "
            "REST API and webhooks are available on Pro and above plans. "
            "Full API documentation is at docs.company.com/api. "
            "OAuth 2.0 is used for all third-party authentication."
        ),
    },
    {
        "id": "tech_004",
        "category": "technical",
        "title": "Data export formats",
        "content": (
            "You can export your data in CSV, JSON, and Excel (XLSX) formats. "
            "Go to Settings → Data → Export. Large exports are queued and delivered via email link. "
            "API-based bulk export is documented at docs.company.com/api/export."
        ),
    },
    {
        "id": "tech_005",
        "category": "technical",
        "title": "Two-factor authentication setup",
        "content": (
            "Enable 2FA under Settings → Security → Two-Factor Authentication. "
            "We support authenticator apps (Google Authenticator, Authy) and SMS. "
            "Backup codes are generated when 2FA is enabled; store them safely. "
            "2FA is mandatory for all admin accounts."
        ),
    },
    {
        "id": "tech_006",
        "category": "technical",
        "title": "Webhook configuration and debugging",
        "content": (
            "Webhooks can be configured in Settings → Integrations → Webhooks. "
            "Each webhook event is logged in the dashboard with the full request/response payload. "
            "Failed deliveries are retried up to 5 times with exponential back-off. "
            "Verify your endpoint by checking for the X-Company-Signature header."
        ),
    },
    {
        "id": "tech_007",
        "category": "technical",
        "title": "Mobile app troubleshooting",
        "content": (
            "Ensure you have the latest version of the app from the App Store or Google Play. "
            "Force-quit and relaunch the app if it freezes. "
            "Clear the app cache in your phone's Settings → Apps → [App Name] → Storage. "
            "Re-login if you experience authentication errors after an update."
        ),
    },
    {
        "id": "tech_008",
        "category": "technical",
        "title": "Error code reference",
        "content": (
            "Common error codes: "
            "400 Bad Request – invalid parameters; check your request payload. "
            "401 Unauthorized – missing or expired API key. "
            "403 Forbidden – action not allowed on your plan. "
            "404 Not Found – resource does not exist. "
            "500 Internal Server Error – retry after a moment; contact support if it persists."
        ),
    },
    {
        "id": "tech_009",
        "category": "technical",
        "title": "SSO and SAML configuration",
        "content": (
            "SAML-based SSO is available on Enterprise plans. "
            "Configuration requires your Identity Provider (IdP) metadata URL. "
            "Supported IdPs: Okta, Azure AD, Google Workspace. "
            "Setup guide: docs.company.com/sso. Contact support for hands-on assistance."
        ),
    },
    {
        "id": "tech_010",
        "category": "technical",
        "title": "Performance and slow loading",
        "content": (
            "Slow performance is often caused by large datasets or complex queries. "
            "Use pagination and filters to reduce data volume. "
            "Enable caching where available. "
            "Check your internet connection speed. "
            "If the problem is on our side, it will appear on status.company.com."
        ),
    },
    # ─── ACCOUNT ────────────────────────────────────────────────────────────
    {
        "id": "account_001",
        "category": "account",
        "title": "How to reset your password",
        "content": (
            "Go to the login page and click 'Forgot Password'. "
            "Enter your registered email address and you will receive a reset link within 5 minutes. "
            "The link expires after 1 hour. "
            "If you don't receive the email, check your spam folder or contact support."
        ),
    },
    {
        "id": "account_002",
        "category": "account",
        "title": "Changing your email address",
        "content": (
            "To change your email, go to Settings → Profile → Email. "
            "A verification link is sent to the new address. "
            "The change takes effect once the new email is verified. "
            "Your old email will receive a notification of the change for security."
        ),
    },
    {
        "id": "account_003",
        "category": "account",
        "title": "Adding and managing team members",
        "content": (
            "Invite team members under Settings → Team → Invite Member. "
            "Enter their email and choose a role: Admin, Editor, or Viewer. "
            "Admins can manage billing and all settings. "
            "Editors can create and edit content. Viewers have read-only access."
        ),
    },
    {
        "id": "account_004",
        "category": "account",
        "title": "Account deletion and data removal",
        "content": (
            "To permanently delete your account, go to Settings → Account → Delete Account. "
            "All data is permanently removed within 30 days in accordance with GDPR. "
            "Exported data will no longer be accessible once deletion is processed. "
            "This action is irreversible; please export your data first."
        ),
    },
    {
        "id": "account_005",
        "category": "account",
        "title": "Transferring account ownership",
        "content": (
            "Account ownership can be transferred to another member with an Admin role. "
            "Go to Settings → Team → [Member] → Transfer Ownership. "
            "The new owner receives an email to confirm the transfer. "
            "Only one owner is allowed per account at a time."
        ),
    },
    {
        "id": "account_006",
        "category": "account",
        "title": "Locked or suspended account",
        "content": (
            "Accounts may be locked after 10 consecutive failed login attempts. "
            "A temporary lock lasts 30 minutes and is lifted automatically. "
            "For suspected fraud or policy violations, accounts may be suspended. "
            "Contact support at support@company.com with your account email to appeal a suspension."
        ),
    },
    {
        "id": "account_007",
        "category": "account",
        "title": "Profile settings and preferences",
        "content": (
            "Update your name, avatar, timezone, and notification preferences under Settings → Profile. "
            "Notification preferences let you control email, in-app, and Slack alerts. "
            "Language and date format can be set under Settings → Profile → Locale."
        ),
    },
    {
        "id": "account_008",
        "category": "account",
        "title": "GDPR and data privacy rights",
        "content": (
            "You have the right to access, correct, and delete your personal data. "
            "Submit a Data Subject Access Request (DSAR) at privacy@company.com. "
            "We process DSARs within 30 days. "
            "Full privacy policy: company.com/privacy."
        ),
    },
    # ─── GENERAL ────────────────────────────────────────────────────────────
    {
        "id": "general_001",
        "category": "general",
        "title": "Contacting support",
        "content": (
            "You can reach our support team via live chat (Mon-Fri, 9 AM - 6 PM UTC), "
            "email at support@company.com, or by submitting a ticket in the Help Center. "
            "Pro and Enterprise customers also have access to priority support with guaranteed response SLAs."
        ),
    },
    {
        "id": "general_002",
        "category": "general",
        "title": "Support response times and SLAs",
        "content": (
            "Free plan: best effort, typically 2-3 business days. "
            "Pro plan: first response within 8 business hours. "
            "Enterprise plan: first response within 1 business hour, 24/7 for critical issues. "
            "Critical issues (service down) are escalated immediately regardless of plan."
        ),
    },
    {
        "id": "general_003",
        "category": "general",
        "title": "What is the free plan?",
        "content": (
            "The free plan includes up to 3 users, 5 GB storage, basic integrations, "
            "and community support. There is no credit card required to sign up. "
            "Free plans have API rate limits of 100 requests/minute. "
            "You can upgrade to Pro at any time from Settings → Billing."
        ),
    },
    {
        "id": "general_004",
        "category": "general",
        "title": "Service status and incident updates",
        "content": (
            "Real-time service status is available at status.company.com. "
            "Subscribe to email or SMS notifications for incident updates. "
            "Planned maintenance is announced at least 48 hours in advance. "
            "Post-incident reports (PIRs) are published within 72 hours of resolution."
        ),
    },
    {
        "id": "general_005",
        "category": "general",
        "title": "Feature requests and roadmap",
        "content": (
            "Submit feature requests at feedback.company.com. "
            "Upvote existing requests to signal priority. "
            "The public roadmap is at company.com/roadmap. "
            "Top-voted features are reviewed quarterly by the product team."
        ),
    },
    {
        "id": "general_006",
        "category": "general",
        "title": "Accessibility and compliance",
        "content": (
            "Our product meets WCAG 2.1 AA accessibility standards. "
            "We are SOC 2 Type II, ISO 27001, and GDPR compliant. "
            "HIPAA BAA is available for qualifying Enterprise customers. "
            "Compliance documentation is available at company.com/compliance."
        ),
    },
    {
        "id": "general_007",
        "category": "general",
        "title": "Referral and affiliate program",
        "content": (
            "Earn a 20% recurring commission for every customer you refer on a paid plan. "
            "Sign up for the affiliate program at company.com/affiliates. "
            "Payouts are processed monthly via PayPal or bank transfer. "
            "Referral links are available in your dashboard under Account → Referrals."
        ),
    },
    {
        "id": "general_008",
        "category": "general",
        "title": "Onboarding and getting started",
        "content": (
            "After signing up, complete the onboarding checklist in your dashboard. "
            "Watch the getting-started video series at docs.company.com/start. "
            "Schedule a free 30-minute onboarding call with our success team via the Help Center. "
            "Our interactive product tour guides you through core features on first login."
        ),
    },
    {
        "id": "general_009",
        "category": "general",
        "title": "Partnerships and reseller program",
        "content": (
            "We offer a reseller program for agencies and MSPs. "
            "Resellers receive volume discounts of 20-40% depending on tier. "
            "Apply at company.com/partners. "
            "A dedicated partner manager is assigned to Silver tier and above partners."
        ),
    },
    {
        "id": "general_010",
        "category": "general",
        "title": "Community and learning resources",
        "content": (
            "Join our community forum at community.company.com to ask questions and share tips. "
            "The Help Center at help.company.com contains articles, tutorials, and video guides. "
            "Weekly live webinars are open to all users – register at company.com/webinars. "
            "Our certification program is available at company.com/certifications."
        ),
    },
]
