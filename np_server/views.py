# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from np_server.models import *
from django.contrib.auth import authenticate, login
from django.template.loader import get_template
from django.template import Context
import md5, random
import base64, hmac, hashlib
import datetime
import StringIO
import re
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from bs4 import BeautifulSoup
from urllib2 import urlopen
from lxml.html import parse

#-------------------------------------------------------------------------------------------------

# Получение userid из сессии
def get_userid(_session_str):
    j = 0
    str_userid = ''
    user_id = 0
    while (_session_str[j] != '|'):
        str_userid = str_userid + _session_str[j]
        j = j + 1
    user_id = int(str_userid)
    return user_id


#Получить хеш django пароля
def get_sha_hesh(password_string):
    algorithm = 'sha1'
    salt = get_random_string()
    raw_password = password_string
    raw_password, salt = smart_str(raw_password), smart_str(salt)
    hsh = get_hexdigest(algorithm, salt, raw_password)
    return '%s$%s$%s' % (algorithm, salt, hsh)


# Автоматизация проверки сессии
def if_user_session(session_key):
    # Вытащить userid из сессии
    userid = get_userid(session_key)
    p0 = UserProfile.objects.get(pk=userid)
    #p0 = User.objects.get(pk=userid)
    # Сравнение сессии юзера со значением в его куках
    if (session_key == p0.you_session):
        return True
    else:
        return False


def if_device_having(user_id_tmp):
    have_dev = Device.objects.get(pk=userid)
    if have_dev.model != None:
        have_status = ClientStatus.objects.get(pk=userid)
        return have_status.monitor_status, have_status.search_status
    else:
        return False

def api_documentation(request):
    return render_to_response("api_v_1.html")


def registration_page(request):
    return render_to_response("login.html")
#---------------------------------------------------------------------------------------------------------

def login(request):
	username = request.POST['username'].lower()
	password = request.POST['password']
	latitude_one = 55.039873
	longitude_one = 55.961532
	user = auth.authenticate(username=username, password=password)
	if user is not None and user.is_active:
		# Правильный пароль и пользователь "активен"
		auth.login(request, user)
		m1 = User.objects.get(username=request.POST['username'])
		userid = m1.id
		test = UserProfile.objects.get(pk=userid)
		session_hashgen = str(userid) + '|' + md5.new(str(userid) + request.META['REMOTE_ADDR']).hexdigest() + md5.new(
			request.META['HTTP_USER_AGENT'] + 'random_secret').hexdigest()
		test.you_session = session_hashgen
		test.save()
		request.session['SESSION_EXPIRE_AT_BROWSER_CLOSE'] = True
		request.session['you_session'] = session_hashgen
		have_dev = Device.objects.get(pk=userid)
		if have_dev.model != None:
			have_status = ClientStatus.objects.get(pk=userid)
			have_dev_to = Device.objects.filter(user_id=userid)
			return render_to_response('usermodule.html', {'have_device': have_status, 'all_devices': have_dev_to, 'latitude_one':latitude_one, 'longitude_one':longitude_one})
		return HttpResponseRedirect("/accounts/login/")
	else:
		# Отображение страницы с ошибкой
		return HttpResponseRedirect("/accounts/invalid/")


def logout(request):
    try:
        del request.session['you_session']
    except KeyError:
        pass
    return HttpResponseRedirect("/")


def reg_set(request):
    if ('username' in request.POST) and ('name' in request.POST) and ('email' in request.POST) and (
                'password' in request.POST):
        if (request.POST['username'].isalnum() and request.POST['name'].isalpha() and checkPass(
                request.POST['password']) and email(request.POST['email'])):
            username_low = request.POST['username'].lower()
            unic_username = User.objects.filter(username=request.POST['username']).count()
            unic_email = User.objects.filter(email=request.POST['email']).count()
            if (unic_username == 0):
                if (unic_email == 0):
                    reg_pass = get_sha_hesh(request.POST['password'])
                    savebase = User(username=username_low, name=request.POST['name'], email=request.POST['email'],
                                    password=reg_pass, user_ip=request.META['REMOTE_ADDR'],
                                    user_agent=request.META['HTTP_USER_AGENT'])
                    savebase.save()
                    user_name = request.POST['username']
                    t = get_template('registration_response.html')
                    message = t.render(Context({'success': user_name}))
                    return HttpResponse(message)
                else:
                    user_name = request.POST['username']
                    return render_to_response('registration_response.html', {'fail_email': user_name})
            else:
                user_name = request.POST['username']
                return render_to_response('registration_response.html', {'fail_name': user_name})


