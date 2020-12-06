from .models import House, Dishwasher, FinePeriod
from rest_framework import serializers


class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = "__all__"
        depth = 1


class DishwasherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dishwasher
        fields = "__all__"
        depth = 1


class FinePeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinePeriod
        fields = "__all__"
        depth = 1