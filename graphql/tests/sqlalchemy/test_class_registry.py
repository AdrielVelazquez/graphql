from unittest import TestCase

from graphql.tests.sqlalchemy import models
from graphql import base_model_registry, model_registry


class TestBaseRegistry(TestCase):
	def test_class_registry(self):
		self.assertTrue(len(model_registry) == 0)
		base_model_registry(models.Base)
		self.assertTrue(len(model_registry) == 2)

