from unittest import TestCase

import graphql

class TestParser(TestCase):
	def test_parser_dict(self):
		string_model = """{User (id:234234) {one {sub1,sub2},two,three,four}}"""
		self.assertTrue(isinstance(graphql.parser(string_model), dict))
		returned_model = {'User': 
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
				'id': '234234'}
			}
		self.assertEqual(graphql.parser(string_model), returned_model)
		string_model = """{User (id:12) {one {one_sub1,one-sub2}, two {sub1}}}"""
		self.assertTrue(isinstance(graphql.parser(string_model), dict))
		returned_model = {'User': 
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
				'id': '12'}
			}
		self.assertEqual(graphql.parser(string_model), returned_model)
		string_model = """{User (ad_name:adriel) {one {one_sub1,one-sub2}, two {sub1}}}"""
		self.assertTrue(isinstance(graphql.parser(string_model), dict))
		returned_model = {'User': 
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
		self.assertEqual(graphql.parser(string_model), returned_model)
		string_model = """{Address (id:1) {street_number, street_name}}"""
		returned_model = {'Address': {'fields': [{'child_fields': [], 'field_name': 'street_number'}, {'child_fields': [], 'field_name': 'street_name'}], 'id': '1'}}
		self.assertEqual(graphql.parser(string_model), returned_model)


	def testing_proper_graphql(self):
		string_model = """{User (id:234234) {one {sub1,sub2},two,three,four}}"""
		self.assertEqual({'User': {'fields': [{'child_fields': [{'child_fields': [], 'field_name': 'sub1'}, {'child_fields': [], 'field_name': 'sub2'}], 'field_name': 'one'}, {'child_fields': [], 'field_name': 'two'}, {'child_fields': [], 'field_name': 'three'}, {'child_fields': [], 'field_name': 'four'}], 'id': '234234'}}, graphql.parser(string_model))

	def testing_alias_graphql(self):
		string_model = """{Adriel: User (id:234234) {one {sub1,sub2},two,three,four}}"""
		self.assertEqual(graphql.parser(string_model), {'alias': 'Adriel', 'User': {'fields': [{'child_fields': [{'child_fields': [], 'field_name': 'sub1'}, {'child_fields': [], 'field_name': 'sub2'}], 'field_name': 'one'}, {'child_fields': [], 'field_name': 'two'}, {'child_fields': [], 'field_name': 'three'}, {'child_fields': [], 'field_name': 'four'}], 'id': '234234'}})
		string_model = """{Adriel: User (id:234234) {alias_attribute: one {sub1,sub2},two,three,four}}"""
		self.assertEqual(graphql.parser(string_model), {'alias': 'Adriel', 'User': {'fields': [{'alias': 'alias_attribute', 'child_fields': [{'child_fields': [], 'field_name': 'sub1'}, {'child_fields': [], 'field_name': 'sub2'}], 'field_name': 'one'}, {'child_fields': [], 'field_name': 'two'}, {'child_fields': [], 'field_name': 'three'}, {'child_fields': [], 'field_name': 'four'}], 'id': '234234'}})

	def testing_multiple_arguements(self):
		string_model = """{User (gender:male,age:27) {one {sub1,sub2},two,three,four}}"""
		self.assertEqual(graphql.parser(string_model), {'User': {'fields': [{'child_fields': [{'child_fields': [], 'field_name': 'sub1'}, {'child_fields': [], 'field_name': 'sub2'}], 'field_name': 'one'}, {'child_fields': [], 'field_name': 'two'}, {'child_fields': [], 'field_name': 'three'}, {'child_fields': [], 'field_name': 'four'}], 'age': '27', 'gender': 'male'}})
		string_model = """{User (gender:male) {one {sub1,sub2},two,three,four}}"""
		self.assertEqual(graphql.parser(string_model), {'User': {'fields': [{'child_fields': [{'child_fields': [], 'field_name': 'sub1'}, {'child_fields': [], 'field_name': 'sub2'}], 'field_name': 'one'}, {'child_fields': [], 'field_name': 'two'}, {'child_fields': [], 'field_name': 'three'}, {'child_fields': [], 'field_name': 'four'}], 'gender': 'male'}})
