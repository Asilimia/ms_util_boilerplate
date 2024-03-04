import fastapi


from src.api.routes.account import router as account_router

router = fastapi.APIRouter()

router.include_router(router=account_router)
