# https://www.youtube.com/watch?v=BppyfPye8eo
import csv, io, ast, time, datetime, django_filters
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, Http404
from django.http import HttpResponse, HttpResponseRedirect
from cc.models import CC
# from ro.models import RO
from po.models import PO
from cc.forms import CC_Form, CC_Update_Form
from django.contrib.auth.decorators import permission_required
from django.db import connection
from cclog.models import CC_log
from django.contrib.auth.models import User
from django.core.mail import send_mail


def home( request ):
	return render( request, 'ie/home.html', {} )

def get_post(request):
	s = ""
	for key in request.POST:
		value = request.POST[key]
		s += key + ':' + value + '<br>'

	return s


# @permission_required( 'admin.can_add_log_entry' )
def upload( request ):
	print( f'[{request.user}]' )
	template	= 'ie/upload.html'
	if request.method == 'GET':
		return render( request, template, {} )

	if request.FILES.get('file') == None:
		context = { 'message': 'You did not select a file.'}
		return render( request, template, context )

	csv_file = request.FILES['file']
	if not csv_file.name.endswith('.csv'):
		context = { 'message': 'This is not a csv file.'}
		return render( request, template, context )

	data_set = csv_file.read().decode('UTF-8')
	io_string = io.StringIO( data_set )
	# next( io_string )		#	To skip the first record.

	cool = request.POST.get('up_type')
	print( cool )
	if cool == None:
		context = {
			'message': 'You did not select a data structure type.'
		}
		return render( request, template, context )

	if request.POST['up_type'] == 'user':
		message = 'User'
		print( 'You selected User')
		i_old, i_new = import_user( request, io_string )

	if request.POST['up_type'] == 'log':
		message = 'Log'
		print( 'You selected Log')
		i_old, i_new = import_log( request, io_string )

	if request.POST['up_type'] == 'po':
		message = 'Purchase Order'
		print( 'You selected Purchase Order')
		i_old, i_new = import_po( request, io_string )
	
	if request.POST['up_type'] == 'cc':
		message = 'Credit Card'
		print( 'You selected Credit Card')
		i_old, i_new = import_cc( request, io_string )

	context =	{
					'computer_nerd': str( request.user ),
					'message': message,
					'i_old': i_old,
					'i_new': i_new
				}
	return render( request, template, context )






def import_user( request, io_string ):
	next( io_string )		#	To skip the first record.
	i_new = 0
	i_old = 0
	status = ''

	for column in csv.reader( io_string, delimiter=',', quotechar='"'):
		# i	= User.objects.create_user(
		i	= User(
			username	= column[0],
			password	= column[1],
			first_name	= column[2],
			email		= column[3]
			)
		
		i.set_password( column[1] )

		if User.objects.filter(pk=i.id).exists():
			i_old += 1
			s = f'------{i_old} { i }'
		else:
			i_new += 1
			s = f'++++++{i_new} { i }'
			i.save(force_insert=True)

		print( s )
		# status += s
		# i_old = 0
		# i_new += 1

	return i_old, i_new



def import_log( request, io_string ):
	i_new = 0
	i_old = 0
	status = ''

	for column in csv.reader( io_string, delimiter=',', quotechar='"'):
		i	= CC_log(
			log_id			= column[0],
			user_id			= column[1],
			cc_id			= column[2],

			transaction_date= column[3],
			vendor			= column[4],
			amount			= (column[5], 0)[not column[5]],
			# ro1				= column[6]
			# ro2				= column[7],
			# ro3				= column[8],
			# ro4				= column[9],
			# ro5				= column[10],
			ro1				= (column[6], 0)[not column[6]],
			ro2				= (column[7], 0)[not column[7]],
			ro3				= (column[8], 0)[not column[8]],
			ro4				= (column[9], 0)[not column[9]],
			ro5				= (column[10], 0)[not column[10]],

			invoice			= column[11],
			returned		= column[12],
			credit			= column[13],
			voided			= column[14],
			closed			= column[15],
			start			= column[16],
			stop			= column[17]
			)


		if CC_log.objects.filter(pk=i.id).exists():
			i_old += 1
			s = f'------{i_old} { i }'
		else:
			i_new += 1
			s = f'++++++{i_new} { i }'
			i.save(force_insert=True)

		print( s )

	# all = CC_log().objects.all()

	all = CC_log.objects.filter( )
	for i in all:
		print( f'{i.id} → {i.log_id}')
		i.log_id = i.id
		i.save()


	return i_old, i_new






def import_po( request, io_string ):
	i_new = 0
	i_old = 0
	status = ''
	next( io_string )		#	To skip the first record.

	for column in csv.reader( io_string, delimiter=',', quotechar='"'):
		i = PO(
			po_id		= column[12],
			up_id		= request.user,
			date		= column[0],
			ro			= column[1],
			invoice		= column[2],
			category	= column[3],
			vendor		= column[4],
			qty			= column[5],
			price		= float( column[6].replace(',','') ),
			cost		= float( column[7].replace(',','') ),
			transferred	= column[8],
			payables	= column[9],
			credit		= column[10],
			voided		= column[11],
			closed		= column[19]
		)

		if PO.objects.filter(pk=i.po_id).exists():
			i_old += 1
			s = f'------{i_old} { i }'
		else:
			i_new += 1
			s = f'++++++{i_new} { i }'
			i.save(force_insert=True)

		print( s )
		# status += s

	return i_old, i_new



def import_cc( request, io_string ):
	next( io_string )		#	To skip the first record.
	i_new = 0
	i_old = 0
	status = ''

	for column in csv.reader( io_string, delimiter=',', quotechar='"'):
		i = CC(
			cc_id			= column[1],
			up_id			= request.user,
			user_id			= '',
			claim_timestamp = 0,
			posted_date		= column[0],
			payee			= column[2],
			address			= column[3],
			amount			= -1 * float( column[4] ),
			ro 				= '',
			invoice			= ''
		)

		if CC.objects.filter(pk=i.cc_id).exists():
			i_old += 1
			s = f'------{i_old} { i }'
		else:
			i_new += 1
			s = f'++++++{i_new} { i }'
			i.save(force_insert=True)

		print( s )
		# status += s

	return i_old, i_new




def current_datetime(request, message):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.<br>%s</body></html>" % ( now, message )
    return HttpResponse(html)





#	================================================================
#	==========================	DOWNLOADS	========================
#	================================================================

def download_log(request):
	# Create the HttpResponse object with the appropriate CSV header.
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="log.csv"'
	writer = csv.writer(response)

	records = CC_log.objects.all()
	for i in records.iterator():
		print( i.log_id )
		writer.writerow([ i.log_id, i.user_id, i.cc_id, i.transaction_date, i.vendor, i.amount, i.ro1, i.ro2, i.ro3, i.ro4, i.ro5, i.invoice, i.returned, i.credit, i.voided, i.closed, i.start, i.stop ] )
	return response
