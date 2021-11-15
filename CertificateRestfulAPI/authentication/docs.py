"""
Authentication app Swagger docs
"""
from drf_yasg import openapi


class SwaggerDocDicts:
    LOGIN_SUCCESS = {
        "email": "john.doe@example.com",
        "token": "JWT-token "
    }

    LOGIN_FAIL = {
        "field_1 OR non_field_errors": [
            "error_1", "error_2"
        ],
        "field_2": [
            "error_1", "error_2"
        ],
    }

    REGISTER_SUCCESS = {
        "email": "john.doe@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "token": "JWT-token"
    }

    REGISTER_FAIL = {
        "field_1": [
            "error_1", "error_2"
        ],
        "field_2": [
            "error_1", "error_2"
        ]
    }

    REGISTER_PARAMETER = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "email": openapi.Schema(type=openapi.TYPE_STRING,
                                    description='email',
                                    max_length=254),
            "first_name": openapi.Schema(type=openapi.TYPE_STRING,
                                         description='First name',
                                         max_length=128),
            "last_name": openapi.Schema(type=openapi.TYPE_STRING,
                                        description='Last Name',
                                        max_length=128),
            "password": openapi.Schema(type=openapi.TYPE_STRING,
                                       description='Password',
                                       max_length=128),
        })

    LOGIN_PARAMETER = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "email": openapi.Schema(type=openapi.TYPE_STRING,
                                    description='email',
                                    max_length=254),
            "password": openapi.Schema(type=openapi.TYPE_STRING,
                                       description='Password',
                                       max_length=128),
        })


class EndpointDocs:

    LOGIN = {
        "request_body": SwaggerDocDicts.LOGIN_PARAMETER,
        "operation_description": "Insert new CovidCertificate into a database",
        "responses": {
            "200": openapi.Response(
                description="Valid data => login (generate JWT)",
                examples={
                    "application/json": SwaggerDocDicts.LOGIN_SUCCESS
                }
            ),
            "400": openapi.Response(
                description="Invalid data => no login",
                examples={
                    "application/json": SwaggerDocDicts.LOGIN_FAIL
                }
            ),
        }
    }

    REGISTER = {
        "request_body": SwaggerDocDicts.REGISTER_PARAMETER,
        "operation_description": "Edit CovidCertificate record by ID in database",
        "responses": {
            "201": openapi.Response(
                description="Valid data, unique email => register + JWT",
                examples={
                    "application/json": SwaggerDocDicts.REGISTER_SUCCESS
                }
            ),
            "400": openapi.Response(
                description="Invalid input parameters = no registration",
                examples={
                    "application/json": SwaggerDocDicts.REGISTER_FAIL
                }
            ),
        }
    }
