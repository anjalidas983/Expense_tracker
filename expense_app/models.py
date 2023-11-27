from django.db import models
from django.utils import timezone
import datetime
from authentication.models import CustomUser
# Create your models here.
class Category(models.Model):
    category_type=models.CharField(max_length=300)

    def __str__(self):
        return f"{self.category_type}"

class Expense(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    expense_name=models.CharField(max_length=500)
    amount=models.FloatField()
    expense_category=models.ForeignKey(Category,on_delete=models.CASCADE)
    date=models.DateField(default=timezone.now)

    def __str__(self):
        return self.expanse_name