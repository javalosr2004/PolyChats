from fastapi.security import OAuth2PasswordRequestForm
from typing import Union
from fastapi.param_functions import Form

# TODO: import from typing when deprecating Python 3.9
from typing_extensions import Annotated, Doc


class OAuth2Creation(OAuth2PasswordRequestForm):

    def __init__(
        self,
        # grant_type: Annotated[
        #     str,
        #     Form(pattern="password"),
        #     Doc(
        #         """
        #         The OAuth2 spec says it is required and MUST be the fixed string
        #         "password". This dependency is strict about it. If you want to be
        #         permissive, use instead the `OAuth2PasswordRequestForm` dependency
        #         class.
        #         """
        #     ),
        # ],
        firstName: Annotated[
            str,
            Form(),
            Doc(
                """
                `firstName` string.
                `firstName".
                """
            ),
        ],
        lastName: Annotated[
            str,
            Form(),
            Doc(
                """
                `lastName` string. 
                `lastName".
                """
            ),
        ],
        username: Annotated[
            str,
            Form(),
            Doc(
                """
                `username` string. The OAuth2 spec requires the exact field name
                `username`.
                """
            ),
        ],
        password: Annotated[
            str,
            Form(),
            Doc(
                """
                `password` string. The OAuth2 spec requires the exact field name
                `password".
                """
            ),
        ],

        scope: Annotated[
            str,
            Form(),
            Doc(
                """
                A single string with actually several scopes separated by spaces. Each
                scope is also a string.

                For example, a single string with:

                ```python
                "items:read items:write users:read profile openid"
                ````

                would represent the scopes:

                * `items:read`
                * `items:write`
                * `users:read`
                * `profile`
                * `openid`
                """
            ),
        ] = "",
        client_id: Annotated[
            Union[str, None],
            Form(),
            Doc(
                """
                If there's a `client_id`, it can be sent as part of the form fields.
                But the OAuth2 specification recommends sending the `client_id` and
                `client_secret` (if any) using HTTP Basic auth.
                """
            ),
        ] = None,
        client_secret: Annotated[
            Union[str, None],
            Form(),
            Doc(
                """
                If there's a `client_password` (and a `client_id`), they can be sent
                as part of the form fields. But the OAuth2 specification recommends
                sending the `client_id` and `client_secret` (if any) using HTTP Basic
                auth.
                """
            ),
        ] = None,
    ):
        super().__init__(
            username=username,
            password=password,
            scope=scope,
            client_id=client_id,
            client_secret=client_secret,
        )
        self.firstName = firstName
        self.lastName = lastName
