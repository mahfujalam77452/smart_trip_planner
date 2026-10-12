from django.db import models
from django.db.models import F,Q
from django.core.exceptions import ValidationError

# Create your models here.

class Trip(models.Model):

    class Status(models.TextChoices):
        PLANNED="PLANNED","Planned"
        OPEN = "OPEN","Open"
        ONGOING="ONGOING","Ongoing"
        COMPLETE="COMPLETE","Complete"

    destination = models.CharField(max_length=150)

    start_date = models.DateField()
    end_date = models.DateField()

    budget = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    max_travelers = models.PositiveIntegerField()
    current_travelers = models.PositiveIntegerField(default=0)

    expense = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PLANNED,
        db_index=True
    )

    notes = models.CharField(
        max_length = 100,
        null=True
    )

    class Meta:

        ordering = ["start_date","id"]

        constraints = [
            models.CheckConstraint(
               condition=Q(max_travelers__gt=0),
               name = "trip_max_travelers_positive",
            ),

            models.CheckConstraint(
                condition=Q(
                    current_travelers__lte=F("max_travelers")
                ),
                name="trip_travelers_within_capacity",
            ),

            models.CheckConstraint(
                condition=Q(expense__gte=0),
                name="trip_expenses_nonnegative",
            ),

            models.CheckConstraint(
                condition=Q(end_date__gte=F("start_date")),
                name="trip_end_after_start",
            )
        ]

    def clean(self):
        super().clean()

        errors = {}

        if self.start_date and self.end_date:

            if self.end_date < self.start_date:
                errors["end_date"] = (
                    "End date cannot be be before start date."
                )

        if (
            self.max_travelers is not None
            and self.max_travelers <= 0
        ):
            errors["max_travelers"] = (
                "Maximum travelers must be greater than zero"
            )

        if (
            self.max_travelers is not None
            and self.current_travelers is not None
            and self.current_travelers > self.max_travelers
        ):
            errors["current_travelers"] = (
                "Current travelers cannot exceed capacity"
            )

        if errors:

            raise ValidationError(errors)
    def __str__(self):
        return f"{self.destination} - {self.start_date}"


class Traveler(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    trips = models.ManyToManyField(
        Trip,
        through="TripMembership",
        related_name="travelers",
        blank=True,
    )

    def __str__(self):
        return self.name


class TripMembership(models.Model):

    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name="memberships"
    )


    traveler = models.ForeignKey(
        Traveler,
        on_delete=models.CASCADE,
        related_name="memberships"
    )

    joined_at = models.DateTimeField(auto_now_add = True)

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields = ["trip","traveler"],
                name="unique_trip_traveler",
            )
        ]
    def __str__(self):
        return f"{self.traveler} - {self.trip}"

class Expense(models.Model):
    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name="expense_items"
    )

    description = models.CharField(max_length=200)

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

        constraints = [
            models.CheckConstraint(
                condition=Q(amount__gt=0),
                name="expense_amount_positive"
            )
        ]

    def __str__(self):
        return f"{self.description} - {self.amount}"

