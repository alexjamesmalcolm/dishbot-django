import operator
from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.query_utils import Q
from datetime import timedelta


class House(models.Model):
    houses = models.Manager()
    name = models.CharField(max_length=128)
    are_dishwashers_skipped = models.BooleanField()

    def __str__(self):
        return self.name


class Dishwasher(models.Model):
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

        super(Dishwasher, self).save(*args, **kwargs)

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


class FinePeriod(models.Model):
    fine_periods = models.Manager()
    house = models.ForeignKey(
        "House", on_delete=models.CASCADE, related_name="fine_periods"
    )
    order = models.IntegerField()
    duration = models.DurationField(default=timedelta(days=1))
    fine_amount = models.DecimalField(max_digits=6, decimal_places=2)

    def save(self, *args, **kwargs):
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

        super(FinePeriod, self).save(*args, **kwargs)

    class Meta:
        constraints = [
            UniqueConstraint(
                name="no two fines can have the same order per house",
                fields=["house", "order"],
            )
        ]
