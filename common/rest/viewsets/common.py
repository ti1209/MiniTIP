from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class UpdateOnlyModelViewSet(mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             GenericViewSet):
    """
    A viewset that provides default `retrieve()` and `update()` actions.
    """
    pass
