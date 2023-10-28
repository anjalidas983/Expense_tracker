from rest_framework import serializers
from . models import Expense,Category
from django.utils import timezone
import datetime

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Expense
        fields = '__all__'

    def validate_amount(self,value):
        if value<0:
            raise serializers.ValidationError('Amount must be a positive value')
        return value
    def validate_date(self,value):
        if value>timezone.now().date():
            raise serializers.ValidationError('Date cannot be in future')
        return value
class TotalExpenseSerializer(serializers.Serializer):
    total_expense=serializers.DecimalField(max_digits=20,decimal_places=2)

