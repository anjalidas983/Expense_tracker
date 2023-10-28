from django.shortcuts import render
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveUpdateDestroyAPIView,ListCreateAPIView
from . serializers import ExpenseSerializer,TotalExpenseSerializer,CategorySerializer
from .models import Expense,Category
from rest_framework.views import APIView
from datetime import datetime
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework  import status
from django.db.models.functions import ExtractMonth,ExtractYear
from django.http import JsonResponse

# Create your views here.


class AddExpenseView(CreateAPIView):
    serializer_class = ExpenseSerializer
    queryset =Expense.objects.all()

class RecentTransactionList(ListAPIView):
    queryset=Expense.objects.order_by('-date')[:10]
    serializer_class=ExpenseSerializer
class ExpenseDetail(RetrieveUpdateDestroyAPIView):
    serializer_class=ExpenseSerializer
    queryset=Expense.objects.all()



class AddCategoryView(CreateAPIView):
    serializer_class=CategorySerializer
    queryset=Category.objects.all()

class TotalExpenseView(APIView):
    def get(self,request):
        today=datetime.today()
        start_of_month=today.replace(day=1)
        end_of_month=today.replace(day=1,month=1,year=today.year+1) if today.month==12 else  today.replace(day=1,month=today.month+1)
        total_amount=Expense.objects.filter(date__gte=start_of_month,date__lt=end_of_month).aggregate(total=Sum('amount'))['total']
        if total_amount is None:
            total_amount=0
        else:
            total_amount = total_amount
        response_data={'total_expense':total_amount}
        serializer=TotalExpenseSerializer(response_data)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

class TotalExpenseCategory(APIView):
    def get(self,request):
        today=datetime.today()
        start_of_month=today.replace(day=1)
        end_of_month=today.replace(day=1,year=today.year+1) if today.month==12 else\
              today.replace(day=1,month=today.month+1)
        monthly_category_expense=Expense.objects.filter(date__gte=start_of_month,date__lt=end_of_month)\
            .values('expense_category__category_type').annotate(total_expense=Sum('amount')) 
        return Response(monthly_category_expense,status=status.HTTP_200_OK)


class ExpenseListCreateView(ListCreateAPIView):
    queryset=Expense.objects.all()
    serializer_class=ExpenseSerializer

 
       
class ExpenseListYearly(APIView):
    def get(self, request, year):
        year = int(year)  # Ensure year is an integer
        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31)

        # Filter expenses for the specified year
        expenses = Expense.objects.filter(date__gte=start_date, date__lte=end_date)

        # Define a dictionary to store monthly expenses by category
        monthly_expenses = {month: {} for month in range(1, 13)}

        # Calculate monthly expenses by category
        for expense in expenses:
            month = expense.date.month
            category = expense.expense_category.category_type
            amount = expense.amount

            if category not in monthly_expenses[month]:
                monthly_expenses[month][category] = 0

            monthly_expenses[month][category] += amount

        return Response(monthly_expenses)