# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import  python_2_unicode_compatible	
from django.db import models

from django.utils.timezone import now as timezone_now
# Create your modelsmixins here.

class CreationModificationDateMixin(models.Model):
	created  = models.DateTimeField(editable = False )
	modified = models.DateTimeField(null = True , editable = False )

	def save(self , *args , **kwargs):
		if not self.pk:
			self.created = timezone_now()

		else:
			if not self.created:
				self.created = timezone_now()

			self.modified = timezone_now()

		super(CreationModificationDateMixin , self).save(*args , **kwargs)
	save.alters_data = True


	class Meta:
		abstract = True
		ordering = ['-created' , '-updated']