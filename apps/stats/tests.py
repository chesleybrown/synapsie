from django.utils import unittest
from django.test import TestCase

from django.contrib.auth.models import User
from apps.stats import services as StatService
from apps.records.models import Record


class StatTest(unittest.TestCase):
	
	def setUp(self):
		self.user = User.objects.create(first_name="Chesley", last_name="Brown")
		#self.records = Record.objects.create(first_name="Chesley", last_name="Brown")
	
	def test_get_weekly(self):
		"""
		Tests that 1 + 1 always equals 2.
		"""
		
		
		self.assertEqual(1 + 1, 2)