#--------------------------------------------------------------------------------------------------------------

def blog(request):
    return render_to_response("blog.html")


def about(request):
    return render_to_response("about.html")
	
def index(request):
    return render_to_response("index.html")

def test_user(request):
    return render_to_response("usermodule2.html")

def main_module(request):
    return render_to_response("usermodule.html")


def monitoring_go(request):
    monitor = 'go_to_monitor'
    return render_to_response("usermodule.html", {'monitoring_go': monitor})


def admin_panel_go(request):
    admin_go = 'go_to_admin'
    return render_to_response("usermodule.html", {'admin_panel_go': admin_go})


def device_adding_go(request):
    adding_go = 'go_to_add'
    return render_to_response("usermodule.html", {'device_adding_go': adding_go})


def api_go(request):
    api_go = 'go_to_api'
    return render_to_response("usermodule.html", {'api_go': api_go})


#------------------------------------------------------------------------------------------------

def where_device_data(request):
    net_info, geo_info, session_info, webcam = False, False, False, False
    test_data = {}
    if (if_user_session(request.session['you_session'])):
        if 'geo_info' in request.POST:
            geo_info = True
        if 'net_info' in request.POST:
            net_info = True
        if 'session_info' in request.POST:
            session_info = True
        if 'webcam' in request.POST:
            webcam = True
        test_data = {'geo_info': geo_info, 'net_info': net_info, 'session_info': session_info, 'webcam': webcam}
        return HttpResponse(simplejson.dumps(test_data), mimetype='application/javascript')
    else:
        return render_to_response("usermodule.html")


def API_generation(request):
    #base64.b64encode(hashlib.sha256( str(random.getrandbits(256)) ).digest(), random.choice(['rA','aZ','gQ','hH','hG','aR','DD'])).rstrip('==')
    #Сохранить ключ в бд, вывести на экран
    #Добавить проверку на сессию
    if (if_user_session(request.session['you_session'])):
        api_key_gen = hashlib.sha224(str(random.getrandbits(256))).hexdigest()
        tmp = UserProfile.objects.select_related().filter(you_session=request.session['you_session']).update(
            api_key=api_key_gen)
        monitor = 'Copy and save your api_key'
        return render_to_response("usermodule.html", {'api_key_view': api_key_gen, 'monitoring_go': monitor})
    else:
        return render_to_response("usermodule.html")


def actions_for_mclient(request):
    #userid = get_userid(request.session['you_session'])
    userid = 1
    # return render_to_response('blog.html')
    if 'login' in request.POST and 'api_key' in request.POST:
        api = ''
        api = UserProfile.objects.get(api_key=request.POST['api_key'])
        if (api != ''):
            to_dev = Device(user_id=userid, model=request.POST['model'], imei=request.POST['imei'],
                            phone_number=request.POST['phone_number'], usbidcode=request.POST['usbidcode'],
                            latitude=request.POST['latitude'], longitude=request.POST['longitude'],
                            ip_info=request.POST['ip_info'], wifi_info=request.POST['api_key'],
                            battery_info=request.POST['battery_info'], webcam_picture=request.POST['webcam_picture'])
            to_dev.save()
            to_status = ClientStatus(user_id=userid, alarm=request.POST['alarm'], warning=request.POST['warning'],
                                     blocking=request.POST['blocking'], privacy=request.POST['privacy'])
            to_status.save()
            to_rep = Report(user_id=userid, all=request.POST['all'], report_text=request.POST['report_text'])
            to_rep.save()
            result_save = True
            ok = 'OK'
            test_data = {'result_save': result_save, 'connect': ok}
            return render_to_response('blog.html')
        #return HttpResponse(simplejson.dumps(test_data), mimetype='application/javascript')
        else:
            result_save = False
            ok = 'error'
            test_data = {'result_save': result_save, 'connect': ok}
        #return HttpResponse(simplejson.dumps(test_data), mimetype='application/javascript')
        return render_to_response('blog.html')
    else:
        return render_to_response('blog.html')


