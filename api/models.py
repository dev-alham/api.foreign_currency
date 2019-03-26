from django.db import models
from django.utils import timezone

DB_PREFIX = 'foreign_currency_'

# Create your models here.

class CreateAt(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    class Meta:
        abstract = True

class UpdateAt(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Setting(models.Model):
    is_maintenance = models.BooleanField(default=0)
    class Meta:
        db_table = DB_PREFIX + 'setting'

class ExchangeRate(CreateAt, UpdateAt):
    from_rate = models.CharField(max_length=50)
    to_rate = models.CharField(max_length=50)
    on_delete = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = DB_PREFIX + 'exchange_rate'
        unique_together = (
            ("from_rate", "to_rate"),
        )
        index_together = [
            ["from_rate", "to_rate", "on_delete"],
            ["on_delete"]
        ]

    def __str__(self):
        return str(self.id)

class ExchangeRateLog(CreateAt):
    date_rate = models.DateField(default=timezone.now)
    exchange_rate = models.ForeignKey(
        ExchangeRate,
        to_field = 'id',
        on_delete=models.CASCADE,
        unique=False,
    )
    rate = models.FloatField(max_length=100)

    @property
    def from_rate(self):
        return self.exchange_rate.from_rate

    @property
    def to_rate(self):
        return self.exchange_rate.to_rate

    class Meta:
        db_table = DB_PREFIX + 'exchange_rate_log'
        unique_together = (
            ("exchange_rate", 'date_rate'),
        )


