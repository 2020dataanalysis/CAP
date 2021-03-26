# https://www.youtube.com/watch?v=BppyfPye8eo
import csv, io, ast, time, datetime, django_filters
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, Http404
from django.http import HttpResponse, HttpResponseRedirect
from .models import CC_log
from cclog.forms import CC_New_Log_Form, CC_Log_Form, CC_Log_Form2

from django.contrib.auth.decorators import permission_required
from django.db import connection
from django.conf.urls import url
from cclog.filters import CC_Log_Filter
from django.contrib.auth.models import User
from mail.views import send_email_attach, get_logs_attach

from cc.models import CC

#	CC Log - Create a Log
@login_required(login_url='login')	#	login → url name
def log( request ):
	print( request.method )
	vendors = get_vendors()

	if request.method == 'GET':
		print( f'{request.user.username} create log' )
		d = datetime.today().strftime('%Y-%m-%d')
		form = CC_New_Log_Form(initial={'transaction_date': d })
		template = 'cclog/log.html'
		context = { 'form': form, 'vendors': vendors }

		return render( request, template, context )

	if request.method == "POST":
		print('post new log')
		form = CC_New_Log_Form( request.POST )
		if form.is_valid():
			print('save new log')
			i			= form.save()
			i.log_id	= i.id
			i.user_id	= str( request.user )
			i.start		= int( time.time() )
			i.save()

			attachment = get_logs_attach()
			send_email_attach( 'BEAR CC Log - Attached', 'Log file is attached.', attachment )

			form = CC_Log_Form( instance=i )
			form = disable( form )
			template = 'cclog/view.html'
			context = { 'title': 'New Log Saved',
						'form': form,
						'card': '44006608902xXxXx0523' }

			return render( request, template, context )

		else:
			print('Form Not Valid')
			print(form.errors)
			return HttpResponse( 'Form is not valid.' )




def get_vendors():
	print('get Vendors')
	records = CC.objects.all()
	d = {}
	n = 0
	for i in records.iterator():
		n += 1
		d[i.payee]	= [ i.payee, i.address ]
		print( f'{n} {d[i.payee]}')

	print( len( d ))

	kill_keys = ['AMAZON.COM', 'Amazon.com', 'AMZN Mktp US', 'AMZN MKTP US', 'eBay']
	for k in kill_keys:
		matches = [s for s in d if k in s]
		remove_keys( d, matches )

	d['Amazon.com']		= 'Amazon.com'
	d['AMZN Mktp US']	= 'AMZN Mktp US'
	d['EBAY.com']		= 'EBAY.com'
	vendors = sorted ( d.keys() )
	for i in range( len( vendors )):
		print( i, vendors[i] )

	return vendors


def remove_keys( vendors, keys ):
	for i in keys:
		del vendors[ i ]

	return vendors


def logs( request ):
	# ro_list = RO.objects.all()
	all = CC_log.objects.all()		# This needs to be in parenthesis

	filter = CC_Log_Filter( request.GET, queryset=all )
	n = len( filter.qs )
	# cost = 0
	# price = 0
	# for i in filter.qs:
	# 	cost	+= i.cost
	# 	price	+= i.price

	# tot = filter.qs.objects.annotate(cost=Sum('cost'))

	context = 	{ 'transactions': filter,
					'count':	n,
					# 'total_cost': round( cost, 2),
					# 'total_price': round( price, 2)
				}
	return render( request, 'cclog/logs.html', context )





@login_required(login_url='login')	#	login → url name
def update( request ):
	pk = request.POST['choice']
	print( f'{request.user.username} update {pk}' )
	qs = CC_log.objects.filter(pk=pk)
	if not qs.exists():
		return HttpResponse(f'Log { pk } does not exist.  Call or text 925.575.7070.')
	
	#	Can not use qs from filter → need to use .get
	i = CC_log.objects.get( pk=pk )	# Causes matching query does not exist

	#	Current Non Linking Rogue Form
	form = CC_Log_Form( instance = i )

	#	Linking Form
	if request.user.is_superuser or request.user.username == 'sam':
		form = CC_Log_Form2( instance = i )

	form.fields['log_id'].widget.attrs['readonly'] = True
	form.fields['user_id'].widget.attrs['readonly'] = True

	title			= 'Update Log'
	template		= 'cclog/update.html'

	if i.voided:
		title		= 'Log Voided'
		template	= 'cclog/view.html'
		form		= disable( form )

	if i.closed:
		title		= 'Log Closed'
		template	= 'cclog/view.html'
		form		= disable( form )

	if not request.user.is_superuser and not request.user.username == 'sam':
		if i.user_id != request.user.username:
			title		= 'Non Purchaser View'
			template	= 'cclog/view.html'
			form		= disable( form )

	vendors = get_vendors()

	context = {
				'title': title,
				'i': i, 
				'form': form,
				'vendors': vendors
				}
	return render( request, template, context )






