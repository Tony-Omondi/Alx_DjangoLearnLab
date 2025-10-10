from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .models import Notification
from .serializers import NotificationSerializer

class NotificationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Mark notifications as read
        Notification.objects.filter(recipient=request.user, unread=True).update(unread=False)
        return Response({'message': 'Notifications marked as read'}, status=200)