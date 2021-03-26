from cclog.models import CC_log
import django_filters

class CC_Log_Filter( django_filters.FilterSet ):
	# CHOICES = [
	# 	('ascending', 'Ascending')
	# 	('descending', 'Descending')
	# ]
	# ordering = django_filters.ChoiceFilter( label='Ordering', choices=CHOICES, method='filter_by_order' )
	user_id	= django_filters.CharFilter(lookup_expr='icontains')
	vendor 	= django_filters.CharFilter(lookup_expr='icontains')
	# closed	= django_filters.BooleanFilter( default = True )

	class Meta:
		model = CC_log
		fields = ['amount', 'ro1', 'invoice', 'returned', 'credit', 'voided', 'closed']		# Exact
		# fields = {
		# 	'user_id':	['icontains'],
		# 	'vendor':	['icontains'],
		# 	'ro':		['icontains'],
		# 	'invoice':	['icontains'],
		# }