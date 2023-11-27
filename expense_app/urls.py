from django.urls import path
from .views import AddExpenseView,RecentTransactionList,ExpenseDetailView,TotalExpenseView,\
    AddCategoryView,TotalExpenseByCategory,ExpenseListCreateView,ExpenseListYearly,\
    CategoryListView,ExpenseHistoryView,GetUserEmail
app_name='expense_app'


urlpatterns = [
    path('add-expense',AddExpenseView.as_view(),name='add-expense'),
    path('expense-history/',ExpenseHistoryView.as_view(),name='expense-history'),
    path('recent-transactions',RecentTransactionList.as_view(),name='recent-transactions'),
    path('expense-detail/<int:pk>/',ExpenseDetailView.as_view(),name='expense-detail'),
    path('total-expense',TotalExpenseView.as_view(),name='total-expense'),
    path('add-category',AddCategoryView.as_view(),name='add-category'),
    path('monthly-category-expense',TotalExpenseByCategory.as_view(),name='category-expense'),
    path('total-expense-list',ExpenseListCreateView.as_view(),name='total-expense-list'),
    path('category-list',CategoryListView.as_view(),name='category-list'),
    path('monthly-expense-category-yearly/<int:year>/',ExpenseListYearly.as_view(),name='yearly_expense_by_category'),
    path('get-user-email',GetUserEmail.as_view(),name='user-email'),
]