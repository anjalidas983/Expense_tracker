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
from rest_framework.permissions import IsAuthenticated
from calendar import month_name
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters 
 

# Create your views here.

#Adding expense view
class AddExpenseView(CreateAPIView):
    serializer_class = ExpenseSerializer
    queryset =Expense.objects.all()
    permission_classes=[IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




class ExpenseHistoryFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name="date", lookup_expr="gte")
    end_date = filters.DateFilter(field_name="date", lookup_expr="lte")
    category = filters.CharFilter(field_name="expense_category__category_type", lookup_expr="iexact")

    class Meta:
        model = Expense
        fields = []        

#Listing all the expense with pagination and filtering
class ExpenseHistoryView(ListAPIView):
    serializer_class=ExpenseSerializer
    permission_classes=[IsAuthenticated]
    pagination_class=PageNumberPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ExpenseHistoryFilter
 
    def get_queryset(self):
        user=self.request.user
        queryset=Expense.objects.filter(user=user)
        self.pagination_class.page_size = 12
        return queryset

class CategoryListView(ListAPIView):
    serializer_class=CategorySerializer
    queryset=Category.objects.all()
    
#Listing all the recent transactions
class RecentTransactionList(ListAPIView):
    serializer_class=ExpenseSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        user=self.request.user
        queryset=Expense.objects.filter(user=user).order_by('-date')[:8]
        return queryset
#Retrieving deleting and updating particular instance of the expense model
class ExpenseDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class=ExpenseSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
         user=self.request.user
         queryset=Expense.objects.filter(user=user)
         return queryset

class AddCategoryView(CreateAPIView):
    serializer_class=CategorySerializer
    queryset=Category.objects.all()


#Showing the total expense of the current month
class TotalExpenseView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        user=self.request.user
        today=datetime.today()
        start_of_month=today.replace(day=1)
        end_of_month=today.replace(day=1,month=1,year=today.year+1) if today.month==12 else \
                      today.replace(day=1,month=today.month+1)
        total_amount=Expense.objects.filter(user=user,date__gte=start_of_month,date__lt=end_of_month)\
                    .aggregate(total=Sum('amount'))['total']
        if total_amount is None:
            total_amount=0
        else:
            total_amount = total_amount
        response_data={'total_expense':total_amount}
        serializer=TotalExpenseSerializer(response_data)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
#Showing the total expense by category of the current month
class TotalExpenseByCategory(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        user=self.request.user
        today=datetime.today()
        start_of_month=today.replace(day=1)
        end_of_month=today.replace(day=1,year=today.year+1) if today.month==12 else\
              today.replace(day=1,month=today.month+1)
        monthly_category_expense=Expense.objects.filter(user=user,date__gte=start_of_month,date__lt=end_of_month)\
            .values('expense_category__category_type').annotate(total_expense=Sum('amount')) 
        return Response(monthly_category_expense,status=status.HTTP_200_OK)


class ExpenseListCreateView(ListCreateAPIView):
    serializer_class=ExpenseSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        user=self.request.user
        queryset=Expense.objects.filter(user=user)
        return queryset
    
#Showing total expense by each category of each month in a year       
class ExpenseListYearly(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request, year=None):
        user=self.request.user
        if year is None:
            today=datetime.today()
            year=today.year
        year = int(year) 
        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31)

        expenses = Expense.objects.filter(user=user,date__gte=start_date, date__lte=end_date)
        monthly_expenses = {month: {} for month in month_name[1:]}

        # Calculating monthly expenses by category
        for expense in expenses:
            month = expense.date.month
            category = expense.expense_category.category_type
            amount = expense.amount

            if category not in monthly_expenses[month_name[month]]:
                monthly_expenses[month_name[month]][category] = 0

            monthly_expenses[month_name[month]][category] += amount
        return Response(monthly_expenses)


class GetUserEmail(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        user_email=request.user.email
        return Response({'email':user_email},status=status.HTTP_200_OK)

