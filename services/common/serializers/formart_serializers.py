import datetime
import decimal

from django.utils import timezone
from rest_framework import serializers

class FormattedFieldSerializer(serializers.Field):
    """
    Base class for formatting serializer fields.
    """
    formatter = None

    def to_representation(self, value):
        if self.formatter is None:
            raise NotImplementedError("Subclasses must define a 'formatter' method.")
        return self.formatter(value)

    def to_internal_value(self, data):
        return data

class MonetaryFieldSerializer(FormattedFieldSerializer, serializers.DecimalField):
    """
    Serializer for formatting currency to dollars.
    """
    def formatter(self, value):
        """Formats the amount to include the dollar sign and comma separators."""
        amount = decimal.Decimal(value)
        amount = amount.quantize(decimal.Decimal('.01'), rounding=decimal.ROUND_HALF_UP)
        amount_str = '{:,.2f}'.format(amount)
        return '$' + amount_str

class DateFieldSerializer(FormattedFieldSerializer, serializers.DateTimeField):
    """
    Serializer for formatting date and time to a string representation.
    """
    def formatter(self, value):
        """Formats the date and time to a string representation."""
        if isinstance(value, datetime.datetime):
            value = value.astimezone()
        return value.strftime('%b %d %Y at %I:%M %p')


class MaskedFieldSerializer(FormattedFieldSerializer, serializers.CharField):
    """
    Serializer for masking sensitive data.
    """
    def formatter(self, value):
        """Masks sensitive data by replacing all characters with asterisks."""
        return '*' * len(str(value))

class PercentageFieldSerializer(FormattedFieldSerializer, serializers.DecimalField):
    """
    Serializer for formatting decimal values as percentages.
    """
    def formatter(self, value):
        """Formats the decimal value as a percentage."""
        percentage = decimal.Decimal(value) * 100
        return '{:.2f}%'.format(percentage)


class BooleanFieldSerializer(FormattedFieldSerializer, serializers.BooleanField):
    """
    Serializer for formatting boolean values.
    """
    def formatter(self, value):
        """Formats the boolean value as 'True' or 'False'."""
        return 'True' if value else 'False'


class DurationFieldSerializer(FormattedFieldSerializer, serializers.DurationField):
    """
    Serializer for formatting durations.
    """
    def formatter(self, value):
        """Formats the duration in a human-readable format."""
        return str(value)
