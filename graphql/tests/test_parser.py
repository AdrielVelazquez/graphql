from unittest import TestCase
from nose.tools import raises

import graphql

class TestParser(TestCase):
	def test_parser_dict(self):
		string_model = """query {User (id:234234) {one {sub1,sub2},two,three,four}}"""
		self.assertTrue(isinstance(graphql.parser(string_model), dict))
		returned_model = {"query": {'User': 
			{
				'fields': 
					[
						{
							'child_fields': 
								[
									{'child_fields': [], 'field_name': 'sub1'}, 
									{'child_fields': [], 'field_name': 'sub2'}
								], 
							'field_name': 'one'
						}, 
						{
							'child_fields': [], 
							'field_name': 'two'
						}, 
						{
							'child_fields': [], 
							'field_name': 'three'
						}, 
						{
							'child_fields': [], 'field_name': 'four'
						}
					], 
				'id': 234234}
			}
		}
		self.assertEqual(graphql.parser(string_model), returned_model)
		string_model = """mutation {User (id:12) {one {one_sub1,one-sub2}, two {sub1}}}"""
		self.assertTrue(isinstance(graphql.parser(string_model), dict))
		returned_model = {"mutation": {'User': 
			{
				'fields': 
					[
						{
							'child_fields': 
								[
									{'child_fields': [], 'field_name': 'one_sub1'}, 
									{'child_fields': [], 'field_name': 'one-sub2'}
								], 
							'field_name': 'one'
						}, 
						{
							'child_fields': 
								[
									{
										'child_fields': [], 
										'field_name': 'sub1'
									}
								], 
							'field_name': 'two'
						}
					], 
				'id': 12}
			}
		}
		self.assertEqual(graphql.parser(string_model), returned_model)
		string_model = """query {User (ad_name:"adriel") {one {one_sub1,one-sub2}, two {sub1}}}"""
		self.assertTrue(isinstance(graphql.parser(string_model), dict))
		returned_model = {"query": {'User': 
			{
				'fields': 
					[
						{
							'child_fields': 
								[
									{'child_fields': [], 'field_name': 'one_sub1'}, 
									{'child_fields': [], 'field_name': 'one-sub2'}
								], 
							'field_name': 'one'
						}, 
						{
							'child_fields': 
								[
									{
										'child_fields': [], 
										'field_name': 'sub1'
									}
								], 
							'field_name': 'two'
						}
					], 
				'ad_name': 'adriel'}
			}
		}
		self.assertEqual(graphql.parser(string_model), returned_model)
		string_model = """query {Address (id:1) {street_number, street_name}}"""
		returned_model = {"query": {'Address': {'fields': [{'child_fields': [], 'field_name': 'street_number'}, {'child_fields': [], 'field_name': 'street_name'}], 'id': 1}}}
		self.assertEqual(graphql.parser(string_model), returned_model)


	def testing_proper_graphql(self):
		string_model = """query {User (id:234234) {one {sub1,sub2},two,three,four}}"""
		self.assertEqual({"query": {'User': {'fields': [{'child_fields': [{'child_fields': [], 'field_name': 'sub1'}, {'child_fields': [], 'field_name': 'sub2'}], 'field_name': 'one'}, {'child_fields': [], 'field_name': 'two'}, {'child_fields': [], 'field_name': 'three'}, {'child_fields': [], 'field_name': 'four'}], 'id': 234234}}}, graphql.parser(string_model))

	def testing_alias_graphql(self):
		string_model = """query {Adriel: User (id:234234) {one {sub1,sub2},two,three,four}}"""
		self.assertEqual(graphql.parser(string_model), {"query": {'alias': 'Adriel', 'User': {'fields': [{'child_fields': [{'child_fields': [], 'field_name': 'sub1'}, {'child_fields': [], 'field_name': 'sub2'}], 'field_name': 'one'}, {'child_fields': [], 'field_name': 'two'}, {'child_fields': [], 'field_name': 'three'}, {'child_fields': [], 'field_name': 'four'}], 'id': 234234}}})
		string_model = """query {Adriel: User (id:234234) {alias_attribute: one {sub1,sub2},two,three,four}}"""
		self.assertEqual(graphql.parser(string_model), {"query": {'alias': 'Adriel', 'User': {'fields': [{'alias': 'alias_attribute', 'child_fields': [{'child_fields': [], 'field_name': 'sub1'}, {'child_fields': [], 'field_name': 'sub2'}], 'field_name': 'one'}, {'child_fields': [], 'field_name': 'two'}, {'child_fields': [], 'field_name': 'three'}, {'child_fields': [], 'field_name': 'four'}], 'id': 234234}}})

	def testing_multiple_arguements(self):
		string_model = """query {User (gender:"male",age:27) {one {sub1,sub2},two,three,four}}"""
		self.assertEqual(graphql.parser(string_model), {"query": {'User': {'fields': [{'child_fields': [{'child_fields': [], 'field_name': 'sub1'}, {'child_fields': [], 'field_name': 'sub2'}], 'field_name': 'one'}, {'child_fields': [], 'field_name': 'two'}, {'child_fields': [], 'field_name': 'three'}, {'child_fields': [], 'field_name': 'four'}], 'age': 27, 'gender': 'male'}}})
		string_model = """query {User (gender:"male") {one {sub1,sub2},two,three,four}}"""
		self.assertEqual(graphql.parser(string_model), {"query": {'User': {'fields': [{'child_fields': [{'child_fields': [], 'field_name': 'sub1'}, {'child_fields': [], 'field_name': 'sub2'}], 'field_name': 'one'}, {'child_fields': [], 'field_name': 'two'}, {'child_fields': [], 'field_name': 'three'}, {'child_fields': [], 'field_name': 'four'}], 'gender': 'male'}}})

	def testing_arguements_as_types(self):
		#age list
		#string_model = """query {User (age:[27,28,35,60]) {one {sub1,sub2},two,three,four}}"""
		#self.assertEqual(graphql.parser(string_model), {"query": {'User': {'fields': [{'child_fields': [{'child_fields': [], 'field_name': 'sub1'}, {'child_fields': [], 'field_name': 'sub2'}], 'field_name': 'one'}, {'child_fields': [], 'field_name': 'two'}, {'child_fields': [], 'field_name': 'three'}, {'child_fields': [], 'field_name': 'four'}], 'age': [27, 28, 35, 60]}}})
		#Mixed types
		string_model = """query {User (age:[27,"twenty",35,60]) {one {sub1,sub2},two,three,four}}"""
		self.assertEqual(graphql.parser(string_model), {"query": {'User': {'fields': [{'child_fields': [{'child_fields': [], 'field_name': 'sub1'}, {'child_fields': [], 'field_name': 'sub2'}], 'field_name': 'one'}, {'child_fields': [], 'field_name': 'two'}, {'child_fields': [], 'field_name': 'three'}, {'child_fields': [], 'field_name': 'four'}], 'age': [27, "twenty", 35, 60]}}})

	def testing_inner_ids_and_criterias(self):
		string_model = """query {User (gender:"male",age:27) {one (id:123) {sub1,sub2},two,three,four}}"""
		self.assertEqual(graphql.parser(string_model), {"query": {'User': {'fields': [{'child_fields': [{'child_fields': [], 'field_name': 'sub1'}, {'child_fields': [], 'field_name': 'sub2'}], 'field_name': 'one', 'id': 123}, {'child_fields': [], 'field_name': 'two'}, {'child_fields': [], 'field_name': 'three'}, {'child_fields': [], 'field_name': 'four'}], 'age': 27, 'gender': 'male'}}})

	def testing_no_attributes(self):
		string_model = """query {User {one (id:123) {sub1,sub2},two,three,four}}"""
		self.assertEqual(graphql.parser(string_model), {"query": {'User': {'fields': [{'child_fields': [{'child_fields': [], 'field_name': 'sub1'}, {'child_fields': [], 'field_name': 'sub2'}], 'field_name': 'one', 'id': 123}, {'child_fields': [], 'field_name': 'two'}, {'child_fields': [], 'field_name': 'three'}, {'child_fields': [], 'field_name': 'four'}]}}})
		string_model = """query {User{one(id:123){sub1,sub2},two,three,four}}"""
		self.assertEqual(graphql.parser(string_model), {"query": {'User': {'fields': [{'child_fields': [{'child_fields': [], 'field_name': 'sub1'}, {'child_fields': [], 'field_name': 'sub2'}], 'field_name': 'one', 'id': 123}, {'child_fields': [], 'field_name': 'two'}, {'child_fields': [], 'field_name': 'three'}, {'child_fields': [], 'field_name': 'four'}]}}})

	def testing_all_users(self):
		string_model = """query {User}"""
		self.assertEqual(graphql.parser(string_model), {"query": {'User': {'fields': []}}})

	def testing_operation_parsing(self):
		string_model = """query {User}"""
		self.assertEqual(graphql.parser(string_model), {'query': {'User': {'fields': []}}})
		string_model = """mutation {User}"""
		self.assertEqual(graphql.parser(string_model), {'mutation': {'User': {'fields': []}}})
		string_model = """query {User {one (id:123) {sub1,sub2},two,three,four}}"""
		self.assertEqual(graphql.parser(string_model), {"query": {'User': {'fields': [{'child_fields': [{'child_fields': [], 'field_name': 'sub1'}, {'child_fields': [], 'field_name': 'sub2'}], 'field_name': 'one', 'id': 123}, {'child_fields': [], 'field_name': 'two'}, {'child_fields': [], 'field_name': 'three'}, {'child_fields': [], 'field_name': 'four'}]}}})

	def testing_fragments(self):
		string_model = """query {User (id:234234) {one {...Gibberish},two,three,four}} fragment Gibberish on User {sub1, sub2}"""
		returned_model = {"query": {'User': 
			{
				'fields': 
					[
						{
							'child_fields': 
								[
									{'child_fields': [], 'field_name': 'sub1'}, 
									{'child_fields': [], 'field_name': 'sub2'}
								], 
							'field_name': 'one'
						}, 
						{
							'child_fields': [], 
							'field_name': 'two'
						}, 
						{
							'child_fields': [], 
							'field_name': 'three'
						}, 
						{
							'child_fields': [], 'field_name': 'four'
						}
					], 
				'id': 234234}
			}
		}
		self.assertEqual(graphql.parser(string_model), returned_model)

	def testing_multiple_fragments(self):
		string_model = """query {User (id:234234) {one {...Gibberish},two {...SecondGibberish},three,four}} fragment Gibberish on User {sub1, sub2} fragment SecondGibberish on User {supersub_1, supersub_2}"""
		returned_model = {"query": {'User': 
			{
				'fields': 
					[
						{
							'child_fields': 
								[
									{'child_fields': [], 'field_name': 'sub1'}, 
									{'child_fields': [], 'field_name': 'sub2'}
								], 
							'field_name': 'one'
						}, 
						{
							'child_fields': 
								[
									{'child_fields': [], 'field_name': 'supersub_1'}, 
									{'child_fields': [], 'field_name': 'supersub_2'}
								], 
							'field_name': 'two'
						}, 
						{
							'child_fields': [], 
							'field_name': 'three'
						}, 
						{
							'child_fields': [], 'field_name': 'four'
						}
					], 
				'id': 234234}
			}
		}
		self.assertEqual(graphql.parser(string_model), returned_model)

	@raises(AssertionError)
	def test_fragment_exceptions(self):
		string_model = """query {User {...Gibbberish}} fragment Gibberish on Advertiser {id, name}"""
		graphql.parser(string_model)
		string_model = """query {User {...Gibbberish}} fragment Gibberish on User {id, name}"""
		graphql.parser(string_model)

	def test_nested_fragment(self):
		string_model = """query {Advertiser {...Gibberish}} fragment Gibberish on Advertiser {id, name, ...nested_frag} fragment nested_frag on Advertiser {ctr, vcr}"""
		self.assertEqual(graphql.parser(string_model), {'query': {'Advertiser': {'fields': [{'child_fields': [], 'field_name': 'id'}, {'child_fields': [], 'field_name': 'name'}, {'child_fields': [], 'field_name': 'ctr'}, {'child_fields': [], 'field_name': 'vcr'}]}}})

	def test_inline_fragment(self):
		string_model = """query {Advertiser {... on Campaign {line_items, name}}}"""
		self.assertEqual(graphql.parser(string_model), {'query': {'Advertiser': {'fields': [{'child_fields': [], 'field_name': 'line_items', 'polymorphic_target': 'Campaign'}, {'child_fields': [], 'field_name': 'name', 'polymorphic_target': 'Campaign'}]}}})

	def test_fragments_not_present(self):
		string_model = """query {User {...Gibberish}} fragment Gibberish on Advertiser {id, name}"""
		self.assertEqual(graphql.parser(string_model), {'query': {'User': {'fields': [{'polymorphic_target': 'Advertiser', 'field_name': 'id', 'child_fields': []}, {'polymorphic_target': 'Advertiser', 'field_name': 'name', 'child_fields': []}]}}})
		string_model = """query {User {age, created, ...Gibberish}} fragment Gibberish on Advertiser {id, name}"""
		self.assertEqual(graphql.parser(string_model), {'query': {'User': {'fields': [{'child_fields': [], 'field_name': 'age'}, {'child_fields': [], 'field_name': 'created'}, {'polymorphic_target': 'Advertiser', 'field_name': 'id', 'child_fields': []}, {'polymorphic_target': 'Advertiser', 'field_name': 'name', 'child_fields': []}]}}})

	def test_mass_varible(self):
		string_model = """query {Advertiser ($name:'adriel') {id ($order_by:'average'), date}}"""
		self.assertEqual({'query': {'Advertiser': {'fields': [{'field_name': 'id', 'child_fields': [], 'order_by': 'average'}, {'child_fields': [], 'field_name': 'date'}], 'name': 'adriel'}}}, graphql.parser(string_model))


	def test_varible_assignment(self):
		string_model = """query {Advertiser ($name:'adriel') {id (user:$name), date}}"""
		self.assertEqual(graphql.parser(string_model), {'query': {'Advertiser': {'fields': [{'child_fields': [], 'field_name': 'id', 'user': 'adriel'}, {'child_fields': [], 'field_name': 'date'}], 'name': 'adriel'}}})
