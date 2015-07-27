from unittest import TestCase

from graphql.tests.sqlalchemy.models import session, Address, Person, Base
from graphql.sqlalchemy.parsed_query import alchemy_data
from graphql.sqlalchemy.class_registry import base_model_registry, session_registry

class TestParsedQueryResults(TestCase):
	def setUp(self):
		base_model_registry(Base)
		session_registry(session)
		persons = session.query(Person).all()
		addresses = session.query(Address).all()
		persons.extend(addresses)
		for i in persons:
			session.delete(i)
		self.person = Person(name='new person')
		session.add(self.person)
		self.address = Address(id=99, post_code='94122', person=self.person)
		session.add(self.address)
		session.commit()

	def tearDown(self):
		session.delete(self.person)
		session.delete(self.address)
		session.commit()

	def test_querying_db(self):
		#{'Address': {'fields': [{'child_fields': [], 'field_name': 'street_number'}, {'child_fields': [], 'field_name': 'street_name'}], 'id': '1'}}
		address_query = """Address (id:99) {post_code,street_number}"""
		results = alchemy_data(address_query)
		self.assertEqual(results, [(u'94122', None)])
		address_query = """Address (id:99) {post_code, person {name}}"""
		results = alchemy_data(address_query)
		self.assertEqual(results, [(u'94122', u'new person')])



