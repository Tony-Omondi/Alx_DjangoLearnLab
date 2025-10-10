from rest_framework import serializers
from .models import Notification
from accounts.serializers import UserSerializer

class NotificationSerializer(serializers.ModelSerializer):
    actor = UserSerializer(read_only=True)
    target = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'verb', 'target', 'timestamp', 'unread']
        read_only_fields = ['recipient', 'actor', 'timestamp', 'unread']

    def get_target(self, obj):
        if obj.target:
            return str(obj.target)
        return None