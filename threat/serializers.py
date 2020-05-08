from rest_framework import serializers

from threat.models import Threat


# 데이터 형태 정의하는 곳
class ThreatSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(
    #     source='tenant_id',
    #     required=True
    # )
    # tenant_name = serializers.CharField(
    #     label='테넌트', source='tenant.tenant_name'
    # source를 사용하는 경우 = viewset에 정의 안한 경우
    # )

    sha256 = serializers.CharField(
        label='SHA256'
    )

    reason = serializers.CharField(
        label='분석 결과'
    )

    # total_device = serializers.IntegerField(
    #     label='발견된 디바이스'
    # )

    # first_found = serializers.DateTimeField(
    #     label='최초 발견 날짜'
    # )
    #
    # last_found = serializers.DateTimeField(
    #     label='마지막 발견 날짜'
    # )

    # 실제 정의하는 곳
    class Meta:
        model = Threat
        fields = (
            'id',
            # 'tenant_name',
            'sha256',
            'reason',
            'classification',
            'sub_classification',
            # 'total_device',
            'cylance_score',
            # 'first_found',
            # 'last_found',
            'detected_by',
            'name'
        )