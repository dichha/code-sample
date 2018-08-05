import datetime

from django.db import models
from django.utils import timezone

from django.core.validators import RegexValidator

import re


# Create your models here.
class Question(models.Model):
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')


	def __str__(self):
		return self.question_text

	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.pub_date <= now

	was_published_recently.admin_order_field = 'pub_date'
	was_published_recently.boolean = True
	was_published_recently.short_description = 'Published recently?'
	

class Choice(models.Model):
	'''
	COLOR_CHOICES = (
		('#000000', 'Black'),
		('#FF0000', 'Red'), 
		('#FFFF00', 'Yellow'),
		('#008000', 'Green'), 
		('#0000FF', 'Blue'),

		)
	'''

	question = models.ForeignKey(Question, on_delete = models.CASCADE)
	choice_text = models.CharField(max_length=200)
	'''
	choice_color = models.CharField(max_length=7, 
					choices = COLOR_CHOICES,
					default = '#000000')'''
	choice_color = models.CharField(max_length=7, 
		default = '#000000', 
		validators = [
		RegexValidator(
			regex = '(^#[0-9A-Fa-f]{6}$)',
			message = 'Hex color is invalid.',
			code = 'invalid_color'),
		]
		)
	votes = models.IntegerField(default=0)


	def __str__(self):
		return self.choice_text

	def has_valid_hex_color_format(self):
		hex_pattern =  re.compile('(^#[0-9A-Fa-f]{6}$)')
		return bool(hex_pattern.match(self.choice_color))



