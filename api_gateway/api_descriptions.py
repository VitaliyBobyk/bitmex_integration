from drf_yasg import openapi
from rest_framework.settings import api_settings

ACCOUNT_PARAMETER = openapi.Parameter(
    'account',
    openapi.IN_HEADER,
    required=True,
    description="Account name",
    type=openapi.TYPE_STRING
)

BAD_SERIALIZER_VALIDATION_RESPONSES = openapi.Schema(
    'Validation Error',
    type=openapi.TYPE_OBJECT,
    properties={
        'errors': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description='error messages for each field that triggered a validation error',
            additional_properties=openapi.Schema(
                description='A list of error messages for the field',
                type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)
            )),
        api_settings.NON_FIELD_ERRORS_KEY: openapi.Schema(
            description='List of validation errors not related to any field',
            type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)
        ),
    }
)


BOOL_RESPONSE = openapi.Schema(
    'Response with bool value: success: True/False',
    type=openapi.TYPE_OBJECT,
    properties={
        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Bool value'),
    }
)
