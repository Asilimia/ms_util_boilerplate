from datetime import datetime, timedelta

import loguru
import typing

import sqlalchemy
from sqlalchemy.sql import functions as sqlalchemy_functions

from src.models.db.account import Account
from src.models.schemas.account import (
    AccountInCreate,
    AccountInLogin,
    AccountInUpdate,
)
from src.repository.crud.base import BaseCRUDRepository
from src.securities.hashing.password import pwd_generator
from src.securities.verifications.credentials import credential_verifier
from src.utilities.exceptions.database import (
    EntityAlreadyExists,
    EntityDoesNotExist, TooManyFailedAttempts,
)
from src.utilities.exceptions.password import PasswordDoesNotMatch


class AccountCRUDRepository(BaseCRUDRepository):
    async def create_account(self, account_create: AccountInCreate,device_id) -> Account:
        """
        The function creates a new account with a username and password, generates a
        hash salt, and sets the hashed password.
        
        :param account_create: The parameter `account_create` is of type
        `AccountInCreate`, which is likely a data model or class representing the
        data needed to create a new account. It probably contains properties such as
        `username` and `password`
        :type account_create: AccountInCreate
        """
        new_account = Account(
            username=account_create.username,
            is_logged_in=True,
        )
        new_account.deviceUUID = device_id

        new_account.set_hash_salt(hash_salt=pwd_generator.generate_salt)

        new_account.set_hashed_password(
            hashed_password=pwd_generator.generate_hashed_password(
                hash_salt=new_account.hash_salt,
                new_password=account_create.password,
            )
        )

        self.async_session.add(instance=new_account)
        await self.async_session.commit()
        await self.async_session.refresh(instance=new_account)

        return new_account  # type: ignore

    async def read_accounts(self) -> typing.Sequence[Account]:
        """
        The function reads all accounts from a database using SQLAlchemy and returns
        them as a list of Account objects.
        :return: a sequence of Account objects.
        """
        stmt = sqlalchemy.select(Account)
        query = await self.async_session.execute(statement=stmt)
        return query.scalars().all()

    async def read_account_by_id(self, id: int) -> Account:
        """
        The function reads an account from a database by its ID and returns it.
        
        :param id: The `id` parameter is an integer that represents the account ID.
        It is used to identify the specific account that needs to be read from the
        database
        :type id: int
        :return: an instance of the `Account` class.
        """
        loguru.logger.info(f"Reading account with account_id `{id}`")
        stmt = sqlalchemy.select(Account).where(Account.id == id)
        query = await self.async_session.execute(statement=stmt)
        account = query.scalar()
        if not account:
            loguru.logger.error(f"Account with account_id `{id}` does not exist!")
            raise EntityDoesNotExist("Account with account_id `{account_id}` does not exist!")
        loguru.logger.info(f"Successfully read account with account_id `{query}`!")
        return account  # type: ignore

    async def read_account_by_username(self, username: str) -> Account:
        """
        The function reads an account from the database based on the provided
        username and returns it.
        
        :param username: The `username` parameter is a string that represents the
        username of the account that you want to retrieve
        :type username: str
        :return: the result of the query, which is an instance of the Account class.
        """
        stmt = sqlalchemy.select(Account).where(Account.username == username)
        query = await self.async_session.execute(statement=stmt)

        if not query:
            raise EntityDoesNotExist(
                "Account with username `{username}` does not exist!"
            )

        return query.scalar()  # type: ignore

    async def read_user_by_password_authentication(
            self, account_login: AccountInLogin,device_id
    ) -> Account:
        """
        The function reads a user account from a database using password
        authentication and returns the account if the username and password match.
        
        :param account_login: The `account_login` parameter is an instance of the
        `AccountInLogin` class. It represents the login information provided by the
        user, including the `username` and `password` fields
        :type account_login: AccountInLogin
        :return: the `db_account` object.
        """
        stmt = sqlalchemy.select(Account).where(
            Account.username == account_login.username,
        )
        query = await self.async_session.execute(statement=stmt)
        db_account = query.scalar()

        # check if  the account device id is the same as the one provided
        if db_account.deviceUUID != device_id:
            raise EntityDoesNotExist("Wrong device id!")

        if not db_account:
            raise EntityDoesNotExist("Wrong username!")

        if db_account.banUntil and db_account.banUntil > datetime.now():
            raise TooManyFailedAttempts(f'Account is locked! until {db_account.banUntil}')

        if db_account.failedLoginAttempts >= 3:
            # ban the account for an hour
            db_account.banUntil = datetime.now() + timedelta(hours=1)
            await self.async_session.commit()
            raise TooManyFailedAttempts(f'Account is locked! until {db_account.banUntil}')

        if not pwd_generator.is_password_authenticated(hash_salt=db_account.hash_salt, password=account_login.password,
                                                       hashed_password=db_account.hashed_password):  # type: ignore
            # add failed login attempts
            db_account.failedLoginAttempts += 1
            await self.async_session.commit()

            raise PasswordDoesNotMatch("Password does not match!")

        return db_account  # type: ignore

    async def update_account_by_id(
            self, id: int, account_update: AccountInUpdate
    ) -> Account:
        """
        The function `update_account_by_id` updates an account in the database based
        on the provided ID and account update data.
        
        :param id: The `id` parameter is an integer that represents the unique
        identifier of the account that needs to be updated
        :type id: int
        :param account_update: The `account_update` parameter is an instance of the
        `AccountInUpdate` class. It contains the updated data for the account
        :type account_update: AccountInUpdate
        :return: an instance of the `Account` class.
        """
        new_account_data = account_update.model_dump()

        select_stmt = sqlalchemy.select(Account).where(Account.id == id)
        query = await self.async_session.execute(statement=select_stmt)
        update_account = query.scalar()

        if not update_account:
            raise EntityDoesNotExist(f"Account with account_id `{id}` does not exist!")  # type: ignore

        update_stmt = sqlalchemy.update(table=Account).where(Account.id == update_account.id).values(
            updated_at=sqlalchemy_functions.now())  # type: ignore

        if new_account_data["username"]:
            update_stmt = update_stmt.values(username=new_account_data["username"])

        if new_account_data["password"]:
            update_account.set_hash_salt(hash_salt=pwd_generator.generate_salt)  # type: ignore
            update_account.set_hashed_password(
                hashed_password=pwd_generator.generate_hashed_password(hash_salt=update_account.hash_salt,
                                                                       new_password=new_account_data[
                                                                           settings.RABBITMQ_DEFAULT_PASS]))  # type: ignore

        await self.async_session.execute(statement=update_stmt)
        await self.async_session.commit()
        await self.async_session.refresh(instance=update_account)

        return update_account  # type: ignore

    async def delete_account_by_id(self, id: int) -> str:
        """
        The function `delete_account_by_id` deletes an account from the database
        based on its ID.
        
        :param id: The `id` parameter is an integer that represents the unique
        identifier of the account that needs to be deleted
        :type id: int
        """
        select_stmt = sqlalchemy.select(Account).where(Account.id == id)
        query = await self.async_session.execute(statement=select_stmt)
        delete_account = query.scalar()

        if not delete_account:
            raise EntityDoesNotExist(f"Account with account_id `{id}` does not exist!")  # type: ignore

        stmt = sqlalchemy.delete(table=Account).where(Account.id == delete_account.id)

        await self.async_session.execute(statement=stmt)
        await self.async_session.commit()

        return f"Account with account_id '{id}' is successfully deleted!"

    async def is_username_taken(self, username: str) -> bool:
        """
        The function checks if a given username is already taken in the database and
        raises an exception if it is not available.
        
        :param username: The `username` parameter is a string that represents the
        username to check if it is already taken or not
        :type username: str
        :return: a boolean value.
        """
        username_stmt = (
            sqlalchemy.select(Account.username)
            .select_from(Account)
            .where(Account.username == username)
        )
        username_query = await self.async_session.execute(username_stmt)
        db_username = username_query.scalar()

        if not credential_verifier.is_username_available(username=db_username):
            raise EntityAlreadyExists(f"The username `{username}` is already taken!")  # type: ignore

        return True

    async def update_password(self, account, new_password):
        user = account
        user.set_hash_salt(hash_salt=pwd_generator.generate_salt)
        user.set_hashed_password(
            hashed_password=pwd_generator.generate_hashed_password(hash_salt=user.hash_salt, new_password=new_password))
        await self.async_session.commit()
