from http import HTTPStatus

import pytest


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'film_id': '2021d8e7-416c-4dc8-99b3-fba694ab6aaa', 'timecode': '214112312312324',
                 'access_token': 'Bearer real_token'},
                {'status_code': HTTPStatus.OK}
        ),
        (
                {'film_id': '2021d8e7-416c-99b3-fba694ab6aaa', 'timecode': '214124',
                 'access_token': 'Bearer real_token'},
                {'status_code': HTTPStatus.UNPROCESSABLE_ENTITY}
        ),
    ],
)
@pytest.mark.asyncio
async def test_send_timecode(
        make_http_request,
        expected_answer,
        query_data,
):
    request_data = {
        'film_id': query_data['film_id'],
        'timecode': query_data['timecode'],
    }
    new_user_register = await make_http_request(
        method='POST',
        service_path='/film_timecode',
        data=request_data,
        headers={'Authorization': query_data['access_token']}
    )
    assert new_user_register['status'] == expected_answer['status_code']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'movie_id': '2021d8e7-416c-4dc8-99b3-fba694ab6aaa',
                 'mark': -1, 'updated_mark': 1, 'access_token': 'Bearer real_token'},
                {'post_status_code': HTTPStatus.OK, 'movie_id': '2021d8e7-416c-4dc8-99b3-fba694ab6aaa',
                 'mark': -1, 'updated_mark': 1}
        ),
        (
                {'movie_id': '2021d8e7-416c--99b3-fba694ab6aaa',
                 'mark': -1, 'updated_mark': 1, 'access_token': 'Bearer real_token'},
                {'post_status_code': HTTPStatus.UNPROCESSABLE_ENTITY}
        ),
        (
                {'movie_id': '2021d8e7-416c-4dc8-99b3-fba694ab6aaa',
                 'mark': 1, 'updated_mark': -1, 'access_token': 'Bearer real_token'},
                {'post_status_code': HTTPStatus.OK, 'movie_id': '2021d8e7-416c-4dc8-99b3-fba694ab6aaa',
                 'user_id': '5421770f-dd22-467c-8a01-861237fdd159', 'mark': 1, 'updated_mark': -1}
        ),
    ],
)
@pytest.mark.asyncio
async def test_crud_mark(
        make_http_request,
        expected_answer,
        query_data,
):
    request_data = {
        'movie_id': query_data['movie_id'],
        'mark': query_data['mark']
    }
    post_user_mark = await make_http_request(
        method='POST',
        service_path='/mark',
        data=request_data,
        headers={'Authorization': query_data['access_token']}
    )
    assert post_user_mark['status'] == expected_answer['post_status_code']
    if expected_answer['post_status_code'] == HTTPStatus.CREATED:
        post_mark_data = post_user_mark['body']
        get_user_mark = await make_http_request(
            method='GET',
            service_path='/mark',
            path=post_mark_data['_id'],
            headers={'Authorization': query_data['access_token']}
        )

        response_data = get_user_mark['body']
        assert response_data['movie_id'] == expected_answer['movie_id']
        assert response_data['mark'] == expected_answer['mark']
        assert response_data['user_id'] == expected_answer['user_id']
        assert '_id' in response_data
        patch_data = {
            'movie_id': query_data['movie_id'],
            'mark': query_data['updated_mark']
        }

        patch_user_mark = await make_http_request(
            method='PUT',
            service_path='/mark',
            path=post_mark_data['_id'],
            data=patch_data,
            headers={'Authorization': query_data['access_token']}
        )
        assert patch_user_mark['status'] == HTTPStatus.OK

        get_user_mark_after_update = await make_http_request(
            method='GET',
            service_path='/mark',
            path=post_mark_data['_id'],
            headers={'Authorization': query_data['access_token']}
        )

        response_data = get_user_mark_after_update['body']
        assert response_data['movie_id'] == expected_answer['movie_id']
        assert response_data['mark'] == expected_answer['updated_mark']
        assert response_data['user_id'] == expected_answer['user_id']

        delete_user_mark = await make_http_request(
            method='DELETE',
            service_path='/mark',
            path=post_mark_data['_id'],
            headers={'Authorization': query_data['access_token']}
        )
        assert delete_user_mark['status'] == HTTPStatus.NO_CONTENT

        get_user_mark_after_delete = await make_http_request(
            method='GET',
            service_path='/mark',
            path=post_mark_data['_id'],
            headers={'Authorization': query_data['access_token']}
        )
        assert get_user_mark_after_delete['status'] == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'movie_id': '2021d8e7-416c-4dc8-99b3-fba694ab6aaa', 'review': 'first_review',
                 'updated_review': 'new_review', 'access_token': 'Bearer real_token'},
                {'post_status_code': HTTPStatus.CREATED, 'movie_id': '2021d8e7-416c-4dc8-99b3-fba694ab6aaa',
                 'user_id': '5421770f-dd22-467c-8a01-861237fdd159',  'review': 'first_review',
                 'updated_review': 'new_review'}
        ),
        (
                {'movie_id': '2021d8e7-416c-4dba694ab6aaa', 'review': 'first_review',
                 'access_token': 'Bearer real_token'},
                {'post_status_code': HTTPStatus.UNPROCESSABLE_ENTITY}
        ),
        (
                {'movie_id': '2021d8e7-416c-4dc8-99b3-fba694ab6aaa',
                 'review': '', 'access_token': 'Bearer real_token'},
                {'post_status_code': HTTPStatus.UNPROCESSABLE_ENTITY}
        ),
    ],
)
@pytest.mark.asyncio
async def test_crud_review(
        make_http_request,
        expected_answer,
        query_data,
):
    request_data = {
        'movie_id': query_data['movie_id'],
        'review': query_data['review']
    }
    post_user_review = await make_http_request(
        method='POST',
        service_path='/review',
        data=request_data,
        headers={'Authorization': query_data['access_token']}
    )
    assert post_user_review['status'] == expected_answer['post_status_code']
    if expected_answer['post_status_code'] == HTTPStatus.CREATED:
        post_review_data = post_user_review['body']
        get_user_mark = await make_http_request(
            method='GET',
            service_path='/review',
            path=post_review_data['_id'],
            headers={'Authorization': query_data['access_token']}
        )
        response_data = get_user_mark['body']
        assert response_data['movie_id'] == expected_answer['movie_id']
        assert response_data['review'] == expected_answer['review']
        assert response_data['user_id'] == expected_answer['user_id']
        assert '_id' in response_data
        patch_data = {
            'movie_id': query_data['movie_id'],
            'review': query_data['updated_review']
        }
        patch_user_review = await make_http_request(
            method='PUT',
            service_path='/review',
            path=post_review_data['_id'],
            data=patch_data,
            headers={'Authorization': query_data['access_token']}
        )
        assert patch_user_review['status'] == HTTPStatus.OK

        get_user_review_after_update = await make_http_request(
            method='GET',
            service_path='/review',
            path=post_review_data['_id'],
            headers={'Authorization': query_data['access_token']}
        )

        response_data = get_user_review_after_update['body']
        assert response_data['movie_id'] == expected_answer['movie_id']
        assert response_data['review'] == expected_answer['updated_review']
        assert response_data['user_id'] == expected_answer['user_id']

        delete_user_review = await make_http_request(
            method='DELETE',
            service_path='/review',
            path=post_review_data['_id'],
            headers={'Authorization': query_data['access_token']}
        )
        assert delete_user_review['status'] == HTTPStatus.NO_CONTENT

        get_user_review_after_delete = await make_http_request(
            method='GET',
            service_path='/review',
            path=post_review_data['_id'],
            headers={'Authorization': query_data['access_token']}
        )
        assert get_user_review_after_delete['status'] == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'movie_id': '2021d8e7-416c-4dc8-99b3-fba694ab6aaa', 'access_token': 'Bearer real_token',
                 'other_movie_id': '129a3b29-3913-415b-8936-37732e02a2da'},
                {'post_status_code': HTTPStatus.OK, 'movie_id': '2021d8e7-416c-4dc8-99b3-fba694ab6aaa',
                 'user_id': '5421770f-dd22-467c-8a01-861237fdd159',
                 'other_movie_id': '129a3b29-3913-415b-8936-37732e02a2da'}
        ),
        (
                {'movie_id': '2021d8e7-416c-4dba694ab6aaa',
                 'review': 'first_review', 'access_token': 'Bearer real_token'},
                {'post_status_code': HTTPStatus.UNPROCESSABLE_ENTITY}
        ),
    ],
)
@pytest.mark.asyncio
async def test_crud_bookmark(
        make_http_request,
        expected_answer,
        query_data,
):
    request_data = {
        'movie_id': query_data['movie_id'],
    }
    post_user_bookmark = await make_http_request(
        method='POST',
        service_path='/bookmark',
        data=request_data,
        headers={'Authorization': query_data['access_token']}
    )
    assert post_user_bookmark['status'] == expected_answer['post_status_code']
    if expected_answer['post_status_code'] == HTTPStatus.CREATED:
        get_all_user_bookmarks = await make_http_request(
            method='GET',
            service_path='/bookmark',
            headers={'Authorization': query_data['access_token']}
        )
        response_data = get_all_user_bookmarks['body']
        assert type(response_data) is list
        assert response_data[-1]['movie_id'] == expected_answer['movie_id']
        assert '_id' in response_data[-1]
        post_bookmark_data = post_user_bookmark['body']
        get_user_bookmark = await make_http_request(
            method='GET',
            service_path='/bookmark',
            path=post_bookmark_data['_id'],
            headers={'Authorization': query_data['access_token']}
        )
        get_response_data = get_user_bookmark['body']
        assert get_response_data['movie_id'] == expected_answer['movie_id']
        assert get_response_data['user_id'] == expected_answer['user_id']
        assert '_id' in get_response_data
        patch_bookmark_data = {
            'movie_id': query_data['other_movie_id'],
        }
        patch_user_bookmark = await make_http_request(
            method='PUT',
            service_path='/bookmark',
            path=post_bookmark_data['_id'],
            data=patch_bookmark_data,
            headers={'Authorization': query_data['access_token']}
        )
        assert patch_user_bookmark['status'] == HTTPStatus.OK

        get_user_bookmark_after_update = await make_http_request(
            method='GET',
            service_path='/bookmark',
            path=post_bookmark_data['_id'],
            headers={'Authorization': query_data['access_token']}
        )

        response_data = get_user_bookmark_after_update['body']
        assert response_data['movie_id'] == expected_answer['other_movie_id']
        assert response_data['user_id'] == expected_answer['user_id']

        delete_user_bookmark = await make_http_request(
            method='DELETE',
            service_path='/bookmark',
            path=post_bookmark_data['_id'],
            headers={'Authorization': query_data['access_token']}
        )
        assert delete_user_bookmark['status'] == HTTPStatus.NO_CONTENT

        get_user_bookmark_after_delete = await make_http_request(
            method='GET',
            service_path='/bookmark',
            path=post_bookmark_data['_id'],
            headers={'Authorization': query_data['access_token']}
        )
        assert get_user_bookmark_after_delete['status'] == HTTPStatus.NOT_FOUND
