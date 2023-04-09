from api.auth.auth_bearer import JWTBearer
from api.grpc_src.service.helpers import jwt_check
from api.schemas.bookmark import (BookmarkModel, InputBookmarkModel,
                                  InternalBookmarkModel, UpdateBookmarkModel)
from api.schemas.helpers import Pagination
from api.services.endpoint_service import EndpointService
from fastapi import APIRouter, Body, Depends, Header, Query, Request, status
from starlette.responses import JSONResponse

router = APIRouter()

service = EndpointService(
    db='user_data',
    table='bookmarks'
)


@router.post(
    path='/bookmark',
    summary='Положить закладку',
    description='Сохранить закладку на фильм',
    response_description='Вывод уникального номера закладки и сохраненного фильма',
    response_model=BookmarkModel,
    response_model_exclude_defaults=True,
    dependencies=[Depends(JWTBearer())]
)
async def post_marker(
    request: Request,
    authorization: str = Header(default=None),
    bookmark: InputBookmarkModel = Body(...),
) -> BookmarkModel:
    user_id = await jwt_check(token=authorization, request_path=request.url)

    created_bookmark = await service.post(
        user_id=user_id,
        model=InternalBookmarkModel(movie_id=bookmark.movie_id)
    )

    return BookmarkModel(
        _id=created_bookmark['_id'],
        movie_id=created_bookmark['movie_id']
    )


@router.get(
    path='/bookmark/{id}',
    summary='Получить закладку',
    description='Получить закладку на фильм',
    response_description="Get a bookmark for a movie",
    response_model=InputBookmarkModel,
    dependencies=[Depends(JWTBearer())]
)
async def get_bookmark(
    request: Request,
    authorization: str = Header(default=None),
    id: str = Query(...)
) -> InputBookmarkModel:

    _ = await jwt_check(token=authorization, request_path=request.url)
    bookmark = await service.get(id=id)

    return InputBookmarkModel(
        movie_id=bookmark['movie_id']
    )


@router.put(
    path='/bookmark/{id}',
    summary='Обновить закладку',
    description='Обновить закладку на фильм',
    response_description="Update a bookmark for a movie",
    response_model=BookmarkModel,
    dependencies=[Depends(JWTBearer())]
)
async def update_bookmark(
    request: Request,
    authorization: str = Header(default=None),
    bookmark: UpdateBookmarkModel = Body(...),
    id: str = Query(...)
) -> BookmarkModel:

    _ = await jwt_check(token=authorization, request_path=request.url)

    updated_bookmark = await service.update(id=id, model=bookmark)

    return BookmarkModel(
        _id=updated_bookmark['_id'],
        movie_id=updated_bookmark['movie_id']
    )


@router.delete(
    path='/bookmark/{id}',
    summary='Удалить закладку',
    description='Удалить закладку на фильм',
    response_description="Delete a bookmark for a movie",
    dependencies=[Depends(JWTBearer())],
)
async def delete_bookmark(
        request: Request,
        authorization: str = Header(default=None),
        id: str = Query(...)
) -> JSONResponse:

    _ = await jwt_check(token=authorization, request_path=request.url)

    result = await service.delete(id=id)
    if result:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content='Ok')


@router.get(
    path='/bookmark',
    summary='Получить все закладки',
    description='Получить все закладки на фильм конкретного пользователя',
    response_description="Get all bookmarks for a user",
    response_model=list[BookmarkModel],
    dependencies=[Depends(JWTBearer())]
)
async def get_all_bookmarks(
    request: Request,
    authorization: str = Header(default=None),
    pagination: Pagination = Depends(),
) -> list[BookmarkModel]:

    user_id = await jwt_check(token=authorization, request_path=request.url)
    bookmarks = await service.get_all_by_userid(
        user_id=user_id,
        page=pagination.number,
        size=pagination.size
    )

    return [BookmarkModel(
        _id=bookmark['_id'],
        movie_id=bookmark['movie_id']
    ) for bookmark in bookmarks]
