from django.urls import path
from .views import AddExpenseView,RecentTransactionList,ExpenseDetail,TotalExpenseView,AddCategoryView,TotalExpenseCategory,ExpenseListCreateView,ExpenseListYearly
app_name='expense_app'


urlpatterns = [
    path('add-expense',AddExpenseView.as_view(),name='add-expense'),
    path('recent-transactions',RecentTransactionList.as_view(),name='recent-transactions'),
    path('expense-detail/<int:pk>/',ExpenseDetail.as_view(),name='expense-detail'),
    path('total-expense',TotalExpenseView.as_view(),name='total-expense'),
    path('add-category',AddCategoryView.as_view(),name='add-category'),
    path('monthly-category-expense',TotalExpenseCategory.as_view(),name='category-expense'),
    path('total-expense-list',ExpenseListCreateView.as_view(),name='total-expense-list'),
    path('monthly-expense-category-yearly/<int:year>/',ExpenseListYearly.as_view(),name='yearly_expense_by_category'),
    path('monthly-expense-category-yearly',ExpenseListYearly.as_view(),name='yearly_expense_by_category'),

]