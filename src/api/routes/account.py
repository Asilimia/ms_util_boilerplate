from src.securities.oauth2 import get_current_user
import fastapi
import loguru

from src.api.dependencies.repository import get_repository
from src.models.schemas.account import (
    AccountInResponse,
    AccountInUpdate,
    AccountWithToken,
)
from src.repository.crud.account import AccountCRUDRepository
from src.utilities.exceptions.database import EntityDoesNotExist, EntityAlreadyExists
from src.utilities.exceptions.http.exc_404 import (
    http_404_exc_id_not_found_request,
)
from ...securities.authorizations.jwt import get_jwt_payload
from ...utilities.exceptions.http.exc_400 import \
    http_400_exc_bad_username_request

router = fastapi.APIRouter(prefix="/accounts", tags=["accounts"])


# @router.get(
#     path="",
#     name="accounts:read-accounts",
#     response_model=list[AccountInResponse],
#     status_code=fastapi.status.HTTP_200_OK,
# )
# async def get_accounts(
#         _: dict = fastapi.Depends(get_current_user),
#         account_repo: AccountCRUDRepository = fastapi.Depends(
#             get_repository(repo_type=AccountCRUDRepository)
#         ),
# ) -> list[AccountInResponse]:
#     """
#     The `get_accounts` function retrieves all accounts from the database and returns
#     them as a list of `AccountInResponse` objects.
#
#     :param _: The underscore (_) parameter is used to indicate that the parameter is
#     intentionally unused. In this case, it is used to indicate that the
#     get_current_user dependency is being used, but its value is not being used in
#     the function body
#     :type _: dict
#     :param account_repo: The `account_repo` parameter is an instance of the
#     `AccountCRUDRepository` class. It is used to interact with the database and
#     perform CRUD operations on the `Account` model. The `get_repository` function is
#     used to get an instance of the `AccountCRUDRepository` class based
#     :type account_repo: AccountCRUDRepository
#     :return: The function `get_accounts` returns a list of `AccountInResponse`
#     objects.
#     """
#     loguru.logger.info("Reading all accounts from database...")
#     db_accounts = await account_repo.read_accounts()
#     db_account_list: list = []
#
#     for db_account in db_accounts:
#         loguru.logger.info(f"Reading account with account_id `{db_account.id}`...")
#         account = AccountInResponse(
#             id=db_account.id,
#             authorized_account=AccountWithToken(
#                 username=db_account.username,
#                 is_verified=db_account.is_verified,
#                 is_active=db_account.is_active,
#                 is_logged_in=db_account.is_logged_in,
#                 created_at=db_account.created_at,
#                 updated_at=db_account.updated_at,
#             ),
#         )
#         db_account_list.append(account)
#     loguru.logger.info("Successfully read all accounts from database!")
#     return db_account_list


