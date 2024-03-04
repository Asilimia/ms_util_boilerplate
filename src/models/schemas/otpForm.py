from pydantic import BaseModel, Field, SecretStr


class OTPVerificationForm(BaseModel):
    username: str
    otp: str


class PasswordResetForm(BaseModel):
    user_name: str = Field(..., description="The  username who is resetting their password.")
    new_password: SecretStr = Field(..., description="The new password the user wants to set.")
    otp: str = Field(..., min_length=6, max_length=6, description="The 6-digit OTP sent to the user for verification.")

    class Config:
        schema_extra = {
            "example": {
                "user_id": 123,
                "new_password": "newSecurePassword123!",
                "otp": "123456"
            }
        }
