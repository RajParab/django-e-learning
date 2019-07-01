from django.db import models
from django.core.exceptions import ObjectDoesNotExist

"""This file is used to assign a oitive value for each Course
This takes that if not positive Integer is already associated to the model 
Then it allots one to it bu uing uery Set
"""


class OrderField(models.PositiveIntegerField):

	def __init__(self,for_fields=None,*args,**kwargs):
		self.for_fields=for_fields
		super (OrderField,self).__init__(*args,**kwargs)

	def pre_save(self, model_instance,add):
		if getattr(model_instance,self.attname) is None:
			try:
				qs=self.model.objects.all()

				if self.for_fields:
					# filter by objects with the same field values
					# for the fields in "for_fields"
					query={fields:getattr(model_instance,fields) for fields in self.for_fields}
					qs=qs.filter(**query)
				# get the order of the last item
				last_value=qs.latest(self.attname)
				value=last_value.order+1
			except ObjectDoesNotExist:
				value=0

			setattr(model_instance,self.attname,value)
			return value

		else:
			return super(OrderField,self).pre_save(model_instance,add)