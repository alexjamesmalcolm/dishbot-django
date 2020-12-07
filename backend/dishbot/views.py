from .serializers import HouseSerializer, DishwasherSerializer, FinePeriodSerializer
from .models import House, Dishwasher, FinePeriod
from rest_framework import viewsets
from permissions import IsOwner


class HouseViewSet(viewsets.ModelViewSet):
    queryset = House.houses.all()
    serializer_class = HouseSerializer
    permission_classes = [IsOwner]


class DishwasherViewSet(viewsets.ModelViewSet):
    queryset = Dishwasher.dishwashers.all()
    serializer_class = DishwasherSerializer
    permission_classes = [IsOwner]


class FinePeriodViewSet(viewsets.ModelViewSet):
    queryset = FinePeriod.fine_periods.all()
    serializer_class = FinePeriodSerializer
    permission_classes = [IsOwner]
