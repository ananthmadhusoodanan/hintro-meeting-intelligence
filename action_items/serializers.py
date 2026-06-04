from rest_framework import serializers
from .models import ActionItem


class ActionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionItem
        fields = [
            'id', 'meeting', 'task', 'assignee', 'due_date',
            'status', 'citations', 'reminder_sent',
            'last_reminded_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'reminder_sent', 'last_reminded_at', 'created_at', 'updated_at']

    def validate_assignee(self, value):
        serializers.EmailField().run_validation(value)
        return value

    def validate_status(self, value):
        valid = ['PENDING', 'IN_PROGRESS', 'COMPLETED']
        if value not in valid:
            raise serializers.ValidationError(f"Status must be one of: {valid}")
        return value


class ActionItemStatusSerializer(serializers.Serializer):
    """Only used for PATCH status update"""
    status = serializers.ChoiceField(choices=['PENDING', 'IN_PROGRESS', 'COMPLETED'])
    