from api.auth.auth_bearer import JWTBearer
from api.grpc_src.service.helpers import jwt_check
from api.schemas.helpers import InternalModel
from api.schemas.review import ReviewModel, UpdateReviewModel
from api.services.endpoint_service import EndpointService
from fastapi import APIRouter, Body, Depends, Header, Query, Request, status
from starlette.responses import JSONResponse

router = APIRouter()

service = EndpointService(
    db='user_feedback',
    table='reviews'
)


@router.post(
    path='/review',
    response_description="Post a review for a movie",
    response_model=ReviewModel,
    dependencies=[Depends(JWTBearer())]
)
async def post_review(
    request: Request,
    authorization: str = Header(default=None),
    review: ReviewModel = Body(...)
) -> ReviewModel:
    user_id = await jwt_check(token=authorization, request_path=request.url)
    created_review = await service.post(
        user_id=user_id,
        model=InternalModel(**review.dict())
    )

    return ReviewModel(
        _id=created_review['_id'],
        movie_id=created_review['movie_id'],
        review=created_review['review']
    )


@router.get(
    path='/review/{id}',
    response_description="Get a review for a movie",
    response_model=ReviewModel,
    dependencies=[Depends(JWTBearer())]
)
async def get_review(
    request: Request,
    authorization: str = Header(default=None),
    id: str = Query(...)
) -> ReviewModel:

    _ = await jwt_check(token=authorization, request_path=request.url)
    review = await service.get(id=id)

    return ReviewModel(
        _id=review['_id'],
        movie_id=review['movie_id'],
        review=review['review']
    )


@router.put(
    path='/review/{id}',
    response_description="Update a review for a movie",
    response_model=ReviewModel,
    dependencies=[Depends(JWTBearer())]
)
async def update_review(
    request: Request,
    authorization: str = Header(default=None),
    review: UpdateReviewModel = Body(...),
    id: str = Query(...)
) -> ReviewModel:

    _ = await jwt_check(token=authorization, request_path=request.url)

    updated_review = await service.update(
        id=id,
        model=InternalModel(**review.dict())
    )

    return ReviewModel(
        _id=updated_review['_id'],
        movie_id=updated_review['movie_id'],
        review=updated_review['review']
    )


@router.delete(
    path='/review/{id}',
    response_description="Delete a review for a movie",
    dependencies=[Depends(JWTBearer())]
)
async def delete_review(
        request: Request,
        authorization: str = Header(default=None),
        id: str = Query(...)
) -> JSONResponse:

    _ = await jwt_check(token=authorization, request_path=request.url)

    result = await service.delete(id=id)
    if result:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content='Ok')
