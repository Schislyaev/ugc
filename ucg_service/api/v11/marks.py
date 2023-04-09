from api.auth.auth_bearer import JWTBearer
from api.grpc_src.service.helpers import jwt_check
from api.schemas.helpers import InternalModel
from api.schemas.mark import MarkModel, UpdateMarkModel
from api.services.endpoint_service import EndpointService
from fastapi import APIRouter, Body, Depends, Header, Query, Request, status
from starlette.responses import JSONResponse

router = APIRouter()

service = EndpointService(
    db='user_feedback',
    table='marks'
)


@router.get(
    path='/mark/{id}',
    response_description="Get a like or dislike for a movie",
    response_model=MarkModel,
    dependencies=[Depends(JWTBearer())]
)
async def get_like(
    request: Request,
    authorization: str = Header(default=None),
    id: str = Query(...),
) -> MarkModel:

    _ = await jwt_check(token=authorization, request_path=request.url)
    mark = await service.get(id=id)

    return MarkModel(
        _id=mark['_id'],
        movie_id=mark['movie_id'],
        mark=mark['mark']
    )


@router.put(
    path='/mark/{id}',
    response_description="Update a like or dislike for a movie",
    response_model=MarkModel,
    dependencies=[Depends(JWTBearer())]
)
async def update_like(
    request: Request,
    authorization: str = Header(default=None),
    mark: UpdateMarkModel = Body(...),
    id: str = Query(...)
) -> MarkModel:

    _ = await jwt_check(token=authorization, request_path=request.url)

    updated_mark = await service.update(
        id=id,
        model=InternalModel(**mark.dict())
    )

    return MarkModel(
        _id=updated_mark['_id'],
        movie_id=updated_mark['movie_id'],
        mark=updated_mark['mark'],
    )


@router.delete(
    path='/mark/{id}',
    response_description="Delete a like or dislike for a movie",
    dependencies=[Depends(JWTBearer())]
)
async def delete_like(
        request: Request,
        authorization: str = Header(default=None),
        id: str = Query(...)
) -> JSONResponse:

    _ = await jwt_check(token=authorization, request_path=request.url)

    result = await service.delete(id=id)
    if result:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content='Ok')


@router.post(
    path='/mark',
    response_description="Add a like or dislike for a movie",
    response_model=MarkModel,
    dependencies=[Depends(JWTBearer())]
)
async def post_like(
    request: Request,
    authorization: str = Header(default=None),
    mark: MarkModel = Body(...)
) -> MarkModel:

    user_id = await jwt_check(token=authorization, request_path=request.url)

    created_mark = await service.post(
        user_id=user_id,
        model=InternalModel(
            mark=mark.mark,
            movie_id=mark.movie_id
        )
    )

    return MarkModel(
        _id=created_mark['_id'],
        movie_id=created_mark['movie_id'],
        mark=created_mark['mark'],
    )
