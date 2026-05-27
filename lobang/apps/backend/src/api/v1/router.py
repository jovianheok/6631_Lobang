from fastapi import APIRouter
from src.api.v1.endpoints.deals import router as deals_router  # Go into deals.py, take the variable named router, 
#                                                                 bring it into this file, rename it deals_router

api_router = APIRouter()

api_router.include_router(deals_router, tags=["deals"])        # Take all endpoints inside deals_router and 
#                                                                add them into api_router