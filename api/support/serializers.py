from rest_framework import serializers

from api.support.models import SupportTicket


class SupportTicketWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = SupportTicket
        fields = ["title", "description", 'image']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['created_by'] = user.email if user and user.email else 'anonim@n.com'
        validated_data['reported_by'] = user
        return super().create(validated_data)


class SupportTicketReadSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    reported_by_email = serializers.SerializerMethodField()

    class Meta:
        model = SupportTicket
        fields = [
            "id",
            "title",
            "description",
            "image_url",
            "status",
            "created_at",
            "updated_at",
            "resolved_at",
            "reported_by_email"
        ]
        read_only_fields = fields

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None

    def get_reported_by_email(self, obj):
        return obj.reported_by.email if obj.reported_by else None