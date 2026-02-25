from django.contrib.auth import authenticate, login

from rest_framework import generics

from django.views import View

from main.forms import UserCreationForm, AddPostForm
from main.models import *
from main.serializers import ShopSerializer

from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, redirect
from coolsite.settings import RECIPIENTS_EMAIL, DEFAULT_FROM_EMAIL


def index(request):
    menu = P_Menu.objects.all()
    which_product = []
    if_in_cart = False
    for i in menu:
        if i.which_product not in which_product:
            which_product.append(i.which_product)
    try:
        request.session['cart']
        request.session['cart'] = list(request.session['cart'])
    except:
        for i in menu:
            i.in_basket = False
            i.save()

        request.session['cart'] = list()

    if request.POST.get('add_in_basket'):

        for i in request.session['cart']:

            if list(i[0].values()) == [request.POST['add_in_basket']]:
                if_in_cart = True
                temp = P_Menu.objects.get(title=request.POST['add_in_basket'])
                temp.in_basket = True
                temp.save()
        if not if_in_cart:
            temp = P_Menu.objects.get(title=request.POST['add_in_basket'])
            request.session['cart'].append(
                [{'title': temp.title}, {'price': temp.price}, {'count': temp.count}, {'summ': temp.price}])

    return render(request, "main/index.html", {'menu': menu, 'which_product': which_product})


def basket(request):
    if request.POST.get('order'):
        if request.user.is_authenticated:
            temp_order = 0
            name_lst = ''
            for i in request.session['cart']:
                temp_order += int((i[3])['summ'])
                name_lst += f"Продукт: {(i[0])['title']}, Колличество: {(i[2])['count']} \n"
                print(temp_order, name_lst)

            try:
                send_mail(f'Заказ от {request.user} на сумму {temp_order} в город {request.session["city"][0][0]}',
                          name_lst,
                          DEFAULT_FROM_EMAIL, RECIPIENTS_EMAIL)
                del request.session['cart']
                request.session.modified = True

            except BadHeaderError:
                context = {
                    'text': 'Ошибка в теме письма.',
                    'title': 'Ошибка',
                }
                return render(request, 'main/dist/index.html', context)

            context = {
                'text': 'Приняли! Спасибо за вашу заявку.',
                'title': 'Приняли',
            }
            return render(request, 'main/dist/index.html', context)

        else:
            context = {
                'text': 'Вы должны пройти регистрацию для заказа с сайта.',
                'title': 'Ошибка',
            }
            return render(request, 'main/dist/index.html', context)

    if request.POST.get('del_in_basket'):
        title = (request.POST['del_in_basket']).split("'")
        for i in request.session['cart']:
            if title[3] == (i[0])['title']:
                (request.session['cart']).remove(i)
                break
        if request.session['cart'] == []:
            del request.session['cart']
        request.session.modified = True
    if request.POST.get('change_count_minus'):
        title = request.POST['change_count_minus']
        title = (title).split(",")
        count = title[2].lstrip("{'count': ").rstrip("}")
        summ = title[3].lstrip("{'summ': ").rstrip("}]")
        name = title[0].lstrip("[{'title': ").rstrip("}'")
        price = title[1].lstrip("{'price': ").rstrip("}")
        for i in request.session['cart']:
            if name == (i[0])['title']:
                (i[2])['count'] = int(count) - 1
                (i[3])['summ'] -= int(price)
        request.session.modified = True
    elif request.POST.get('change_count_plus'):
        title = request.POST['change_count_plus']
        title = (title).split(",")
        count = title[2].lstrip("{'count': ").rstrip("}")
        summ = title[3].lstrip("{'summ': ").rstrip("}]")
        name = title[0].lstrip("[{'title': ").rstrip("}'")
        price = title[1].lstrip("{'price': ").rstrip("}")
        for i in request.session['cart']:
            if name == (i[0])['title']:
                (i[2])['count'] = int(count) + 1
                (i[3])['summ'] += int(price)
        request.session.modified = True
    request.session.summ_money = 0
    try:
        for i in (request.session['cart']):
            for j in i:
                if 'summ' in j.keys():
                    request.session.summ_money += j['summ']
    except:
        request.session.summ_money = 0

    try:
        return render(request, "main/basket.html",
                      {'menu': request.session['cart'], 'summ_money': request.session.summ_money})
    except:
        return render(request, "main/basket.html", {'menu': []})


Global_Form = None


def add_to_menu(request):
    if request.method == "POST":
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            context = {
                'text': 'Ошибка при создании формы.',
                'title': 'Ошибка'
            }
            return render(request, 'main/dist/index.html', context)

    else:
        form = AddPostForm()

    return render(request, 'main/add_to_menu.html', {'form': AddPostForm()})


class Register(View):
    template_name = 'registration/register.html'

    global Global_Form

    def get(self, request):
        context = {
            'form': UserCreationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            global Global_Form
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            Global_Form = form

            try:
                send_mail(f'Подтвердите вход в почту',
                          f'Пользователь {username} хочет зарегестрироваться на сайт под вашей почтой перейдите по ссылке для подтверждения {request.get_host()}/email_confirm если это не вы проигнарируйте письмо',
                          DEFAULT_FROM_EMAIL, [username, ])
                context = {
                    'text': 'Спасибо! После подтверждения почты аккаунт станет доступным!',
                    'title': 'Регистрация'
                }
                return render(request, 'main/dist/index.html', context)
            except BadHeaderError:
                context = {
                    'text': 'Ошибка в теме письма.',
                    'title': 'Ошибка письма'
                }
                return render(request, 'main/dist/index.html', context)

        context = {
            'form': form
        }
        return render(request, self.template_name, context)


def email_confirm(request):
    form = Global_Form
    form.save()
    user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password1'))
    login(request, user)
    return redirect('home')


class ShopAPIView(generics.ListAPIView):
    queryset = P_Menu.objects.all()
    serializer_class = ShopSerializer


def Catch_404(request, exception):
    context = {
        'text': 'Страница не найдена. Ошибка 404',
        'title': 'Ошибка 404',
    }
    return render(request, 'main/dist/index.html', context)


def profil(request):
    cities = [['Кокшетау', "Астана", "Алмата"], ["Караганда", 'Костанай', "Петропавловск"],
              ["Ерементау", "Шымкент", 'Семей'], ["Актобе", "Уральск", "Павлодар"]]

    if request.POST.get('city'):
        print('CITY', request.POST['city'])
        try:
            request.session['city']
            del request.session['city']
            request.session['city'] = list()
            request.session['city'].append([request.POST['city']])
        except:
            request.session['city'] = list()
            request.session['city'].append([request.POST['city']])
    return render(request, 'main/profil.html', {'cities': cities})


def game(request):
    return render(request, 'main/game/index.html')




def search1(request):
    menu = P_Menu.objects.all()
    menu1 = []
    if request.POST.get('q'):
        print(request.POST.get('q'))
    for i in menu:
        if request.POST.get('q') and request.POST.get('q') in i.title:
            menu1.append(i)
    return render(request, "main/f1.html", {'menu': menu1})
