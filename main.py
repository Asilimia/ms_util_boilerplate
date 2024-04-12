# main.py
from fastapi import FastAPI
from starlette.requests import Request

from configs.auth import auth_required, DecodedToken

app = FastAPI()


# Protected endpoint that requires authentication
# Protected endpoint that requires authentication
@app.get("/protected")
@auth_required
async def protected_route(request: Request, current_user: DecodedToken):
    return {"message": f"Hello, {current_user.name}! Your email is {current_user.email}."}


# Public endpoint
@app.get("/public")
async def public_route():
    return {"message": "This is a public endpoint."}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