def actions_webuser(request):
    if (if_user_session(request.session['you_session'])):
        act1 = Action(alarm=False, warning=False, blocking=False, privacy=False)
        act1.save()
        userid = get_userid(request.session['you_session'])
        # act2 = SmsCommands(user_id=userid,status=False,alarm=False,message=False,sound_on=False,sound_off=False,speak=False,data_start=False,data_stop=False,wifi_start=False,wifi_stop=False,call=False,hangup=request.POST['hangup'],recordsound=request.POST['recordsound'],apn_copy=request.POST['apn_copy'],apn_remove=request.POST['apn_remove'],apn_enable=request.POST['apn_enable'],apn_disable=request.POST['apn_disable'],gps_on=request.POST['gps_on'],block=request.POST['block'],unblock=request.POST['unblock'],startapp=request.POST['startapp'],erasesdcard=request.POST['erasesdcard'],wipe=request.POST['wipe'])
        # act2.save()
        act2 = SmsCommands(user_id=userid, status=False, alarm=False, message=False, sound_on=False, sound_off=False,
                           speak=False, data_start=False, data_stop=False, wifi_start=False, wifi_stop=False,
                           call=False, hangup=False, recordsound=False, apn_copy=False, apn_remove=False,
                           apn_enable=False, apn_disable=False, gps_on=False, block=False, unblock=False,
                           startapp=False, erasesdcard=False, wipe=False)
        act2.save()
        act3 = Research(geo_info=False, wifi_info=False, webcam=False)
        act3.save()
        message_to_console = "Status: start! sms command sending, wait 5-10 min.."
        #Отправить запрос клиенту через sms
        return render_to_response('usermodule.html', {'console': message_to_console})
    else:
        message_to_console = "Nothing doing, go to read FAQ for searching.."
        return render_to_response('usermodule.html', {'console': message_to_console})


def update_device_(request):
	userid = "1"
	#if (inbase.installer != Null):
	#Делаем запрос к базе Device, посмотреть
	# device_adding = userid
	#
	# return render_to_response("usermodule.html", "device_adding": device_adding)
	message_to_console = "Device add to base!"
	return render_to_response("UpdateDevice.html",  {'console_out': message_to_console})


def add_device_(request):
	# userid = "1"
	# #userid = get_userid(request.session['you_session'])
	# to_dev = Device(user_id=userid, model=request.POST['model'], imei=request.POST['imei'],
						# phone_number=request.POST['phone_number'], usbidcode=request.POST['usbidcode'],
						# latitude=request.POST['latitude'], longitude=request.POST['longitude'],
						# ip_info=request.POST['ip_info'], wifi_info=request.POST['wifi_info'],
						# battery_info=request.POST['battery_info'], webcam_picture=request.POST['webcam_picture'])
	# to_dev.save()
	# if (inbase.installer != Null):
	#Делаем запрос к базе Device, посмотреть
	# device_adding = userid
	#
	# return render_to_response("usermodule.html", "device_adding": device_adding)
	message_to_console = "Device add to base!"
	return render_to_response("AddDevice.html", {'console': message_to_console})
	
