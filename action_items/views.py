from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import ActionItem
from .serializers import ActionItemSerializer, ActionItemStatusSerializer


class ActionItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ActionItemSerializer

    def get_queryset(self):
        queryset = ActionItem.objects.all()

        # Filtering support
        status_filter = self.request.query_params.get('status')
        assignee = self.request.query_params.get('assignee')
        meeting_id = self.request.query_params.get('meeting_id')

        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if assignee:
            queryset = queryset.filter(assignee=assignee)
        if meeting_id:
            queryset = queryset.filter(meeting_id=meeting_id)

        return queryset

    def list(self, request):
        """GET /api/action-items/"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(self._success(serializer.data))

    def create(self, request):
        """POST /api/action-items/"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = serializer.save()
        return Response(
            self._success(ActionItemSerializer(item).data),
            status=status.HTTP_201_CREATED
        )

    def retrieve(self, request, pk=None):
        """GET /api/action-items/:id/"""
        item = get_object_or_404(ActionItem, pk=pk)
        serializer = self.get_serializer(item)
        return Response(self._success(serializer.data))

    @action(detail=True, methods=['patch'], url_path='status')
    def update_status(self, request, pk=None):
        """PATCH /api/action-items/:id/status/"""
        item = get_object_or_404(ActionItem, pk=pk)
        serializer = ActionItemStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item.status = serializer.validated_data['status']
        item.save()
        return Response(self._success(ActionItemSerializer(item).data))

    @action(detail=False, methods=['get'], url_path='overdue')
    def overdue(self, request):
        """GET /api/action-items/overdue/"""
        now = timezone.now()
        overdue_items = ActionItem.objects.filter(
            due_date__lt=now
        ).exclude(status='COMPLETED')
        serializer = self.get_serializer(overdue_items, many=True)
        return Response(self._success(serializer.data))

    def _success(self, data):
        return {
            "traceId": getattr(self.request, 'trace_id', None),
            "success": True,
            "data": data
        }