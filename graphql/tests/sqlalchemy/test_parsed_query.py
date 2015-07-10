from unittest import TestCase

from graphql.tests.sqlalchemy.models import session, Address, Person
from graphql.sqlalchemy.parsed_query import alchemy_data

class TestParsedQueryResults(TestCase):
	def setUp(self):
		self.person = Person(name='new person')
		session.add(self.person)
		self.address = Address(id=1, post_code='94122', person=self.person)
		session.add(self.address)
		session.commit()

	def tearDown(self):
		session.delete(self.person)
		session.delete(self.address)
		session.commit()

	def test_querying_db(self):
		#{'Address': {'fields': [{'child_fields': [], 'field_name': 'street_number'}, {'child_fields': [], 'field_name': 'street_name'}], 'id': '1'}}
		address_query = """Address (id:i) {street_name,street_number}"""
		returned_results = alchemy_data(address_query)

		select_statements = [Address.]
		session.query(Address)



