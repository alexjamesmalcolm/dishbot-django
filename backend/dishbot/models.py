import operator
from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.manager import Manager
from django.db.models.query_utils import Q
from datetime import timedelta
from utils import request_current_user
from .abstract_models import OwnedByGroupMeUser, BaseModel


class GroupMeUser(BaseModel):
    users = Manager()
    name = models.CharField(max_length=64)
    group_me_id = models.CharField(max_length=32)
    token = models.CharField(max_length=32)

    def __str__(self):
        return self.name

    @property
    def is_authenticated(self):
        response = request_current_user(self.token)
        return response["meta"]["code"] == 200


class House(OwnedByGroupMeUser):
    houses = models.Manager()
    name = models.CharField(max_length=128)
    do_fine_periods_loop = models.BooleanField()

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            UniqueConstraint(
                name="unique house names per user", fields=["owned_by", "name"]
            )
        ]


class Dishwasher(OwnedByGroupMeUser):
    dishwashers = models.Manager()
    name = models.CharField(max_length=64)
    order = models.IntegerField()
    house = models.ForeignKey(
        "House", on_delete=models.CASCADE, related_name="dishwashers"
    )
    is_current_dishwasher = models.BooleanField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_current_dishwasher:
            self.house.dishwashers.exclude(id=self.id).filter(
                is_current_dishwasher=True
            ).update(is_current_dishwasher=False)
        else:
            self.is_current_dishwasher = (
                not self.house.dishwashers.exclude(id=self.id)
                .filter(is_current_dishwasher=True)
                .exists()
            )

        super(Dishwasher, self).save(*args, **kwargs)

        dishwashers = list(self.house.dishwashers.all())
        for dishwasher in dishwashers:
            if dishwasher.id is self.id:
                dishwasher.order = self.order

        dishwashers = sorted(dishwashers, key=operator.attrgetter("order"))
        for num, dishwasher in enumerate(dishwashers, start=1):
            dishwasher.order = num
            if dishwasher.id is self.id:
                self.order = num

        self.house.dishwashers.bulk_update(dishwashers, fields=["order"])

    class Meta:
        constraints = [
            UniqueConstraint(
                name="no two dishwashers can have the same order per house",
                fields=["house", "order"],
            ),
            UniqueConstraint(
                name="only one dishwasher can be current per house",
                fields=["house", "is_current_dishwasher"],
                condition=Q(is_current_dishwasher=True),
            ),
        ]


class FinePeriod(OwnedByGroupMeUser):
    fine_periods = models.Manager()
    house = models.ForeignKey(
        "House", on_delete=models.CASCADE, related_name="fine_periods"
    )
    order = models.IntegerField()
    duration = models.DurationField(default=timedelta(days=1))
    fine_amount = models.DecimalField(max_digits=6, decimal_places=2)
    is_current_fine_period = models.BooleanField()

    def save(self, *args, **kwargs):
        if self.is_current_fine_period:
            self.house.fine_periods.exclude(id=self.id).filter(
                is_current_fine_period=True
            ).update(is_current_fine_period=False)
        else:
            self.is_current_fine_period = (
                not self.house.fine_periods.exclude(id=self.id)
                .filter(is_current_fine_period=True)
                .exists()
            )

        super(FinePeriod, self).save(*args, **kwargs)

        fine_periods = list(self.house.fine_periods.all())
        for fine_period in fine_periods:
            if fine_period.id is self.id:
                fine_period.order = self.order

        fine_periods = sorted(fine_periods, key=operator.attrgetter("order"))
        for num, fine_period in enumerate(fine_periods, start=1):
            fine_period.order = num
            if fine_period.id is self.id:
                self.order = num

        self.house.fine_periods.bulk_update(fine_periods, fields=["order"])

    class Meta:
        constraints = [
            UniqueConstraint(
                name="no two fines can have the same order per house",
                fields=["house", "order"],
            ),
            UniqueConstraint(
                name="only one fine period can be current per house",
                fields=["house", "is_current_fine_period"],
                condition=Q(is_current_fine_period=True),
            ),
        ]
