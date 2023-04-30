from django.shortcuts import render, HttpResponse
from .forms import CustomUserCreationForm, TransactionForm, EditTransactionForm, LoanForm, EditLoanForm, ProfileForm, LoanRepaymentForm, EditRepaymentForm
from django.db import IntegrityError, transaction
from decimal import Decimal
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Profile, Loan, Transaction, LoanRepayment, LoanUsertransactions
from django.utils import timezone
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse

def registerUser(request):

    form = CustomUserCreationForm()
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.save()
                profile = Profile.objects.create(user_id=user)
                login(request, user)
                return redirect('home')
            except IntegrityError:
                messages.error(request,'Username already exists')
        else:
            messages.error(request,'An error occurred during registration')
    return render(request, 'login_register.html', {'form': form})

def loginUser(request):
    page ='login'
    if request.user.is_authenticated:
         return redirect('home')
    if request.method =="POST":
         username = request.POST.get('username').lower()
         password = request.POST.get('password')
         try:
             user = User.objects.get(username=username)         
         except:
             messages.error(request, "User does not exist!")
        
         user = authenticate(request, username=username, password=password)
        
         if user is not None:
             login(request, user)
             return redirect('home')
         else:
             messages.error(request,"Username or Password is incorrect!")
    context = { 'page': page }
    return render(request, "login_register.html", context)

def logoutUser(request):
    logout(request)
    return redirect('loginpage')




@login_required(login_url="loginpage")
def home(request):
     if request.user.is_superuser:
         loan = Loan.objects.all()[:10]
         transaction = Transaction.objects.all()[:10]
     else:
         loan = Loan.objects.filter(user_id=request.user)[:3]
         transaction = Transaction.objects.filter(loan__user=request.user)[:3]
    
     context = {
         'loan': loan,
         'transaction': transaction,
     }
     return render(request,'home.html', context)



 
@login_required(login_url="loginpage")
def loan_details(request):
     if request.user.is_superuser:
         loan = Loan.objects.all() 
     else:
         loan = Loan.objects.filter(user_id=request.user)
    
     context = {
         'loan': loan,
     }
     return render(request, 'loan_details.html', context)
 
@user_passes_test(lambda u: u.is_superuser)

def createLoan(request):
    if request.method == 'POST':
        form = LoanForm(request.POST)
        try:
            if form.is_valid():
                loan = form.save(commit=False)
                loan.remaining_balance = loan.amount
                loan.save()
                Transaction.objects.create(loan=loan, transaction_type='Debit', transaction_amount=loan.amount)
                return redirect('home')
        except ValidationError:
            # handle the validation error here
            pass
    else:
        form = LoanForm()
    context = {'form': form}
    return render(request, 'create-loan.html', context)

@login_required(login_url="loginpage")
def updateLoan(request, pk):
    loan = get_object_or_404(Loan, pk=pk)
    transaction = loan.transaction_set.first()
    if loan.status == 'paid':
        disabled = True
    else:
        disabled = False

    if request.method == 'POST':
        form = EditLoanForm(request.POST, instance=loan)
        if form.is_valid():
            loan = form.save(commit=False)
            if loan.remaining_balance == 0:
                loan.status = 'paid'
            else:
                loan.status = 'active'
            loan.remaining_balance = loan.amount
            loan.save()

            if transaction:
                transaction.transaction_amount = loan.amount
                transaction.save()
            else:
                Transaction.objects.create(loan=loan, transaction_type='Debit', transaction_amount=loan.amount)

            return redirect('loan-details')
    else:
        form = EditLoanForm(instance=loan)
    context = {'form': form,
               'disabled': disabled,
               'loan': loan}
    # form.fields['user'].disabled = True 
    return render(request, 'edit-loan.html', context)

@login_required(login_url="loginpage")
def deleteLoan(request,pk):
    loan = Loan.objects.get(pk=pk)
    if not request.user.is_superuser:
        return HttpResponse("you are not allowed!")
    if request.method == "POST":
        loan.delete()
        return redirect("loan-details")
    return render(request, "delete.html", {'obj':loan}) 



 