def save_device_(request):
	userid = "1"
	#userid = get_userid(request.session['you_session'])
	to_dev = Device(user_id=userid, model=request.POST['model'], imei=request.POST['imei'],
						phone_number=request.POST['phone_number'], usbidcode=request.POST['usbidcode'],
						latitude=request.POST['latitude'], longitude=request.POST['longitude'],
						ip_info=request.POST['ip_info'], wifi_info=request.POST['wifi_info'],
						battery_info=request.POST['battery_info'], webcam_picture=request.POST['webcam_picture'])
	to_dev.save()
	#if (inbase.installer != Null):
	#Делаем запрос к базе Device, посмотреть
	# device_adding = userid
	#
	# return render_to_response("usermodule.html", "device_adding": device_adding)
	message_to_console = "Device add to base!"
	return render_to_response("AddDevice.html",  {'console_out': message_to_console})


	
#Отображение местоположения устройства на карте
def view_on_map(request):
	if (if_user_session(request.session['you_session'])):
		userid = get_userid(request.session['you_session'])
		to_dev = Device.objects.get(pk=userid)
		return render_to_response('usermodule.html', { 'on_the_map': to_dev })
	else:
		message_to_console = "Nothing doing, go to read FAQ for searching.."
		return render_to_response('usermodule.html', { 'on_the_map': message_to_console })
	# message_to_console = "Nothing doing, go to read FAQ for searching.."
	# return render_to_response('usermodule.html', { 'on_the_map': message_to_console })
	
#Отправка команд с сайта
#def send_sms_command():
	#Получить данные из формы
	#Сформировать текст смс команды, номер телефона
	#Отправить данные на сервис отправки сообщений, послать команду
	#
	


def mvd_message(request):
	if "you_session" in request.session:
		if 'mvd' in request.POST:
			tmp_mvd = "mvd_map"
			t = get_template('usermodule.html')
			message = t.render(Context({'tmp_mvd': tmp_mvd }))
			return HttpResponse(message)
	else:
		error_message = "error"
		t = get_template('usermodule.html')
		message = t.render(Context({'error_message': error_message }))
		return HttpResponse(message)

def all_tools(request):
	if "you_session" in request.session:
		if 'all_tools' in request.POST:
			all_tools = 'tools_view'
			t = get_template('usermodule.html')
			message = t.render(Context({'all_tools': all_tools}))
			return HttpResponse(message)

def parsing_for_cellid():
    if (if_user_session(request.session['you_session'])):
        tmp_dev = Device.objects.get(pk=userid)
        str_lat1 = ''
        str_lat2 = ''
        str_lon1 = ''
        str_lon2 = ''
        if tmp_dev.cell_id == True:
            tmpBase = CellId.objects.get(pk=userid)
            parse_str = 'http://mobile.maps.yandex.net/cellid_location/?cellid=' + srt(
                tmpBase.cid) + '&operatorid=' + srt(tmpBase.mnc) + '&countrycode=' + srt(tmpBase.mcc) + '&lac=' + srt(
                tmpBase.lac)
            # html_doc = urlopen(parse_str).read()
            # soup = BeautifulSoup(html_doc)
            page = parse(parse_str).getroot()
            # Ищем все теги <a> с css классом topic
            hrefs = page.cssselect("coordinates")
            for row in hrefs:
                # Получаем атрибут href
                str_lat1 = row.get("latitude")
                str_lon1 = row.get("longitude")
                str_lat2 = row.get("nlatitude")
                str_lon2 = row.get("nlongitude")

            return render_to_response("usermodule.html", {'latitude': str_lat1, 'longitude': str_lon1})
        else:
            return render_to_response("usermodule.html")
        #Сделать запрос Device()
        #Отправить запрос на один из сайтов
        #Получить координаты
        #Вывести в яндекс карты
        #Вывести в консоль - координаты получены


#----------------------------Биржа задач-------------------------
def task_manager_output(request):
	if (if_user_session(request.session['you_session'])):
		tmp_task = Task.objects.all()
		return render_to_response("usermodule.html", {'tmp_task': tmp_task})
	else:
		return render_to_response("usermodule.html")
#Добавить задачу в базу
#Если изменена стоимость

#--------------------------Дать задание---------------------------

