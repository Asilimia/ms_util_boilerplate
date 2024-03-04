from src.securities.hashing.hash import hash_generator


class PasswordGenerator:
    @property
    def generate_salt(self) -> str:
        return hash_generator.generate_password_salt_hash

    def generate_hashed_password(self, hash_salt: str, new_password: str) -> str:
        """
        The function generates a hashed password using a given hash salt and new
        password.
        
        :param hash_salt: The `hash_salt` parameter is a string that is used as a
        salt value when generating the hashed password. A salt is a random value
        that is added to the password before hashing to make it more secure. It
        helps prevent attackers from using precomputed tables (rainbow tables) to
        quickly crack hashed
        :type hash_salt: str
        :param new_password: The `new_password` parameter is the password that you
        want to hash
        :type new_password: str
        :return: a hashed password as a string.
        """
        return hash_generator.generate_password_hash(
            hash_salt=hash_salt, password=new_password
        )

    def is_password_authenticated(
        self, hash_salt: str, password: str, hashed_password: str
    ) -> bool:
        """
        The function `is_password_authenticated` checks if a given password,
        combined with a hash salt, matches a given hashed password.
        
        :param hash_salt: The `hash_salt` parameter is a string that is used as a
        salt when hashing the password. A salt is a random value that is added to
        the password before hashing to make it more secure
        :type hash_salt: str
        :param password: The `password` parameter is the plain text password that
        the user is trying to authenticate
        :type password: str
        :param hashed_password: The `hashed_password` parameter is a string that
        represents the hashed version of the user's password
        :type hashed_password: str
        :return: a boolean value, indicating whether the password is authenticated
        or not.
        """
        return hash_generator.is_password_verified(
            password=hash_salt + password, hashed_password=hashed_password
        )


def get_pwd_generator() -> PasswordGenerator:
    return PasswordGenerator()


pwd_generator: PasswordGenerator = get_pwd_generator()