@router.get(
    path="/",
    name="accounts:read-account-by-token",
    response_model=AccountInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_account(
        _: dict = fastapi.Depends(get_jwt_payload),
        account_repo: AccountCRUDRepository = fastapi.Depends(
            get_repository(repo_type=AccountCRUDRepository)
        ),
) -> AccountInResponse:
    """
    The `get_account` function retrieves an account from the database by its ID and
    returns it in a response object.

    :param _: The underscore (_) parameter is used to indicate that the parameter is
    intentionally unused. In this case, it is used to indicate that the
    get_current_user dependency is being used, but its value is not needed in the
    function
    :type _: dict
    :param account_repo: The `account_repo` parameter is an instance of the
    `AccountCRUDRepository` class. It is used to interact with the database and
    perform CRUD operations on the `Account` entity
    :type account_repo: AccountCRUDRepository
    :return: The function `get_account` returns an instance of `AccountInResponse`.
    """
    username = _.get("username")
    loguru.logger.info(f"Reading account with account_id `{username}`...")

    try:

        db_account = await account_repo.read_account_by_username(username=username)
    except EntityDoesNotExist as e:
        loguru.logger.error(f"Account with username `{username}` does not exist!")
        raise http_404_exc_id_not_found_request(id=username) from e
    loguru.logger.info(f"Successfully read account with account_id `{username}`!")

    return AccountInResponse(
        id=db_account.id,
        authorized_account=AccountWithToken(
            username=db_account.username,
            is_verified=db_account.is_verified,
            is_active=db_account.is_active,
            is_logged_in=db_account.is_logged_in,
            created_at=db_account.created_at,
            updated_at=db_account.updated_at,
        ),
    )


@router.patch(
    path="/{id}",
    name="accounts:update-account-by-account_id",
    response_model=AccountInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def update_account(
        id: int = fastapi.Path(..., title="The account_id of the account to update."),
        username: str | None = fastapi.Body(None, title="The new username."),
        password: str | None = fastapi.Body(None, title="The new password."),
        _: dict = fastapi.Depends(get_current_user),
        account_repo: AccountCRUDRepository = fastapi.Depends(
            get_repository(repo_type=AccountCRUDRepository)
        ),
) -> AccountInResponse:
    """
    The `update_account` function updates an account with a new username and
    password, and returns the updated account information.
    
    :param id: The `id` parameter is the account_id of the account that needs to be
    updated. It is a required parameter and is passed as a path parameter in the URL
    :type id: int
    :param username: The `username` parameter is the new username that you want to
    update for the account. It is of type `str` and can be `None` if you don't want
    to update the username
    :type username: str | None
    :param password: The `password` parameter is an optional parameter that
    represents the new password for the account. It is of type `str | None`, which
    means it can either be a string or `None`. If a new password is provided, it
    will be used to update the account's password. If `None
    :type password: str | None
    :param _: The underscore (_) parameter is used to indicate that the parameter is
    intentionally unused. In this case, it is used to ignore the `get_current_user`
    dependency, which means that the function does not use the value returned by
    `get_current_user`
    :type _: dict
    :param account_repo: The `account_repo` parameter is an instance of the
    `AccountCRUDRepository` class. It is used to interact with the database and
    perform CRUD operations on the `Account` entity. The `get_repository` function
    is used to get an instance of the `AccountCRUDRepository` class based
    :type account_repo: AccountCRUDRepository
    :return: The function `update_account` returns an instance of
    `AccountInResponse`.
    """
    loguru.logger.info(f"Updating account with account_id `{id}`...")
    account_update = AccountInUpdate(username=username, password=password)
    try:
        updated_db_account = await account_repo.update_account_by_id(
            id=id, account_update=account_update
        )
    except EntityDoesNotExist as e:
        raise http_404_exc_id_not_found_request(id=id) from e
    try:
        await account_repo.is_username_taken(username=username)
    except EntityAlreadyExists as e:
        loguru.logger.error(f"Username `{username}` is taken!")
        raise http_400_exc_bad_username_request(username=username) from e
    return AccountInResponse(
        id=updated_db_account.id,
        authorized_account=AccountWithToken(
            username=updated_db_account.username,
            is_verified=updated_db_account.is_verified,
            is_active=updated_db_account.is_active,
            is_logged_in=updated_db_account.is_logged_in,
            created_at=updated_db_account.created_at,
            updated_at=updated_db_account.updated_at,
        ),
    )


@router.delete(
    path="/{id}",
    name="accounts:delete-account-by-account_id",
    status_code=fastapi.status.HTTP_200_OK,
)
async def delete_account(
        id: int = fastapi.Path(..., title="The account_id of the account to deleted."),
        _: dict = fastapi.Depends(get_current_user),
        account_repo: AccountCRUDRepository = fastapi.Depends(
            get_repository(repo_type=AccountCRUDRepository)
        ),
) -> dict[str, str]:
    """
    The `delete_account` function deletes an account by its ID and returns a
    notification of the deletion result.
    
    :param id: The `id` parameter is the `account_id` of the account that needs to
    be deleted. It is a required parameter and is passed as a path parameter in the
    URL
    :type id: int
    :param _: The underscore (_) is used as a variable name to indicate that the
    value is not going to be used in the function. In this case, it is used to
    indicate that the current user information is not going to be used in the
    function logic
    :type _: dict
    :param account_repo: An instance of the AccountCRUDRepository class, which is
    responsible for interacting with the database and performing CRUD operations on
    the account entity
    :type account_repo: AccountCRUDRepository
    :return: a dictionary with a single key-value pair. The key is "notification"
    and the value is the result of the account deletion operation.
    """
    try:
        deletion_result = await account_repo.delete_account_by_id(id=id)
    except EntityDoesNotExist as e:
        raise http_404_exc_id_not_found_request(id=id) from e

    return {"notification": deletion_result}