def task_manager_input_first(request):
	if (if_user_session(request.session['you_session'])):
		task_input = 'Сохранение в задачи в базу данных'
		return render_to_response("usermodule.html", {'task_input': task_input})
	else:
		return render_to_response("usermodule.html")
		

def task_manager_input_second(request):
	if (if_user_session(request.session['you_session'])):
		#new_task = Task(user='g1pn0z', status=request.POST['1'], theme=request.POST['2'], task=request.POST['3'], term=request.POST['4'], cost=request.POST['5'], karma=request.POST['6'])
		#new_task.save()
		task_input_second = 'Сохранение в задачи в базу данных'
		return render_to_response("usermodule.html", {'task_input_second': task_input_second})
	else:
		return render_to_response("usermodule.html")
		
def task_manager_input_third(request):
	if (if_user_session(request.session['you_session'])):
		userid = "1"
		new_task = Task(user_id=userid, status=True, theme=request.POST['task_theme'], task=request.POST['task_task'], term=request.POST['task_term'], cost=request.POST['task_cost'], karma='1')
		new_task.save()
		tmp_task = Task.objects.all()
		return render_to_response("usermodule.html", { 'tmp_task': tmp_task })
	else:
		return render_to_response("usermodule.html")
#--------------------------------------------------------------------

#------------------------Заказчик------------------------------------

def customer_menu(request):
	if (if_user_session(request.session['you_session'])):
		customer_menu = 'Сохранение в задачи в базу данных'
		return render_to_response("usermodule.html", {'customer_menu': customer_menu})
	else:
		return render_to_response("usermodule.html")

#------------------------Исполнитель------------------------------------

def artist_menu(request):
	if (if_user_session(request.session['you_session'])):
		artist_menu = 'Сохранение в задачи в базу данных'
		return render_to_response("usermodule.html", {'artist_menu': artist_menu})
	else:
		return render_to_response("usermodule.html")

#-------------------------Карточка-задачи-------------------------------
		
def task_card(request):
	if (if_user_session(request.session['you_session'])):
		if 'task_id' in request.POST:
			task_card = Task.objects.get(id=request.POST['task_id'])
			return render_to_response("usermodule.html", {'task_card': task_card})
	else:
		return render_to_response("usermodule.html")

#artist_message
def artist_message(request):
	if (if_user_session(request.session['you_session'])):
		artist_message = 'Сохранение в сообщения в базу данных'
		return render_to_response("usermodule.html", {'artist_message': artist_message})
	else:
		return render_to_response("usermodule.html")	

#message_list
def message_list(request):
	if (if_user_session(request.session['you_session'])):
		message_list = 'Сохранение в сообщения в базу данных'
		return render_to_response("usermodule.html", {'message_list': message_list})
	else:
		return render_to_response("usermodule.html")	

#------------------------Сообщения-Чат----------------------------------

def message_chat(request):
	if (if_user_session(request.session['you_session'])):
		message_chat = 'Сохранение в задачи в базу данных'
		return render_to_response("usermodule.html", {'message_chat': message_chat})
	else:
		return render_to_response("usermodule.html")

#--------------------------------------------------------------------
		
def checked_device(request): #Происходит при выборе устройства
	api_key = 'AKgqHEkBAAAA-WzMYwIAeAeamm8ETZZZpdfp2R07eIuGyX4AAAAAAAAAAACjUCDoHIHZJ2pcl5mSL1zWVp2Myw=='
	pos[0] = 55.039873
	pos[1] = 55.961532
	
	if 'modelDevice' in request.POST:
		if request.POST['modelDevice'] == 'Gsmart 1345':
			pick_dev = Device.objects.get(user_id=1, model='Gsmart 1345')
			my_way = UpdateDevice.objects.get(model='Gsmart 1345')
			return render_to_response("usermodule.html", {'my_way':my_way,'pick_dev':pick_dev})

	#Делаем запрос в базу, ищем конкретное устройство - 1, Device
	#Выбираем три последние координаты привязанные к данному устройству - UpdateDevice
	#Выводим координаты на карту

#-------------------------------------------------------------
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from np_server.serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer





