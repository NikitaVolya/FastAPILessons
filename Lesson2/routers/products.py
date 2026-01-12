
from fastapi import APIRouter, Query

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/search")
async def search_product(page: int = Query( 1, ge=1),
                         limit: int = Query(10, le=10, ge=1),
                         search: str = Query(None, min_length=3)):

    products = ["Xbox Seria X", "PC Samurai", "Camera", "Nintendo switch 2", "Xiaomi readme note 10", "Xbox One"]

    return {
        "page": page,
        "limit": limit,
        "items": list(
                    filter(
                        lambda item: search is None or \
                                     search.replace(" ", "").lower() in item.replace(" ", "").lower(),
                        products
                    )
        )[(page - 1) * limit: (page - 1) * limit + limit],
    }