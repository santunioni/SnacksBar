from fastapi import APIRouter

from snacksbar.products.routes import categories, drinks, ingredients, snacks

router = APIRouter(prefix="/products")
router.include_router(categories.router)
router.include_router(snacks.router)
router.include_router(drinks.router)
router.include_router(ingredients.router)
