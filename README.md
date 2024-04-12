
## UTIL

### Introduction
This Python package enhances security and functionality in FastAPI applications, featuring modules for authentication, logging, and encryption. These features can be seamlessly integrated into any FastAPI project to boost security and monitoring.

### Installation
Install the package via `pip` with the following command:

```bash
pip install git+https://github.com/Asilimia/ms_util_boilerplate.git

```

This package requires Python 3.6 or higher.

### Configuration
After installing the package, configure it within your FastAPI project by setting up authentication, logging, and encryption in the `config` package.

**Authentication:**
To use authentication, decorate relevant FastAPI endpoints with the authentication decorator provided by the package.

```python
from your_package.auth import requires_auth

@app.get("/protected")
@requires_auth
def protected_route(request: Request,current_user: DecodedToken):
    print(current_user)
    return {"message": "This is a protected route"}
```

**Logging:**
To configure logging throughout your application, use the provided function at the application setup stage.

```python
from configs.logging import configure_app_logging

configure_app_logging(app)
```

**Encryption:**
For encryption, use the encryption decorator to automatically encrypt and decrypt data in specific routes.

```python
from your_package.encryption import encrypt_data

@app.get("/encrypt")
@encrypt_data
def encrypted_route():
    return {"message": "This data is encrypted"}
```

### Usage
Utilize these features in your FastAPI project to enhance security and functionality:
- **Authentication:** Secure your endpoints using the `requires_auth` decorator to manage user access.
- **Logging:** Implement application-wide logging by calling `configure_app_logging` during app initialization.
- **Encryption:** Protect sensitive data with encryption decorators, simplifying the process of encrypting and decrypting data transmitted through specific routes.

### Contributing
Contributions are welcome! If you wish to contribute, please fork the repository and submit a pull request with your proposed changes.

### License
This project is licensed under the MIT License. See the LICENSE file for more details.
