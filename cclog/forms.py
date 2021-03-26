from django import forms
from cclog.models import CC_log


class CC_New_Log_Form( forms.ModelForm ):
	class Meta:
		model 	= CC_log
		#	sans voided, could add user_id & disable.
		fields	= [									'transaction_date', 'vendor', 'amount', 'ro1', 'ro2', 'ro3', 'ro4', 'ro5', 'invoice', 'returned', 'credit', 		  'closed']
		

	# def __init__( self, *args, **kwargs ):
	# 	super().__init__( *args, **kwargs )
	# 	self.fields['vendor'].queryset = ['a', 'b', 'c', 'qbert']


class CC_Log_Form( forms.ModelForm ):
	class Meta:
		model 	= CC_log
		fields	= ['log_id', 'user_id', 			'transaction_date', 'vendor', 'amount', 'ro1', 'ro2', 'ro3', 'ro4', 'ro5', 'invoice', 'returned', 'credit', 'voided', 'closed']


class CC_Log_Form2( forms.ModelForm ):
	class Meta:
		model 	= CC_log
		fields	= ['log_id', 'user_id', 'cc_id',	'transaction_date', 'vendor', 'amount', 'ro1', 'ro2', 'ro3', 'ro4', 'ro5', 'invoice', 'returned', 'credit', 'voided', 'closed']
