from .serializers import HouseSerializer, DishwasherSerializer, FinePeriodSerializer
from .models import House, Dishwasher, FinePeriod
from rest_framework import viewsets


class HouseViewSet(viewsets.ModelViewSet):
    queryset = House.houses.all()
    serializer_class = HouseSerializer


class DishwasherViewSet(viewsets.ModelViewSet):
    queryset = Dishwasher.dishwashers.all()
    serializer_class = DishwasherSerializer


class FinePeriodViewSet(viewsets.ModelViewSet):
    queryset = FinePeriod.fine_periods.all()
    serializer_class = FinePeriodSerializer