# @login_required(login_url='login')	#	login → url name
def updatelink( request ):
	# from ../models import CC
	c = request.POST['choice']
	# print( '**************************************')
	# print ( type ( c ) )
	print( c )

	pks		= ast.literal_eval( request.POST.get("choice") )
	# pk		= CC_log.objects.get( pk=pks[0] )
	pk		= pks[0]
	cc_id	= pks[1]

	print( f'{request.user.username} update {pk}' )
	qs = CC_log.objects.filter(pk=pk)
	if not qs.exists():
		return HttpResponse(f'Log { pk } does not exist.  Call or text 925.575.7070.')

	#	Can not use qs from filter → need to use .get
	i		= CC_log.objects.get( pk=pk )	# Causes matching query does not exist
	i.cc_id	= cc_id
	form	= CC_Log_Form2( instance = i )

	form.fields['log_id'].widget.attrs['readonly'] = True
	form.fields['user_id'].widget.attrs['readonly'] = True

	title			= 'Update Link Log'
	template		= 'cclog/update.html'

	if i.voided:
		title		= 'Log Voided'
		template	= 'cclog/view.html'
		form		= disable( form )

	if i.closed:
		title		= 'Log Closed'
		template	= 'cclog/view.html'
		form		= disable( form )

	if not request.user.is_superuser:
		if i.user_id != request.user.username:
			title		= 'Non Purchaser View'
			template	= 'cclog/view.html'
			form		= disable( form )

	context = {
				'title': title,
				'i': i,
				'form': form }
	return render( request, template, context )


















def disable( form ):
	form.fields['log_id'].widget.attrs['readonly'] = True
	form.fields['user_id'].widget.attrs['readonly'] = True
	# if form.fields['cc_id'].exists:
	# form.fields['cc_id'].widget.attrs['readonly'] = True	#	Not used in add new log
	form.fields['transaction_date'].widget.attrs['readonly'] = True
	form.fields['vendor'].widget.attrs['readonly'] = True
	form.fields['amount'].widget.attrs['readonly'] = True
	form.fields['ro1'].widget.attrs['readonly'] = True
	form.fields['ro2'].widget.attrs['readonly'] = True
	form.fields['ro3'].widget.attrs['readonly'] = True
	form.fields['ro4'].widget.attrs['readonly'] = True
	form.fields['ro5'].widget.attrs['readonly'] = True
	form.fields['invoice'].widget.attrs['readonly'] = True
	form.fields['returned'].widget.attrs['disabled'] = True
	form.fields['credit'].widget.attrs['disabled'] = True
	form.fields['voided'].widget.attrs['disabled'] = True
	form.fields['closed'].widget.attrs['disabled'] = True
	return form



@login_required(login_url='login')	#	login → url name
def update_save(request, pk):
	print('get post')
	post_keys = list(request.POST.keys())
	print( post_keys )
	i = CC_log.objects.get(pk=pk)
	form = CC_Log_Form( request.POST, instance = i )

	if request.user.is_superuser:			#	if User.is_superuser:  Does not work !
		form = CC_Log_Form2( request.POST, instance = i )
		print('Superuser → Log Form 2')
	
	if form.is_valid():
		if form.cleaned_data.get("voided"):
			i.stop	= int( time.time() )

		if form.cleaned_data.get("closed"):
			i.stop	= int( time.time() )

		form.save()

		form = disable( form )
		if 'cc_id' in post_keys:
			form.fields['cc_id'].widget.attrs['readonly'] = True	# Not used in adding a new log

		title	= 'Update Saved'		#	status confirmation
		template = 'cclog/view.html'
		context = {
				'title': title,
				'form': form,
					'i': i
		}
		return render( request, template, context )

	else:
		print('Form Not Valid')
		print(form.errors)
		return HttpResponse('Error detected.')


def get_post(request):
	s = ""
	for key in request.POST:
		value = request.POST[key]
		s += key + ':' + value + '<br>'

	return s


@login_required(login_url='login')	#	login → url name
def reopen(request, pk):
	print('reopen')
	i = CC_log.objects.get(pk=pk)
	i.closed = False				#		Admin override
	i.stop	= 1
	i.save()
	print( i )
	form = CC_Log_Form( instance = i )
	form = disable( form )
	title	= 'Update Saved'		#	status confirmation
	template = 'cclog/view.html'
	context = {
			'title': title,
			'form': form,
				'i': i
	}
	return render( request, template, context )





# Deprecated No search filter
# # @login_required(login_url='login')	#	login → url name
# def logs( request ):
# 	cursor = connection.cursor()
# 	t = timestamp	= int( time.time() )
# 	cursor.execute(f"select log_id, user_id, transaction_date, vendor, debit, amount, ro1, invoice, returned, voided, closed, cc_id, start, stop FROM cclog_cc_log" )
# 	results = cursor.fetchall()
# 	context =	{	'transactions': results,
# 					'count':		len( results)
# 				}
# 	return render( request, 'cclog/logs.html', context )
