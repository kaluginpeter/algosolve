from django.urls import reverse
from rest_framework import status


class TestCommentInAlgorithm:
    def test_comment_creation(
        self, authenticated_api_client,
        data_for_creation_comment_for_algorithm,
        create_algorithm
    ):
        response = authenticated_api_client.post(
            reverse(
                'algorithm_comments-list',
                kwargs={'algorithm_slug': create_algorithm.slug}
            ), data=data_for_creation_comment_for_algorithm
        )
        # Check that response will successfull
        assert response.status_code == status.HTTP_201_CREATED

    def test_comment_list(
        self, client, create_five_comments_on_algorithm, create_algorithm
    ):
        response = client.get(
            reverse(
                'algorithm_comments-list',
                kwargs={'algorithm_slug': create_algorithm.slug}
            )
        )
        # Check that response successfull
        assert response.status_code == status.HTTP_200_OK
        # Check that response body have all comments
        assert response.json().get('count') == \
            create_five_comments_on_algorithm

    def test_comment_detail(
        self, authenticated_api_client, create_algorithm,
        creation_comment_for_algorithm
    ):
        response = authenticated_api_client.get(
            reverse(
                'algorithm_comments-detail',
                kwargs={
                    'algorithm_slug': create_algorithm.slug,
                    'id': creation_comment_for_algorithm.id
                }
            )
        )
        # Check that http response successfull
        assert response.status_code == status.HTTP_200_OK

    def test_author_can_edit_comment_patch(
        self, authenticated_api_client,
        create_algorithm, creation_comment_for_algorithm,
        data_for_creation_comment_for_algorithm
    ):
        new_data = data_for_creation_comment_for_algorithm.copy()
        new_data['text'] = 'new text on comment'
        response = authenticated_api_client.patch(
            reverse(
                'algorithm_comments-detail',
                kwargs={
                    'algorithm_slug': create_algorithm.slug,
                    'id': creation_comment_for_algorithm.id
                }
            ), data=new_data
        )
        # Check that response successfull
        assert response.status_code == status.HTTP_200_OK
        # Check that comment has been changed
        assert response.json().get('text') == new_data.get('text')

    def test_author_can_edit_comment_put(
        self, authenticated_api_client,
        create_algorithm, creation_comment_for_algorithm,
        data_for_creation_comment_for_algorithm
    ):
        new_data = data_for_creation_comment_for_algorithm.copy()
        new_data['text'] = 'new text on comment'
        response = authenticated_api_client.put(
            reverse(
                'algorithm_comments-detail',
                kwargs={
                    'algorithm_slug': create_algorithm.slug,
                    'id': creation_comment_for_algorithm.id
                }
            ), data=new_data
        )
        # Check that response successfull
        assert response.status_code == status.HTTP_200_OK
        # Check that comment has been changed
        assert response.json().get('text') == new_data.get('text')

    def test_author_can_delete_comment(
        self, authenticated_api_client,
        create_algorithm, creation_comment_for_algorithm
    ):
        response = authenticated_api_client.delete(
            reverse(
                'algorithm_comments-detail',
                kwargs={
                    'algorithm_slug': create_algorithm.slug,
                    'id': creation_comment_for_algorithm.id
                }
            )
        )
        # Check that response successfull
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_another_user_cant_change_comment(
        self, authenticated_api_client_not_author,
        create_algorithm, creation_comment_for_algorithm,
        data_for_creation_comment_for_algorithm
    ):
        new_data = data_for_creation_comment_for_algorithm.copy()
        new_data['text'] = 'text for trying change comment by not author'
        response = authenticated_api_client_not_author.patch(
            reverse(
                'algorithm_comments-detail',
                kwargs={
                    'algorithm_slug': create_algorithm.slug,
                    'id': creation_comment_for_algorithm.id
                }
            ), data=new_data
        )
        # Check that resposne code recieved as excepcted
        assert response.status_code == status.HTTP_403_FORBIDDEN