@login_required(login_url="loginpage")
def transactions(request):
     if request.user.is_superuser:
         transaction = Transaction.objects.all() 
     else:
         transaction = Transaction.objects.filter(loan__user_id=request.user)
    
     context = {
         'transaction': transaction,
     }
     return render(request, 'transactions.html', context)

@login_required(login_url="loginpage")
def createTransaction(request):
    if not request.user.is_superuser:
        return HttpResponse("you are not allowed!")
    form = TransactionForm()

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transactions')
    context = {'form': form}
    return render(request, 'create-transaction.html', context)

# @login_required(login_url="loginpage")
# def edit_transaction(request, pk):
#     transaction = get_object_or_404(Transaction,id=pk)
#     loan = transaction.loan 
#     old_amount = transaction.transaction_amount
#     if request.method == 'POST':
#         form = TransactionForm(request.POST, instance=transaction)
#         if form.is_valid():
#             transaction = form.save(commit=False)
#             new_amount = transaction.transaction_amount
#             diff = new_amount - old_amount
#             transaction.save()
            
#             if transaction.transaction_type == 'credit':
#                 loan.balance += diff
#             elif transaction.transaction_type == 'debit':
#                 loan.balance -= diff
#             loan.save()
#             return redirect('transactions')
#     else:
#         form = TransactionForm(instance=transaction)
#     return render(request, 'edit-transaction.html', {'form': form})
# def updateTransaction(request,pk):
#     transaction = Transaction.objects.get(id=pk)
#     form = EditTransactionForm(instance=transaction)
    
    
#     if not request.user.is_superuser:
#         return HttpResponse("you are not allowed!")
    
#     if request.method == 'POST':
#         form = EditTransactionForm(request.POST, instance=transaction)
        
#         if form.is_valid():
#             form.save()
#             return redirect('transactions')
#     else:
#         loan_user = transaction.loan.user.username
#         context = {'form': form,
#                'transaction':transaction,
#                'loan_user': loan_user
#                }
#     return render(request, 'edit-transaction.html', context)

@login_required(login_url="loginpage")
def deleteTransaction(request,pk):
    transaction = Transaction.objects.get(id=pk)
    
    if not request.user.is_superuser:
        return HttpResponse("you are not allowed!")
    if request.method == "POST":
        transaction.delete()
        return redirect("transactions")
    return render(request, "delete.html", {'obj': transaction})

@login_required(login_url="loginpage")
def profiles(request):
    if request.user.is_superuser:
        profile = Profile.objects.all()
    else:
        profile = Profile.objects.filter(user_id=request.user)
    
    context = {
        'profile': profile,
    }
    return render(request,'profile.html', context)

@login_required(login_url="loginpage")
def admin_profile(request):
    
    profile = Profile.objects.filter(user_id=request.user)
    
    context = {
        'profile': profile,
    }
    return render(request,'admin_profile.html', context)


@login_required(login_url="loginpage")
def createProfile(request):
    if not request.user.is_superuser:
        return HttpResponse("you are not allowed!")
    form = ProfileForm()
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('profile')
    context = {'form': form}
    return render(request, 'create_profile.html', context)

@login_required(login_url="loginpage")
def updateProfile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    context = {'form': form}
    return render(request, 'edit-user.html', context)

@login_required(login_url="loginpage")
def deleteProfile(request, pk):
    profile = Profile.objects.get(profile_id=pk)
    if not request.user.is_superuser:
        return HttpResponse("you are not allowed!")
    if request.method == "POST":
        profile.delete()
        return redirect("profile")
    return render(request, "delete.html", {'obj': profile})



