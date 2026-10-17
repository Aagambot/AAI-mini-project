"""
Labeled dataset of 80 support tickets with:
- ticket_id, text, expected_category, expected_priority, reference_reply
Used as the LangSmith evaluation dataset.
"""

LABELED_TICKETS = [
    # ─── BILLING (20 tickets) ───────────────────────────────────────────────
    {
        "ticket_id": "T001",
        "text": "I was charged twice for this month. Please refund the duplicate charge.",
        "expected_category": "billing",
        "expected_priority": "high",
        "reference_reply": (
            "We're sorry to hear about the duplicate charge. Please share your order ID "
            "and we'll investigate immediately. If confirmed, a refund will be processed "
            "to your original payment method within 5-7 business days."
        ),
    },
    {
        "ticket_id": "T002",
        "text": "Where can I download my invoice for last month?",
        "expected_category": "billing",
        "expected_priority": "low",
        "reference_reply": (
            "You can download your invoices from Settings → Billing → Invoice History. "
            "They are available in PDF format and also sent to your registered email."
        ),
    },
    {
        "ticket_id": "T003",
        "text": "My credit card payment keeps failing. What should I do?",
        "expected_category": "billing",
        "expected_priority": "high",
        "reference_reply": (
            "Sorry for the trouble! Please update your card details in Settings → Billing. "
            "If the issue persists, try a different card or contact your bank. "
            "We retry failed payments on days 3, 7, and 14."
        ),
    },
    {
        "ticket_id": "T004",
        "text": "I want to cancel my subscription. How do I do that?",
        "expected_category": "billing",
        "expected_priority": "medium",
        "reference_reply": (
            "You can cancel at any time from Settings → Billing → Cancel Plan. "
            "Your access continues through the end of your billing period, "
            "and there are no cancellation fees."
        ),
    },
    {
        "ticket_id": "T005",
        "text": "Do you accept PayPal?",
        "expected_category": "billing",
        "expected_priority": "low",
        "reference_reply": (
            "Yes, we accept PayPal along with Visa, Mastercard, and American Express. "
            "All transactions are processed securely via Stripe."
        ),
    },
    {
        "ticket_id": "T006",
        "text": "Can I get a refund? I signed up 2 weeks ago and haven't used the product.",
        "expected_category": "billing",
        "expected_priority": "medium",
        "reference_reply": (
            "Absolutely! We offer a 30-day money-back guarantee. "
            "Please share your order ID and we'll process the refund within 5-7 business days."
        ),
    },
    {
        "ticket_id": "T007",
        "text": "How does the annual plan discount work?",
        "expected_category": "billing",
        "expected_priority": "low",
        "reference_reply": (
            "Annual plans are billed upfront and include a discount equivalent to 2 months free. "
            "You can switch to annual billing anytime from Settings → Billing → Change Plan."
        ),
    },
    {
        "ticket_id": "T008",
        "text": "I need an invoice with our company VAT number on it.",
        "expected_category": "billing",
        "expected_priority": "medium",
        "reference_reply": (
            "You can add your VAT number in Settings → Billing → Tax Info. "
            "Once saved, all future invoices will include it. "
            "For past invoices, please contact support and we'll reissue them."
        ),
    },
    {
        "ticket_id": "T009",
        "text": "What happens to my data if I downgrade to the free plan?",
        "expected_category": "billing",
        "expected_priority": "medium",
        "reference_reply": (
            "When you downgrade, your data is retained, but features above the free tier limits "
            "become inaccessible. We recommend exporting any data that exceeds free plan limits before downgrading."
        ),
    },
    {
        "ticket_id": "T010",
        "text": "We need a custom invoice with a purchase order number.",
        "expected_category": "billing",
        "expected_priority": "medium",
        "reference_reply": (
            "Custom invoicing with PO numbers is available on Enterprise plans. "
            "Please contact our sales team at sales@company.com to discuss your requirements."
        ),
    },
    {
        "ticket_id": "T011",
        "text": "I upgraded but my account still shows the old plan.",
        "expected_category": "billing",
        "expected_priority": "high",
        "reference_reply": (
            "Upgrades take effect immediately. Please try logging out and back in. "
            "If the issue persists, contact support with your order confirmation number."
        ),
    },
    {
        "ticket_id": "T012",
        "text": "Is there a student discount available?",
        "expected_category": "billing",
        "expected_priority": "low",
        "reference_reply": (
            "We currently don't offer a specific student discount, but our free plan is available "
            "to everyone with no credit card required. Check company.com/pricing for current promotions."
        ),
    },
    {
        "ticket_id": "T013",
        "text": "My account was suspended after a failed payment. How do I reactivate it?",
        "expected_category": "billing",
        "expected_priority": "high",
        "reference_reply": (
            "After three failed retries, accounts are downgraded to free tier. "
            "Update your payment method in Settings → Billing and resubscribe to your plan. "
            "Your data is preserved during this period."
        ),
    },
    {
        "ticket_id": "T014",
        "text": "Can I switch from monthly to annual billing mid-cycle?",
        "expected_category": "billing",
        "expected_priority": "low",
        "reference_reply": (
            "Yes! You can switch at any time. Upgrades to annual are prorated, so you only "
            "pay the difference for the remaining days in your current billing cycle."
        ),
    },
    {
        "ticket_id": "T015",
        "text": "Why was I charged a different amount than what was shown at checkout?",
        "expected_category": "billing",
        "expected_priority": "high",
        "reference_reply": (
            "The difference is likely due to applicable VAT/GST taxes added at checkout "
            "based on your billing address. Check your invoice for a full tax breakdown. "
            "Contact support if the discrepancy is not tax-related."
        ),
    },
    {
        "ticket_id": "T016",
        "text": "I need to update my billing address.",
        "expected_category": "billing",
        "expected_priority": "low",
        "reference_reply": (
            "Update your billing address in Settings → Billing → Payment Details. "
            "The new address will appear on future invoices."
        ),
    },
    {
        "ticket_id": "T017",
        "text": "Do you offer non-profit discounts?",
        "expected_category": "billing",
        "expected_priority": "low",
        "reference_reply": (
            "Yes, we offer a 30% discount for registered non-profit organizations. "
            "Contact sales@company.com with proof of non-profit status to apply."
        ),
    },
    {
        "ticket_id": "T018",
        "text": "I cancelled but was still charged. This is unacceptable.",
        "expected_category": "billing",
        "expected_priority": "high",
        "reference_reply": (
            "We sincerely apologize for this inconvenience. "
            "Please share your cancellation confirmation and the charge date. "
            "We will investigate and issue a full refund if the charge was in error."
        ),
    },
    {
        "ticket_id": "T019",
        "text": "What currency do you charge in?",
        "expected_category": "billing",
        "expected_priority": "low",
        "reference_reply": (
            "We charge in USD by default. Some regions may see prices displayed in local currency, "
            "but the charge is always converted to USD at the time of transaction."
        ),
    },
    {
        "ticket_id": "T020",
        "text": "How do I add a backup payment method?",
        "expected_category": "billing",
        "expected_priority": "low",
        "reference_reply": (
            "Go to Settings → Billing → Payment Methods to add additional cards. "
            "You can set a default payment method, and all backups are stored securely."
        ),
    },
    # ─── TECHNICAL (20 tickets) ─────────────────────────────────────────────
    {
        "ticket_id": "T021",
        "text": "The app won't load. I just see a white screen.",
        "expected_category": "technical",
        "expected_priority": "high",
        "reference_reply": (
            "Try hard-refreshing the page (Ctrl+Shift+R), clearing your browser cache, "
            "and disabling extensions. Also check status.company.com for any ongoing incidents."
        ),
    },
    {
        "ticket_id": "T022",
        "text": "I'm getting a 429 error from the API.",
        "expected_category": "technical",
        "expected_priority": "high",
        "reference_reply": (
            "HTTP 429 means you've exceeded your rate limit. "
            "Free plans allow 100 calls/minute. Check the X-RateLimit-Remaining response header "
            "and implement exponential back-off in your code."
        ),
    },
    {
        "ticket_id": "T023",
        "text": "How do I set up 2FA on my account?",
        "expected_category": "technical",
        "expected_priority": "low",
        "reference_reply": (
            "Enable 2FA under Settings → Security → Two-Factor Authentication. "
            "We support authenticator apps like Google Authenticator and Authy, as well as SMS. "
            "Save your backup codes in a secure location."
        ),
    },
    {
        "ticket_id": "T024",
        "text": "My webhooks are not being delivered.",
        "expected_category": "technical",
        "expected_priority": "high",
        "reference_reply": (
            "Check the webhook logs in Settings → Integrations → Webhooks for failed delivery details. "
            "Failed deliveries are retried up to 5 times. Ensure your endpoint is publicly accessible "
            "and returns a 2xx status code."
        ),
    },
    {
        "ticket_id": "T025",
        "text": "Can I export my data to CSV?",
        "expected_category": "technical",
        "expected_priority": "low",
        "reference_reply": (
            "Yes! Go to Settings → Data → Export and select CSV format. "
            "Large exports are queued and a download link is sent to your email."
        ),
    },
    {
        "ticket_id": "T026",
        "text": "I'm getting a 401 Unauthorized error on the API.",
        "expected_category": "technical",
        "expected_priority": "high",
        "reference_reply": (
            "A 401 error means your API key is missing or expired. "
            "Check that you're including the Authorization: Bearer <your_api_key> header. "
            "Regenerate your API key in Settings → API Keys if needed."
        ),
    },
    {
        "ticket_id": "T027",
        "text": "How do I connect my Slack workspace?",
        "expected_category": "technical",
        "expected_priority": "low",
        "reference_reply": (
            "Go to Settings → Integrations → Slack and click 'Connect to Slack'. "
            "You'll be redirected through Slack's OAuth flow. "
            "The integration requires the Pro plan or higher."
        ),
    },
    {
        "ticket_id": "T028",
        "text": "The app is very slow today. Is there an outage?",
        "expected_category": "technical",
        "expected_priority": "medium",
        "reference_reply": (
            "Please check status.company.com for real-time service status. "
            "If your connection is fine and we have no reported incidents, "
            "try reducing the data volume in your queries using filters and pagination."
        ),
    },
    {
        "ticket_id": "T029",
        "text": "How do I configure SSO with Okta?",
        "expected_category": "technical",
        "expected_priority": "medium",
        "reference_reply": (
            "SAML SSO with Okta is available on Enterprise plans. "
            "You'll need your Okta metadata URL. Follow the guide at docs.company.com/sso "
            "or contact support for hands-on setup assistance."
        ),
    },
    {
        "ticket_id": "T030",
        "text": "My mobile app crashes on startup after the latest update.",
        "expected_category": "technical",
        "expected_priority": "high",
        "reference_reply": (
            "Please clear the app cache (Settings → Apps → [App Name] → Storage → Clear Cache) "
            "and relaunch. If that doesn't work, uninstall and reinstall the latest version. "
            "Share your device model and OS version if the issue persists."
        ),
    },
    {
        "ticket_id": "T031",
        "text": "What programming languages does your API support?",
        "expected_category": "technical",
        "expected_priority": "low",
        "reference_reply": (
            "Our REST API works with any language that can make HTTP requests. "
            "Official SDKs are available for Python, JavaScript, Ruby, and Go. "
            "Full documentation is at docs.company.com/api."
        ),
    },
    {
        "ticket_id": "T032",
        "text": "I see a 500 error when I try to save my settings.",
        "expected_category": "technical",
        "expected_priority": "high",
        "reference_reply": (
            "A 500 error is an internal server error. Please try again after a few minutes. "
            "If it persists, contact support with the exact time and the steps you took "
            "so we can investigate the server logs."
        ),
    },
    {
        "ticket_id": "T033",
        "text": "How do I verify my webhook signature?",
        "expected_category": "technical",
        "expected_priority": "medium",
        "reference_reply": (
            "Check for the X-Company-Signature header on incoming webhook requests. "
            "Compare it against an HMAC-SHA256 of the request body using your webhook secret. "
            "Full verification guide: docs.company.com/webhooks/security."
        ),
    },
    {
        "ticket_id": "T034",
        "text": "The GitHub integration stopped syncing.",
        "expected_category": "technical",
        "expected_priority": "high",
        "reference_reply": (
            "Try reconnecting the GitHub integration under Settings → Integrations → GitHub. "
            "Ensure the GitHub App still has permission to your repositories. "
            "Check the integration logs for specific error messages."
        ),
    },
    {
        "ticket_id": "T035",
        "text": "Can I use your API without OAuth?",
        "expected_category": "technical",
        "expected_priority": "low",
        "reference_reply": (
            "Yes! For server-to-server integrations you can use API keys instead of OAuth. "
            "Generate an API key in Settings → API Keys. OAuth is only required for "
            "user-facing third-party integrations."
        ),
    },
    {
        "ticket_id": "T036",
        "text": "My 2FA codes are not working.",
        "expected_category": "technical",
        "expected_priority": "high",
        "reference_reply": (
            "Ensure your device's clock is synchronized (TOTP codes are time-sensitive). "
            "If using an authenticator app, re-sync the time. "
            "Use a backup code to log in, then re-configure 2FA under Settings → Security."
        ),
    },
    {
        "ticket_id": "T037",
        "text": "How do I bulk export data via the API?",
        "expected_category": "technical",
        "expected_priority": "low",
        "reference_reply": (
            "Use the bulk export endpoint documented at docs.company.com/api/export. "
            "Paginate results using the cursor parameter. "
            "Large jobs are asynchronous; poll the job status endpoint for completion."
        ),
    },
    {
        "ticket_id": "T038",
        "text": "The app works in Chrome but not Firefox. Why?",
        "expected_category": "technical",
        "expected_priority": "medium",
        "reference_reply": (
            "This is likely a browser extension or cookie conflict. "
            "Try Firefox in private mode with no extensions. "
            "Clear Firefox cache and cookies. Report the specific error if it persists."
        ),
    },
    {
        "ticket_id": "T039",
        "text": "How many API calls can I make per day on the free plan?",
        "expected_category": "technical",
        "expected_priority": "low",
        "reference_reply": (
            "The free plan allows 10,000 API calls per day and 100 per minute. "
            "Check the X-RateLimit-Remaining header to track your usage in real time."
        ),
    },
    {
        "ticket_id": "T040",
        "text": "The Jira integration isn't creating tickets automatically.",
        "expected_category": "technical",
        "expected_priority": "high",
        "reference_reply": (
            "Reconnect the Jira integration in Settings → Integrations → Jira. "
            "Verify the Jira API token has the necessary project permissions. "
            "Check the integration logs for error details."
        ),
    },
    # ─── ACCOUNT (20 tickets) ───────────────────────────────────────────────
    {
        "ticket_id": "T041",
        "text": "I forgot my password and can't log in.",
        "expected_category": "account",
        "expected_priority": "high",
        "reference_reply": (
            "Click 'Forgot Password' on the login page and enter your registered email. "
            "You'll receive a reset link within 5 minutes. Check your spam folder if it doesn't arrive."
        ),
    },
    {
        "ticket_id": "T042",
        "text": "I want to change the email address on my account.",
        "expected_category": "account",
        "expected_priority": "medium",
        "reference_reply": (
            "Go to Settings → Profile → Email, enter your new address, and verify it via "
            "the link sent to the new email. Your old email will also receive a security notification."
        ),
    },
    {
        "ticket_id": "T043",
        "text": "How do I add a new team member?",
        "expected_category": "account",
        "expected_priority": "low",
        "reference_reply": (
            "Go to Settings → Team → Invite Member and enter their email address. "
            "Choose their role (Admin, Editor, or Viewer) and send the invitation."
        ),
    },
    {
        "ticket_id": "T044",
        "text": "I want to permanently delete my account.",
        "expected_category": "account",
        "expected_priority": "medium",
        "reference_reply": (
            "You can delete your account from Settings → Account → Delete Account. "
            "All data is permanently removed within 30 days. This action is irreversible, "
            "so please export your data first."
        ),
    },
    {
        "ticket_id": "T045",
        "text": "My account has been locked out. How do I get back in?",
        "expected_category": "account",
        "expected_priority": "high",
        "reference_reply": (
            "Accounts are temporarily locked for 30 minutes after 10 failed login attempts. "
            "The lock lifts automatically. Use 'Forgot Password' if you've forgotten your credentials."
        ),
    },
    {
        "ticket_id": "T046",
        "text": "How do I transfer ownership of the account to someone else?",
        "expected_category": "account",
        "expected_priority": "medium",
        "reference_reply": (
            "Go to Settings → Team → [Member Name] → Transfer Ownership. "
            "The new owner must have an Admin role and will receive an email to confirm the transfer."
        ),
    },
    {
        "ticket_id": "T047",
        "text": "I didn't receive the verification email.",
        "expected_category": "account",
        "expected_priority": "medium",
        "reference_reply": (
            "Check your spam or junk folder. Try clicking 'Resend Verification Email' on the login page. "
            "Ensure the email address is correct. Contact support if it still doesn't arrive."
        ),
    },
    {
        "ticket_id": "T048",
        "text": "How do I change a team member's role from Viewer to Editor?",
        "expected_category": "account",
        "expected_priority": "low",
        "reference_reply": (
            "Go to Settings → Team, click on the team member's name, and select their new role. "
            "The change takes effect immediately."
        ),
    },
    {
        "ticket_id": "T049",
        "text": "I want to request a copy of all data you hold on me (GDPR request).",
        "expected_category": "account",
        "expected_priority": "medium",
        "reference_reply": (
            "Submit a Data Subject Access Request at privacy@company.com. "
            "We will process your request within 30 days as required by GDPR."
        ),
    },
    {
        "ticket_id": "T050",
        "text": "My account was suspended. I believe it was a mistake.",
        "expected_category": "account",
        "expected_priority": "high",
        "reference_reply": (
            "We're sorry to hear that. Please email support@company.com with your account email "
            "and a brief explanation. We'll review and respond within 1 business day."
        ),
    },
    {
        "ticket_id": "T051",
        "text": "How do I update my profile picture?",
        "expected_category": "account",
        "expected_priority": "low",
        "reference_reply": (
            "Go to Settings → Profile → Avatar and upload a new image. "
            "Supported formats: JPG, PNG, GIF (max 5MB)."
        ),
    },
    {
        "ticket_id": "T052",
        "text": "I can't remove a team member who left the company.",
        "expected_category": "account",
        "expected_priority": "medium",
        "reference_reply": (
            "Go to Settings → Team, find the member, and click 'Remove Member'. "
            "Only Admin-level users can remove team members. Contact support if you're blocked."
        ),
    },
    {
        "ticket_id": "T053",
        "text": "I keep getting logged out every time I close my browser.",
        "expected_category": "account",
        "expected_priority": "low",
        "reference_reply": (
            "This is likely because your browser clears cookies on close. "
            "Check your browser's privacy settings and allow cookies for our domain. "
            "Tick 'Remember me' at login to extend your session."
        ),
    },
    {
        "ticket_id": "T054",
        "text": "How do I change my timezone settings?",
        "expected_category": "account",
        "expected_priority": "low",
        "reference_reply": (
            "Update your timezone under Settings → Profile → Locale. "
            "All dates and times in the app will reflect the selected timezone."
        ),
    },
    {
        "ticket_id": "T055",
        "text": "Someone else is logged into my account. I think I've been hacked.",
        "expected_category": "account",
        "expected_priority": "high",
        "reference_reply": (
            "Change your password immediately under Settings → Security → Change Password. "
            "Enable 2FA if not already active. Review active sessions and revoke any unknown ones "
            "in Settings → Security → Active Sessions. Contact support if you need further assistance."
        ),
    },
    {
        "ticket_id": "T056",
        "text": "How do I turn off email notifications?",
        "expected_category": "account",
        "expected_priority": "low",
        "reference_reply": (
            "Manage notification preferences in Settings → Profile → Notifications. "
            "You can toggle email, in-app, and Slack notifications independently."
        ),
    },
    {
        "ticket_id": "T057",
        "text": "Can I merge two accounts into one?",
        "expected_category": "account",
        "expected_priority": "medium",
        "reference_reply": (
            "Account merging is not self-serve at this time. "
            "Contact support@company.com with both account emails and we'll assist manually."
        ),
    },
    {
        "ticket_id": "T058",
        "text": "I need to change the language in the app.",
        "expected_category": "account",
        "expected_priority": "low",
        "reference_reply": (
            "Change the app language in Settings → Profile → Locale. "
            "Currently supported languages include English, French, German, and Spanish."
        ),
    },
    {
        "ticket_id": "T059",
        "text": "My password reset link is expired.",
        "expected_category": "account",
        "expected_priority": "medium",
        "reference_reply": (
            "Password reset links expire after 1 hour. "
            "Please request a new link by clicking 'Forgot Password' on the login page."
        ),
    },
    {
        "ticket_id": "T060",
        "text": "How do I see who has accessed my account recently?",
        "expected_category": "account",
        "expected_priority": "low",
        "reference_reply": (
            "Go to Settings → Security → Active Sessions to see all current sessions "
            "and recent login activity. You can revoke any suspicious session from there."
        ),
    },
    # ─── GENERAL (20 tickets) ───────────────────────────────────────────────
    {
        "ticket_id": "T061",
        "text": "How fast will you respond to my support request?",
        "expected_category": "general",
        "expected_priority": "low",
        "reference_reply": (
            "Response times depend on your plan: Free (2-3 business days), "
            "Pro (within 8 hours), Enterprise (within 1 hour). "
            "Critical issues are escalated immediately regardless of plan."
        ),
    },
    {
        "ticket_id": "T062",
        "text": "What features are included in the free plan?",
        "expected_category": "general",
        "expected_priority": "low",
        "reference_reply": (
            "The free plan includes up to 3 users, 5 GB storage, basic integrations, "
            "community support, and 100 API calls/minute. No credit card required."
        ),
    },
    {
        "ticket_id": "T063",
        "text": "Is the service currently down? I can't access anything.",
        "expected_category": "general",
        "expected_priority": "high",
        "reference_reply": (
            "Check real-time status at status.company.com. "
            "Subscribe to incident updates for SMS or email notifications. "
            "If your issue is not reflected there, contact support immediately."
        ),
    },
    {
        "ticket_id": "T064",
        "text": "How do I suggest a new feature?",
        "expected_category": "general",
        "expected_priority": "low",
        "reference_reply": (
            "Submit feature requests at feedback.company.com and upvote existing ideas. "
            "The public roadmap is at company.com/roadmap. Top-voted features are reviewed quarterly."
        ),
    },
    {
        "ticket_id": "T065",
        "text": "Is your product GDPR compliant?",
        "expected_category": "general",
        "expected_priority": "low",
        "reference_reply": (
            "Yes, we are GDPR compliant. We also hold SOC 2 Type II and ISO 27001 certifications. "
            "Full compliance documentation: company.com/compliance."
        ),
    },
    {
        "ticket_id": "T066",
        "text": "I'm new. How do I get started?",
        "expected_category": "general",
        "expected_priority": "low",
        "reference_reply": (
            "Welcome! Complete the onboarding checklist in your dashboard, "
            "watch the getting-started videos at docs.company.com/start, "
            "and schedule a free onboarding call via the Help Center."
        ),
    },
    {
        "ticket_id": "T067",
        "text": "Do you have an affiliate program?",
        "expected_category": "general",
        "expected_priority": "low",
        "reference_reply": (
            "Yes! Earn a 20% recurring commission for referrals. "
            "Sign up at company.com/affiliates. Payouts are processed monthly."
        ),
    },
    {
        "ticket_id": "T068",
        "text": "When will the planned maintenance end?",
        "expected_category": "general",
        "expected_priority": "medium",
        "reference_reply": (
            "Maintenance windows and their expected end times are posted on status.company.com. "
            "We announce planned maintenance at least 48 hours in advance."
        ),
    },
    {
        "ticket_id": "T069",
        "text": "Do you offer reseller or agency pricing?",
        "expected_category": "general",
        "expected_priority": "low",
        "reference_reply": (
            "Yes! We have a reseller program with 20-40% volume discounts. "
            "Apply at company.com/partners."
        ),
    },
    {
        "ticket_id": "T070",
        "text": "Is there a community forum where I can ask questions?",
        "expected_category": "general",
        "expected_priority": "low",
        "reference_reply": (
            "Yes! Join our community forum at community.company.com. "
            "You can also attend weekly live webinars at company.com/webinars."
        ),
    },
    {
        "ticket_id": "T071",
        "text": "Do you support HIPAA for healthcare customers?",
        "expected_category": "general",
        "expected_priority": "medium",
        "reference_reply": (
            "HIPAA BAA is available for qualifying Enterprise customers. "
            "Contact sales@company.com to discuss HIPAA requirements."
        ),
    },
    {
        "ticket_id": "T072",
        "text": "Where can I find tutorials and documentation?",
        "expected_category": "general",
        "expected_priority": "low",
        "reference_reply": (
            "Documentation, tutorials, and video guides are available at help.company.com "
            "and docs.company.com. Our certification program is at company.com/certifications."
        ),
    },
    {
        "ticket_id": "T073",
        "text": "I want to schedule an onboarding call with your team.",
        "expected_category": "general",
        "expected_priority": "low",
        "reference_reply": (
            "Schedule a free 30-minute onboarding call through the Help Center. "
            "Our success team will walk you through core features tailored to your use case."
        ),
    },
    {
        "ticket_id": "T074",
        "text": "How is my data protected?",
        "expected_category": "general",
        "expected_priority": "low",
        "reference_reply": (
            "We encrypt data at rest and in transit (TLS 1.2+). "
            "We are SOC 2 Type II and ISO 27001 certified. Full security details: company.com/security."
        ),
    },
    {
        "ticket_id": "T075",
        "text": "Your service has been down for 3 hours and no one is responding!",
        "expected_category": "general",
        "expected_priority": "high",
        "reference_reply": (
            "We sincerely apologize for this disruption. Our team is actively investigating. "
            "Follow live updates on status.company.com. We are committed to resolving this as fast as possible."
        ),
    },
    {
        "ticket_id": "T076",
        "text": "Is there live chat support available?",
        "expected_category": "general",
        "expected_priority": "low",
        "reference_reply": (
            "Yes, live chat is available Monday to Friday, 9 AM – 6 PM UTC. "
            "You can also reach us by email at support@company.com or via a Help Center ticket."
        ),
    },
    {
        "ticket_id": "T077",
        "text": "Does the product meet WCAG accessibility standards?",
        "expected_category": "general",
        "expected_priority": "low",
        "reference_reply": (
            "Yes, our product meets WCAG 2.1 AA accessibility standards. "
            "For accessibility-related concerns, contact support@company.com."
        ),
    },
    {
        "ticket_id": "T078",
        "text": "I'm a developer building on your platform. Where do I start?",
        "expected_category": "general",
        "expected_priority": "low",
        "reference_reply": (
            "Start with the developer documentation at docs.company.com/api. "
            "Join the developer community at community.company.com and explore SDK quickstarts."
        ),
    },
    {
        "ticket_id": "T079",
        "text": "When will the next maintenance window be?",
        "expected_category": "general",
        "expected_priority": "low",
        "reference_reply": (
            "Planned maintenance is announced at least 48 hours in advance on status.company.com. "
            "Subscribe to notifications to receive advance warnings."
        ),
    },
    {
        "ticket_id": "T080",
        "text": "What are your support hours?",
        "expected_category": "general",
        "expected_priority": "low",
        "reference_reply": (
            "Live chat and email support run Monday to Friday, 9 AM – 6 PM UTC. "
            "Enterprise customers have 24/7 support for critical issues."
        ),
    },
]
