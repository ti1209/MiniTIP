from django.db.models import F
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from threat import serializers
from threat.models import Threat


# 출처?
class ThreatViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ThreatSerializer
    queryset = Threat.objects.annotate(
        tenant_name=F('tenant__tenant_name'),
        reason=F('globallist__reason')
    )


class ThreatDashboardViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.ThreatSerializer
    queryset = Threat.objects.annotate(
        reason=F('globallist__reason')
    )

    @action(detail=False, methods=['GET'], name='threat_count')
    def threat_count(self, request):
        threat_count = Threat.objects.count()
        return Response({'threat_count': threat_count})
