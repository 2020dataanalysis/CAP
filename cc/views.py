# https://www.youtube.com/watch?v=BppyfPye8eo
import csv, io, ast, time, datetime, django_filters
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, Http404
from django.http import HttpResponse, HttpResponseRedirect
from cc.models import CC
from ro.models import RO
from cc.forms import CC_Form, CC_Update_Form
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.db import connection



def home( request ):
	print( f'{ datetime.datetime.now() } { request.user }' )
	return render( request, 'cc/welcome.html', {} )


def view( request ):
	# print( request.method )
	linked = ''		#	Include linked transactions checkbox
	if request.method == 'GET':
		s = get_get( request )
		print( s )
		# log_id 	= request.GET['logid']	# log_id is used by Filter
		# print( log_id )
		key = 'linked'
		if key in request.GET:
			linked = 'checked'	# request.GET[key]
			print( linked )			
			all = CC.objects.all().order_by('-posted_date')
		else:
			print( f'key { key } is not in GET request.')
			# cc_clear_linked()		#	Updates cc: user_id ro invoice
			# cc_mark_linked()		#	Refreshes after each search
			all = CC.objects.filter( log_id=0 ).order_by('-posted_date')


	# if request.method == "POST":
	# 	log_id 	= request.POST['log_id']
	# 	# print( type( log_id ))
	# 	# logid = int( log_id )
	# 	cc_clear_linked()		#	Updates cc: user_id ro invoice
	# 	cc_mark_linked()
	# 	all = CC.objects.filter( log_id=0 ).order_by('-posted_date')


	from .filters import CC_Filter
	filter = CC_Filter( request.GET, queryset=all )
	n = len( filter.qs )
	cost = 0
	for i in filter.qs:
		cost	+= i.amount

	context =	{
					'linked': linked,
					'transactions': filter,
					'count':	n,

					'total_cost': round( cost, 2)
				}
	return render( request, 'cc/view.html', context )





def link( request ):
	print( request.method )
	keys = list( request.GET.keys() )
	print( keys )


	linked = ''		#	Include linked transactions checkbox
	if request.method == 'GET':
		s = get_get( request )
		print( s )
		log_id 	= request.GET['logid']	# log_id is used by Filter
		print( log_id )
		key = 'linked'
		if key in request.GET:
			linked = 'checked'	# request.GET[key]
			print( linked )			
			all = CC.objects.all().order_by('-posted_date')
		else:
			print( f'key { key } is not in GET request.')
			cc_clear_linked()		#	Updates cc: user_id ro invoice
			cc_mark_linked()		#	Refreshes after each search

			all = CC.objects.filter( log_id=0, payee=request.GET['payee'] ).order_by('-posted_date')



	if request.method == "POST":
		log_id 	= request.POST['log_id']
		# print( type( log_id ))
		# logid = int( log_id )
		cc_clear_linked()		#	Updates cc: user_id ro invoice
		cc_mark_linked()
		all = CC.objects.filter( log_id=0 ).order_by('-posted_date')


	from .filters import CC_Filter
	filter = CC_Filter( request.GET, queryset=all )
	n = len( filter.qs )
	cost = 0
	for i in filter.qs:
		cost	+= i.amount

	context =	{
					'linked': linked,
					'transactions': filter,
					'count':	n,
					'log_id':	log_id,
					'total_cost': round( cost, 2)
				}
	return render( request, 'cc/link.html', context )



def cc_clear_linked():
	print('Clear Linked')
	records = CC.objects.all()
	for i in records.iterator():
		i.user_id	= ''
		i.log_id	= 0
		i.ro		= ''
		i.invoice	= ''
		i.save()


def cc_mark_linked():
	# print('cc_mark_linked()')
	cursor = connection.cursor()
	cursor.execute("select cc_cc.cc_id, cclog_cc_log.user_id, cclog_cc_log.log_id, cclog_cc_log.ro1, cclog_cc_log.invoice FROM cc_cc INNER JOIN cclog_cc_log ON cc_cc.cc_id = cclog_cc_log.cc_id" )
	results = cursor.fetchall()

	for i in results:
		pk = i[0]
		qs = CC.objects.filter(pk= pk)
		if not qs.exists():
			return HttpResponse(f'CC { pk } does not exist.  Call or text 925.575.7070.')

		#	Can not use qs from filter → need to use .get
		j		= CC.objects.get( pk=pk )	# Causes matching query does not exist
		j.user_id	= i[1]
		j.log_id	= i[2]
		j.ro		= str( i[3] )
		j.invoice	= i[4]
		j.save()



def get_post(request):
	s = ""
	for key in request.POST:
		value = request.POST[key]
		s += key + ':' + value + '<br>'

	return s


def get_get(request):
	s = ""
	for key in request.GET:
		value = request.GET[key]
		s += key + ':' + value + '<br>'

	return s
