import typing
from datetime import datetime, timedelta

import sqlalchemy
from sqlalchemy.sql import functions as sqlalchemy_functions

from src.models.db.otp import Otp  # Assuming this is your OTP model
from src.models.schemas.otp import (
    OtpCreate,  # Schema for creating an OTP
    OtpValidate  # Schema for validating an OTP
)
from src.repository.crud.base import BaseCRUDRepository
from src.utilities.exceptions.database import (
    EntityDoesNotExist,
    EntityExpired,
)
from src.utilities.exceptions.otp import OtpInvalidOrExpired


class OtpCRUDRepository(BaseCRUDRepository):
    async def create_otp(self, otp_create: OtpCreate) -> Otp:
        """
        Create and store an OTP for a user.
        """
        new_otp = Otp(
            user_id=otp_create.user_id,
            otp_code=otp_create.otp_code,  # Assuming otp_code is generated beforehand
            expiration=datetime.utcnow() + timedelta(minutes=5)  # OTP expires in 5 minutes
        )

        self.async_session.add(instance=new_otp)
        await self.async_session.commit()
        await self.async_session.refresh(instance=new_otp)

        return new_otp

    async def validate_otp(self, otp_validate: OtpValidate) -> bool:
        """
        Validate an OTP code for a user.
        """
        stmt = sqlalchemy.select(Otp).where(
            Otp.user_id == otp_validate.user_id,
            Otp.otp_code == otp_validate.otp_code,
            Otp.expiration > datetime.utcnow()
        )
        query = await self.async_session.execute(statement=stmt)
        otp = query.scalar()

        if not otp:
            raise OtpInvalidOrExpired("OTP is invalid or expired.")

        # Optionally delete OTP after validation
        await self.delete_otp(otp.id)

        return True

    async def delete_otp(self, otp_id: int) -> None:
        """
        Delete an OTP record.
        """
        stmt = sqlalchemy.delete(Otp).where(Otp.id == otp_id)
        await self.async_session.execute(statement=stmt)
        await self.async_session.commit()

    # Additional methods like updating OTP (if applicable) or reading OTP details can be added here.

# Note: This is a simplified example. You should include error handling, logging, and other practical considerations as in the AccountCRUDRepository class.
