from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
import logging

from .models import Meeting
from .serializers import MeetingSerializer, MeetingListSerializer
from .services.ai_service import analyze_transcript

logger = logging.getLogger(__name__)


class MeetingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MeetingSerializer

    def get_queryset(self):
        return Meeting.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return MeetingListSerializer
        return MeetingSerializer

    def list(self, request):
        """GET /api/meetings/"""
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(self._success(serializer.data))
        serializer = self.get_serializer(queryset, many=True)
        return Response(self._success(serializer.data))

    def create(self, request):
        """POST /api/meetings/"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        meeting = serializer.save()
        return Response(
            self._success(MeetingSerializer(meeting).data),
            status=status.HTTP_201_CREATED
        )

    def retrieve(self, request, pk=None):
        """GET /api/meetings/:id/"""
        meeting = get_object_or_404(Meeting, pk=pk)
        serializer = self.get_serializer(meeting)
        return Response(self._success(serializer.data))

    @action(detail=True, methods=['post'], url_path='analyze')
    def analyze(self, request, pk=None):
        """POST /api/meetings/:id/analyze"""
        meeting = get_object_or_404(Meeting, pk=pk)

        # Don't re-analyze if already done (save API costs)
        if meeting.analysis:
            return Response(self._success(meeting.analysis))

        logger.info(f"[{request.trace_id}] Analyzing meeting {meeting.id}")

        try:
            analysis = analyze_transcript(
                transcript=meeting.transcript,
                participants=meeting.participants
            )

            # Save analysis back to the meeting
            meeting.analysis = analysis
            meeting.save()

            # Auto-create ActionItem records from AI output
            # We import here to avoid circular imports
            from action_items.models import ActionItem
            for item in analysis.get('actionItems', []):
                ActionItem.objects.create(
                    meeting=meeting,
                    task=item['task'],
                    assignee=item.get('assignee', ''),
                    citations=item.get('citations', [])
                )

            logger.info(
                f"[{request.trace_id}] Analysis complete for meeting {meeting.id} "
                f"— {len(analysis.get('actionItems', []))} action items created"
            )

            return Response(self._success(analysis))

        except Exception as e:
            logger.error(f"[{request.trace_id}] AI analysis failed: {str(e)}")
            return Response(
                {
                    "traceId": request.trace_id,
                    "success": False,
                    "error": {
                        "code": "AI_ANALYSIS_FAILED",
                        "message": f"Analysis failed: {str(e)}"
                    }
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _success(self, data):
        return {
            "traceId": getattr(self.request, 'trace_id', None),
            "success": True,
            "data": data
        }