from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class PrivacyPolicyView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "title": "Privacy Policy",
            "last_updated": "2025-05-20",
            "content": [
                {
                    "heading": "1. Information We Collect",
                    "subsections": [
                        {
                            "subheading": "a. Information You Provide to Us",
                            "items": [
                                "Account Information: When you register, we collect your email address and password.",
                                "Profile Information: You may provide additional information such as your name or contact details.",
                                "Support Requests: When you submit a support ticket, we collect the information you provide, including any attachments.",
                                "Subscription and Billing: If you purchase a subscription, we collect payment and billing information via our payment processor.",
                            ]
                        },
                        {
                            "subheading": "b. Information Collected Automatically",
                            "items": [
                                "Usage Data: We collect information about your interactions with the Service, such as pages visited, features used, and actions taken.",
                                "Device and Log Data: We may collect information about your device, browser type, IP address, and access times.",
                                "Cookies and Tracking Technologies: We use cookies and similar technologies to enhance your experience and analyze usage.",
                            ]
                        }
                    ]
                },
                {
                    "heading": "2. How We Use Your Information",
                    "items": [
                        "Provide, operate, and maintain the Service",
                        "Process your registration and manage your account",
                        "Process payments and manage subscriptions",
                        "Respond to your support requests and feedback",
                        "Improve and personalize the Service",
                        "Communicate with you about updates, offers, and important notices",
                        "Ensure the security and integrity of the Service",
                        "Comply with legal obligations",
                    ]
                },
                {
                    "heading": "3. How We Share Your Information",
                    "items": [
                        "Service Providers: Third-party vendors who help us operate the Service (e.g., payment processors, hosting providers, analytics).",
                        "Legal Requirements: If required by law or to protect our rights, we may disclose your information to authorities.",
                        "Business Transfers: In the event of a merger, acquisition, or sale of assets, your information may be transferred.",
                        "We do not sell your personal information to third parties.",
                    ]
                },
                {
                    "heading": "4. Data Security",
                    "text": "We implement reasonable security measures to protect your information. However, no method of transmission over the Internet or electronic storage is 100% secure."
                },
                {
                    "heading": "5. Your Rights and Choices",
                    "text": "Depending on your location, you may have the right to access, update, or delete your personal information; object to or restrict certain processing; withdraw consent where processing is based on consent. To exercise your rights, please contact us at support@example.com."
                },
                {
                    "heading": "6. Data Retention",
                    "text": "We retain your information as long as your account is active or as needed to provide the Service, comply with legal obligations, resolve disputes, and enforce agreements."
                },
                {
                    "heading": "7. Children’s Privacy",
                    "text": "Our Service is not intended for children under 16. We do not knowingly collect personal information from children."
                },
                {
                    "heading": "8. Changes to This Policy",
                    "text": "We may update this Privacy Policy from time to time. We will notify you of any material changes by posting the new policy on this page."
                },
                {
                    "heading": "9. Contact Us",
                    "text": "If you have any questions about this Privacy Policy, please contact us at support@example.com."
                },
            ]
        })


class TermsOfServiceView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "title": "Terms of Service",
            "effective_date": "2025-05-20",
            "content": [
                {
                    "heading": "1. Acceptance of Terms",
                    "text": (
                        "By accessing or using our Service, you agree to be bound by these "
                        "Terms of Service and our Privacy Policy. If you do not agree, you "
                        "may not use the Service."
                    )
                },
                {
                    "heading": "2. Description of Service",
                    "text": (
                        "Our Service provides a cloud-based platform for managing subscriptions, "
                        "user accounts, and support tickets. We may update or modify the Service at any time."
                    )
                },
                {
                    "heading": "3. User Accounts",
                    "text": (
                        "You must register for an account to access certain features. You are "
                        "responsible for maintaining the confidentiality of your account credentials "
                        "and for all activities that occur under your account."
                    )
                },
                {
                    "heading": "4. Subscription and Payment",
                    "text": (
                        "Some features require a paid subscription. By subscribing, you agree to "
                        "pay all applicable fees. Subscriptions renew automatically unless canceled. "
                        "You may cancel at any time, but payments are non-refundable except as required by law."
                    )
                },
                {
                    "heading": "5. User Conduct",
                    "items": [
                        "Violating any laws or regulations",
                        "Infringing intellectual property rights",
                        "Transmitting harmful or malicious content",
                        "Attempting to gain unauthorized access to the Service"
                    ]
                },
                {
                    "heading": "6. Support and Ticket System",
                    "text": (
                        "You may submit support requests or report issues through our support ticket "
                        "system. We strive to respond promptly but do not guarantee specific response times."
                    )
                },
                {
                    "heading": "7. Intellectual Property",
                    "text": (
                        "All content, trademarks, and software associated with the Service are the "
                        "property of the Company or its licensors. You may not copy, modify, or distribute "
                        "any part of the Service without our written consent."
                    )
                },
                {
                    "heading": "8. Termination",
                    "text": (
                        "We may suspend or terminate your access to the Service at our discretion, "
                        "including for violation of these Terms. You may also close your account at any time."
                    )
                },
                {
                    "heading": "9. Disclaimers",
                    "text": (
                        "The Service is provided “as is” and “as available.” We make no warranties "
                        "regarding the Service’s availability, reliability, or suitability for your purposes."
                    )
                },
                {
                    "heading": "10. Limitation of Liability",
                    "text": (
                        "To the maximum extent permitted by law, the Company is not liable for any "
                        "indirect, incidental, or consequential damages arising from your use of the Service."
                    )
                },
                {
                    "heading": "11. Changes to Terms",
                    "text": (
                        "We may update these Terms from time to time. We will notify you of material "
                        "changes by posting the new Terms on this page. Continued use of the Service "
                        "constitutes acceptance of the updated Terms."
                    )
                },
                {
                    "heading": "12. Governing Law",
                    "text": (
                        "These Terms are governed by the laws of [Your Jurisdiction], without regard "
                        "to its conflict of law principles."
                    )
                },
                {
                    "heading": "13. Contact Us",
                    "text": (
                        "If you have any questions about these Terms, please contact us at "
                        "[support@example.com]."
                    )
                },
            ]
        })
