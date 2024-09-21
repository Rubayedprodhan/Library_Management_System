from django.forms.forms import BaseForm
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import FormView,CreateView
from django.contrib.auth import login,logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView,LogoutView
from .forms import UserRegistionfrom,DepositForm, ProfileUpdateForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import  update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import  PasswordChangeForm
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from . models import Deposit
def send_transaction_email(user, amount, subject, template):
    message = render_to_string(template, {
        'user': user,
        'amount': amount,
    }) 

    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, 'text/html')
    send_email.send()


class UserRegisterView(FormView):
    template_name = 'account/user_registation.html'
    form_class = UserRegistionfrom
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        user = form.save()
        login(self.request,user)
        messages.success(self.request, 'Registation  Successfully')
        return super().form_valid(form)

class UserLogin(LoginView):
    template_name = 'account/user_loging.html'
    def get_success_url(self):
        messages.success(self.request, 'Login Successfully')
        return reverse_lazy('home')
    
class UserLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            return self.post(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)
    def get_success_url(self):
        messages.success(self.request, 'Logout Successfully')
        return reverse_lazy('home')

    
class PasschangView(LoginRequiredMixin, FormView):
    form_class = PasswordChangeForm
    template_name = 'account/pass_chang.html'
    success_url = reverse_lazy('profile')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, 'Password Updated Successfully')
        send_transaction_email(self.request.user,  "Password Change Message", "transactions/pass_email.html")
        return super().form_valid(form)


class DepositMoneyView(LoginRequiredMixin, CreateView):
    model = Deposit
    form_class = DepositForm  
    template_name = 'account/deposit.html'  
    success_url = reverse_lazy('home')  

    def form_valid(self, form):
        deposit = form.save(commit=False)
        deposit.account = self.request.user.account

        deposit.save()

        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        account.balance += amount  
        account.save(update_fields=['balance']) 

        messages.success(self.request, f'Your deposit of {amount} was successful!')
        send_transaction_email(self.request.user, amount, 'Deposit Confirmation', 'book/deposit_email.html')
        return super().form_valid(form)  


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            password1 = form.cleaned_data.get('password1')
            if password1:
                user.set_password(password1)
            user.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'account/update_profile.html', {'form': form})