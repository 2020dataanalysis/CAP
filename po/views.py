from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from po.models import PO

from po.filters import PO_Filter
# @login_required(login_url='login')	#	login → url name
def po( request ):
	# ro_list = RO.objects.all()
	all = PO.objects.all()		# This needs to be in parenthesis

	filter = PO_Filter( request.GET, queryset=all )
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
	return render( request, 'po/po.html', context )



@permission_required( 'admin.can_add_log_entry' )
def killpo( request ):
	#	The following code is deadly so it is commented out.
	# while RO.objects.count():
	# 	print( RO.objects.count() )
	# 	RO.objects.all()[0].delete()

	all = PO.objects.all()
	n	= PO.objects.count()
	context = { 'transactions': all,
					'count':	n }
	return render( request, 'po/index.html', context )