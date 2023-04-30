from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# app_name = 'loan'

urlpatterns = [
    path('login/', views.loginUser, name="loginpage"),
    # path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='loginpage'),
    path('logout/', views.logoutUser, name="logoutpage"),
    path('register/', views.registerUser, name="registerpage"),
    
    path('', views.home, name='home'),
    
    path('profile/', views.profiles, name="profile"),
    path('create-profile/', views.createProfile, name="create-profile"),
    path('admin-profile/', views.admin_profile, name="admin-profile"),
    path('update-profile/', views.updateProfile, name="update-profile"),
    path('delete-profile/<str:pk>/', views.deleteProfile, name="delete-profile"),
    
    path('loan_details/', views.loan_details, name="loan-details"),
    path('create-loan/', views.createLoan, name="create-loan"),
    path('update-loan/<int:pk>', views.updateLoan, name="update-loan"),
    path('delete-loan/<str:pk>', views.deleteLoan, name="delete-loan"),
    
    path('transactions/', views.transactions, name="transactions"),
    path('create-transaction/', views.createTransaction, name="create-transaction"),
    # path('update-transaction/<int:pk>/', views.edit_transaction, name="update-transaction"),
    path('delete-transaction/<str:pk>/', views.deleteTransaction, name="delete-transaction"),
    
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('repay-loan/<int:loan_id>/', views.repay_loan, name='repay_loan'),
    path('update-repayloan/<int:loan_id>/<int:repayment_id>/', views.edit_repayment, name="edit-repay"),
    path('loan/<int:pk>/transactions/', views.view_loan_transactions, name='view-loan-transactions'),
]