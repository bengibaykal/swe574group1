# import django
# from django.core.validators import BaseValidator
# import jsonschema
#
#
# class JSONSchemaValidator(BaseValidator):
#     def compare(self, a, b):
#         try:
#             jsonschema.validate(a, b)
#         except jsonschema.exceptions.ValidationError:
#             raise django.core.exceptions.ValidationError(
#                 '%(value)s failed JSON schema check', params={'value': a})