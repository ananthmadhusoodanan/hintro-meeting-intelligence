from rest_framework import serializers
from .models import Meeting


class TranscriptSegmentSerializer(serializers.Serializer):
    """Validates each segment in the transcript array"""
    timestamp = serializers.CharField()
    speaker = serializers.CharField()
    text = serializers.CharField()


class MeetingSerializer(serializers.ModelSerializer):
    # Validate transcript is a proper list of segments
    transcript = TranscriptSegmentSerializer(many=True)

    class Meta:
        model = Meeting
        fields = [
            'id', 'title', 'participants', 'meeting_date',
            'transcript', 'analysis', 'created_at', 'updated_at'
        ]
        # These fields are set automatically, not by the user
        read_only_fields = ['id', 'analysis', 'created_at', 'updated_at']

    def validate_participants(self, value):
        """Make sure participants is a non-empty list of valid emails"""
        if not value:
            raise serializers.ValidationError("At least one participant is required.")
        for email in value:
            serializers.EmailField().run_validation(email)
        return value

    def validate_transcript(self, value):
        """Make sure transcript is not empty"""
        if not value:
            raise serializers.ValidationError("Transcript cannot be empty.")
        return value


class MeetingListSerializer(serializers.ModelSerializer):
    """Lighter serializer for list view — no full transcript"""
    class Meta:
        model = Meeting
        fields = ['id', 'title', 'participants', 'meeting_date', 'created_at']