from fastapi import FastAPI,Request
import uvicorn

from configs.logging import configure_app

app = FastAPI()

configure_app(app)

@app.get("/")
async def root(request: Request):
    request.state.app_variable1 = "value1"
    request.state.app_variable2 = "value2"
    request.state.app_customVariable = "Hello World"

    # More variables can be added as needed
    return {"message": "Hello, World"}


if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)
