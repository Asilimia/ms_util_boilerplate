from fastapi import FastAPI
from starlette.requests import Request

from configs.auth import auth_required, DecodedToken
from configs.logging import configure_app

app = FastAPI(title="Secure API", version="0.1.0", description="This is a secure API.")

configure_app(app)


@app.get("/")
@auth_required
async def read_root(request: Request, current_user: DecodedToken):
    request.state.app_var = "Hello World!"
    request.state.app_mpesa_code = "123456"
    print(current_user)
    return {"message": "Hello World!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