@login_required(login_url="loginpage")
def repay_loan(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)
    
    if request.method == 'POST':
        payment_amount = float(request.POST.get('payment_amount', 0))
        payment_mode = request.POST.get('payment_mode', '')
        payment_id = request.POST.get('payment_id', '')
        
        if payment_amount <= 0:
            messages.error(request, 'Payment amount must be greater than 0.')
        elif payment_amount > loan.remaining_balance:
            messages.error(request, 'Payment amount cannot be greater than remaining balance.')
        else:
            payment_amount = Decimal(str(payment_amount))
            loan.remaining_balance -= payment_amount
            loan.balance = loan.amount - loan.remaining_balance
            
            if loan.remaining_balance == 0:
                loan.status = 'paid'
                
            loan.save()
            
            loan_repayment = LoanRepayment.objects.create(
                loan=loan,
                payment_amount=payment_amount
            )
            
            transaction = Transaction.objects.create(
                loan=loan,
                transaction_type='debit',
                transaction_amount=payment_amount,
                payment_mode=payment_mode,
                payment_id=payment_id
            )
            
            messages.success(request, 'Loan repayment added successfully.')
            
            return redirect('transactions')
    
    return render(request, 'repay_loan.html', {'loan': loan})

@login_required(login_url="loginpage")
# def edit_repayment(request, pk):
#     repayment = get_object_or_404(LoanRepayment,pk=7)
#     loan = repayment.loan
    
#     # if loan.id != repayment_id:  # check if loan id is invalid
#     #     raise Http404("Invalid repayment id")
    
#     if request.method == 'POST':
#         form = LoanRepaymentForm(request.POST, instance=repayment)
#         if form.is_valid():
#             payment_amount = form.cleaned_data['payment_amount']
        
#         if payment_amount <= 0:
#             messages.error(request, 'Payment amount must be greater than 0.')
#         elif payment_amount > loan.remaining_balance + repayment.payment_amount:
#             messages.error(request, 'Payment amount cannot be greater than remaining balance plus the previous payment amount.')
#         else:
#             old_amount = repayment.payment_amount
#             repayment.payment_amount = Decimal(str(payment_amount))
#             loan.remaining_balance += old_amount - repayment.payment_amount
#             loan.balance = loan.amount - loan.remaining_balance
            
#             if loan.remaining_balance == 0:
#                 loan.status = 'paid'
                
#             with transaction.atomic():
#                 loan.save()
#                 repayment.save()
#                 Transaction.objects.filter(loan=loan, transaction_type='debit', transaction_amount=old_amount).delete()
#                 Transaction.objects.create(
#                     loan=loan,
#                     transaction_type='debit',
#                     transaction_amount=repayment.payment_amount,
#                     payment_mode=repayment.payment_mode,
#                     payment_id=repayment.payment_id
#                 )
            
#             messages.success(request, 'Loan repayment updated successfully.')
            
#             return redirect('transactions')
    
#     return render(request, 'edit_repayment.html', {'repayment': repayment})

def edit_repayment(request, loan_id, repayment_id):
    loan = get_object_or_404(Loan, pk=loan_id)
    repayment = get_object_or_404(LoanRepayment, pk=repayment_id)

    if request.method == 'POST':
        form = LoanRepaymentForm(request.POST, instance=repayment)
        if form.is_valid():
            # update repayment record
            form.save()

            # update transaction records
            transaction = Transaction.objects.filter(
                loan=loan,
                transaction_time=repayment.payment_date,
                transaction_type='REPAYMENT'
            ).first()
            if transaction:
                transaction.amount = form.cleaned_data['balance']
                transaction.save()

            messages.success(request, 'Repayment has been updated.')
            return redirect('loan-details')
    else:
        form = LoanRepaymentForm(instance=repayment)

    return render(request, 'edit_repayment.html', {'form': form, 'loan': loan, 'repayment': repayment})



def view_loan_transactions(request, loan_id):
    loan = Loan.objects.get(id=loan_id)
    repayments = loan.repayments.all()
    transactions = []
    for repayment in repayments:
        transactions += list(repayment.transactions.all())
    context = {
        'loan': loan,
        'transactions': transactions,
    }
    return render(request, 'loan_transactions.html', context)


def about(request):
    return render(request,'aboutus.html')


def contact(request):
    return render(request,'contactus.html')