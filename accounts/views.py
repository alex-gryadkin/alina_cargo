from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import AuthForm, RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import OTPStorage, CargoUser, Cities
from .mixins import send_otp
from alina_cargo import settings


def login_view(request):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)
    if request.method == 'POST':
        form = AuthForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('packages:list')
    else:
        form = AuthForm()
    return render(request, 'login.html', {'form': form})


def register_view(request):
    form = RegisterForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()

            full_name = form.cleaned_data.get('full_name')
            city_name = form.cleaned_data.get('city')
            city = Cities.objects.get(city_name=city_name)

            user_id = user.id
            cargo_code = f'WINWIN-{city.city_short_name}{user_id}'
            cargouser = CargoUser(username=user, full_name=full_name, city=city, cargo_code=cargo_code)
            cargouser.save()

            OTPStorage.objects.filter(phone=username).delete()
            login(request, user)
            return redirect('packages:list')
        return render(request, 'final_creation.html', {'form': form,
                                                       'username': username})

    if request.GET.get('username') and request.GET.get('in_otp'):
        username = request.GET.get('username')
        out_otp = OTPStorage.objects.get(phone=username).otp
        in_otp = request.GET.get('in_otp')
        if in_otp == out_otp:
            return render(request, 'final_creation.html', {'form': form,
                                                           'username': username})
        else:
            otp_error = "Код не совпадает"
            return render(request, 'OTP_input.html', {'username': username,
                                                      'error': otp_error})

    elif request.GET.get('username'):
        username = request.GET.get('username')
        profile = User.objects.filter(username=username)

        if profile.exists():
            user_exist_error = 'Пользователь с таким номером уже зарегистрирован'
            return render(request, 'register.html', {'form': form,
                                                     'error': user_exist_error})
        send_otp(username)
        return render(request, 'OTP_input.html', {'username': username})

    return render(request, 'register.html', {'form': form})


def password_reset_phone(request):
    username = request.POST.get('username')
    if not username:
        return render(request, 'password_reset.html')

    user = User.objects.filter(username=username)
    if not user:
        error_message = 'Пользователь с указанным номером не найден'
        return render(request, 'password_reset.html', {'error': error_message})

    request.session['username'] = request.POST['username']
    return redirect('accounts:password_reset_otp')


def password_reset_otp(request):
    if 'username' not in request.session:
        return redirect('accounts:password_reset')

    username = request.session['username']
    if request.method == 'POST':
        in_otp = request.POST.get('in_otp')
        out_otp = OTPStorage.objects.get(phone=username).otp
        if in_otp == out_otp:
            return redirect('accounts:new_password')
        error_message = 'Неверный код. Проверьте в SMS'
        return render(request, 'password_OTP_input.html', {'error': error_message})

    send_otp(username)
    return render(request, 'password_OTP_input.html', {'username': username})


def new_password(request):
    if 'username' not in request.session:
        return redirect('accounts:password_reset')

    if request.method == 'GET':
        return render(request, 'new_password.html')

    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')

    if password1 == password2:
        username = request.session['username']
        user = User.objects.get(username=username)
        user.set_password(password1)
        user.save()
        OTPStorage.objects.filter(phone=username).delete()
        login(request, user)

        return redirect('packages:list')

    error_message = 'Пароли не совпадают'
    return render(request, 'new_password.html', {'error': error_message})


def change_password(request):
    if request.method == 'GET':
        return render(request, 'change_password.html')

    old_password = request.POST.get('old_password')
    new_password_1 = request.POST.get('password1')
    new_password_2 = request.POST.get('password2')

    if new_password_1 != new_password_2:
        error = 'Новые пароли не совпадают'
        return render(request, 'change_password.html', {'error': error})

    user = request.user
    if user.check_password(old_password):
        user.set_password(new_password_1)
        user.save()
        message = 'Пароль успешно изменен'
        login(request, user)
        return render(request, 'change_password.html', {'message': message})

    error = 'Вы ввели неверный текущий пароль'
    return render(request, 'change_password.html', {'error': error})

@login_required(login_url='accounts:login')
def profile_view(request):
    cargodata = CargoUser.objects.get(username=request.user)
    return render(request, 'profile.html', {'cargodata': cargodata})

def logout_view(request):
    logout(request)
    return redirect('accounts:login')

