from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.http import require_POST
from .models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.

def userlist(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'accounts/userlist.html', context)


def userdetail(request, user_pk):
    user1 = get_object_or_404(User, pk=user_pk)
    context = {'user1': user1}
    return render(request, 'accounts/userdetail.html', context)


def signup(request):
    if request.user.is_authenticated:
        return redirect('movies:index')
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('movies:index')
    else:
        form = CustomUserCreationForm()
    context = {'form': form}
    return render(request, 'accounts/auth_form.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('movies:index')
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'movies:index')
    else:
        form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'accounts/login.html', context)


def logout(request):
    auth_logout(request)
    return redirect('movies:index')

@require_POST # post요청만 받는다.
def delete(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    if request.user.is_staff:
        user.delete()
    return redirect('accounts:staff')

@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('movies:index')
    else:
        form = CustomUserChangeForm(instance=request.user) # request.user : 유저정보
    context = {'form': form,}
    return render(request, 'accounts/auth_form.html', context)

@login_required # 비로그인 상태로 접근할 수 없게 만든다.
def change_password(request):
    if request.method == 'POST': # 비밀번호 수정
        form = PasswordChangeForm(request.user, request.POST) # 유저정보(request.user), 데이터(request.POST) 순으로 들어감
        if form.is_valid():
            user = form.save() # user로 안받으면 form.user로 해줘야한다!
            update_session_auth_hash(request, user) # 비번 변경 후 로그아웃되지 않고 로그인 상태 유지
            return redirect('movies:index')
    else:
        form = PasswordChangeForm(request.user) # user 정보(request.user) 필요함!
    context = {'form': form,}
    return render(request, 'accounts/change_password.html', context)

@staff_member_required
def staff(request):
    users = User.objects.all()
    context = {'users': users,}
    return render(request, 'accounts/adminpage.html', context)