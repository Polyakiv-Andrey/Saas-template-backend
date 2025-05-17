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

