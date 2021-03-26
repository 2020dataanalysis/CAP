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



# 03/15/2021
# @login_required(login_url='login')	#	login → url name
def linked( request ):
	cursor = connection.cursor()
	# cursor.execute("select cc_cc.cc_id, cc_cc.ro_id, cc_cc.posted_date, cc_cc.payee, cc_cc.address, cc_cc.amount FROM cc_cc WHERE cc_cc.ro_id > 0" )
	# select log_id, user_id, transaction_date, vendor, debit, amount, ro1, invoice, returned, voided, closed, cc_id, start, stop FROM cclog_cc_log" )
	# cursor.execute("select cc_cc.cc_id, cc_cc.posted_date, cc_cc.payee, cc_cc.address, cc_cc.amount, cclog_cc_log.log_id, cclog_cc_log.vendor, cclog_cc_log.amount,   cclog_cc_log.ro1, cclog_cc_log.invoice, cclog_cc_log.user_id FROM cc_cc INNER JOIN cclog_cc_log ON cc_cc.cc_id = cclog_cc_log.cc_id" )
	# cursor.execute("select cc_cc.cc_id, cc_cc.posted_date, cc_cc.payee, cc_cc.address, cc_cc.amount  FROM cc_cc" )	# Works 03/15/2021

	# cursor.execute("select cc_cc.cc_id, cc_cc.posted_date, cc_cc.payee, cc_cc.address, cc_cc.amount, cclog_cc_log.log_id, cclog_cc_log.vendor, cclog_cc_log.amount,   cclog_cc_log.ro1, cclog_cc_log.invoice, cclog_cc_log.user_id FROM cc_cc INNER JOIN cclog_cc_log ON cc_cc.cc_id = cclog_cc_log.cc_id" )
	cursor.execute("select cc_cc.cc_id, cc_cc.posted_date, cc_cc.payee, cc_cc.address, cc_cc.amount, cclog_cc_log.log_id, cclog_cc_log.vendor, cclog_cc_log.amount,   cclog_cc_log.ro1, cclog_cc_log.invoice, cclog_cc_log.user_id FROM cc_cc LEFT JOIN cclog_cc_log ON cc_cc.cc_id = cclog_cc_log.cc_id ORDER BY cc_cc.posted_date DESC" )
	results = cursor.fetchall()
	context = { 'transactions': results,
				'count':		len( results) }
	return render( request, 'cc/linked.html', context )





#	====================================================================
#	CC Link Log
#	Before 03/10/2021

@login_required(login_url='login')	#	login → url name
def unlinked( request ):
	cursor = connection.cursor()
	# cursor.execute("select * FROM cc_cc WHERE cc_cc.ro_id = 0" )
	t = timestamp	= int( time.time() )
	cursor.execute(f"select cc_cc.cc_id, cc_cc.up_id, cc_cc.user_id, cc_cc.claim_timestamp, cc_cc.posted_date, cc_cc.payee, cc_cc.address, cc_cc.amount, cc_cc.ro, cc_cc.invoice, { t } - cc_cc.claim_timestamp as lapse FROM cc_cc ORDER BY cc_cc.posted_date DESC" )
	# cursor.execute(f"select cc_cc.cc_id, cc_cc.up_id, cc_cc.user_id, cc_cc.claim_timestamp, cc_cc.posted_date, cc_cc.payee, cc_cc.address, cc_cc.amount, cc_cc.ro, cc_cc.invoice, { datetime.datetime.fromtimestamp( cc_cc.claim_timestamp ) } as lapse FROM cc_cc" )
	results = cursor.fetchall()
	context = { 'transactions': results,
				'count':		len( results),
				'computer_nerd': str( request.user )
				 }
	return render( request, 'cc/unlinked.html', context )



@login_required(login_url='login')	#	login → url name
def unlinked_update( request ):
	print('update')
	pk = request.POST['choice']
	cc	= CC.objects.get( pk=pk )
	form = CC_Update_Form( instance=cc )
	print('form')
	template = 'cc/unlinked-update.html'
	context = {
				'cc': cc, 
				'form': form
	 }
	return render( request, template, context )



@login_required(login_url='login')	#	login → url name
def unlinked_update_save(request, pk):
	print('get post')
	cc = CC.objects.get(pk=pk)
	cc.user_id			= str( request.user )
	cc.claim_timestamp	= int( time.time() )
	form = CC_Update_Form( request.POST, instance= cc )
	if form.is_valid():
		form.save()

		form = CC_Form( instance= cc )
		template = 'cc/unlinked-update-save.html'
		context = { 'form': form,
					'user_id': pk
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



def current_datetime(request, message):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.<br>%s</body></html>" % ( now, message )
    return HttpResponse(html)


from ro.filters import RO_Filter
@login_required(login_url='login')	#	login → url name
def po( request ):
	# ro_list = RO.objects.all()
	all = RO.objects.all()		# This needs to be in parenthesis

	filter = RO_Filter( request.GET, queryset=all )
	n = len( filter.qs )
	# cool = len( filter.qs['cost'] )
	cost = 0
	price = 0
	for i in filter.qs:
		cost	+= i.cost
		price	+= i.price

	# tot = filter.qs.objects.annotate(cost=Sum('cost'))

	context = { 'transactions': filter,
					'count':	n,
					'total_cost': round( cost, 2),
					'total_price': round( price, 2)
					 }
	return render( request, 'cc/po.html', context )
