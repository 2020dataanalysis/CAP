from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from vendor.models import VendorModel
from vendor.filters import Vendor_Filter

# @login_required(login_url='login')	#	login → url name
def view( request ):
	all = VendorModel.objects.all()		# This needs to be in parenthesis
	filter = Vendor_Filter( request.GET, queryset=all )
	n = len( filter.qs )

	cw = [1, 15, 5, 15, 10, 1, 2, 3, 3, 5, 5, 5, 1]

	context = { 'transactions': filter,
					'count':	n,
					'cw': cw
					 }
	return render( request, 'vendor/view.html', context )

