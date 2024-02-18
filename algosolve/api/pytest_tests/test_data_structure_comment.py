from django.urls import reverse
from rest_framework import status


class TestCommentInDataStructure:
    def test_comment_creation(
        self, authenticated_api_client,
        data_for_creation_comment_for_data_structure,
        create_data_structure
    ):
        response = authenticated_api_client.post(
            reverse(
                'data_structures_comments-list',
                kwargs={'data_structure_slug': create_data_structure.slug}
            ), data=data_for_creation_comment_for_data_structure
        )
        # Check that response will successfull
        assert response.status_code == status.HTTP_201_CREATED

    def test_comment_list(
        self, client, create_five_comments_on_data_structure,
        create_data_structure
    ):
        response = client.get(
            reverse(
                'data_structures_comments-list',
                kwargs={'data_structure_slug': create_data_structure.slug}
            )
        )
        # Check that response successfull
        assert response.status_code == status.HTTP_200_OK
        # Check that response body have all comments
        assert response.json().get('count') == \
            create_five_comments_on_data_structure

    def test_comment_detail(
        self, authenticated_api_client, create_data_structure,
        creation_comment_for_data_structure
    ):
        response = authenticated_api_client.get(
            reverse(
                'data_structures_comments-detail',
                kwargs={
                    'data_structure_slug': create_data_structure.slug,
                    'id': creation_comment_for_data_structure.id
                }
            )
        )
        # Check that http response successfull
        assert response.status_code == status.HTTP_200_OK

    def test_author_can_edit_comment_patch(
        self, authenticated_api_client,
        create_data_structure, creation_comment_for_data_structure,
        data_for_creation_comment_for_data_structure
    ):
        new_data = data_for_creation_comment_for_data_structure.copy()
        new_data['text'] = 'new text on comment'
        response = authenticated_api_client.patch(
            reverse(
                'data_structures_comments-detail',
                kwargs={
                    'data_structure_slug': create_data_structure.slug,
                    'id': creation_comment_for_data_structure.id
                }
            ), data=new_data
        )
        # Check that response successfull
        assert response.status_code == status.HTTP_200_OK
        # Check that comment has been changed
        assert response.json().get('text') == new_data.get('text')

    def test_author_can_edit_comment_put(
        self, authenticated_api_client,
        create_data_structure, creation_comment_for_data_structure,
        data_for_creation_comment_for_data_structure
    ):
        new_data = data_for_creation_comment_for_data_structure.copy()
        new_data['text'] = 'new text on comment'
        response = authenticated_api_client.put(
            reverse(
                'data_structures_comments-detail',
                kwargs={
                    'data_structure_slug': create_data_structure.slug,
                    'id': creation_comment_for_data_structure.id
                }
            ), data=new_data
        )
        # Check that response successfull
        assert response.status_code == status.HTTP_200_OK
        # Check that comment has been changed
        assert response.json().get('text') == new_data.get('text')

    def test_author_can_delete_comment(
        self, authenticated_api_client,
        create_data_structure, creation_comment_for_data_structure
    ):
        response = authenticated_api_client.delete(
            reverse(
                'data_structures_comments-detail',
                kwargs={
                    'data_structure_slug': create_data_structure.slug,
                    'id': creation_comment_for_data_structure.id
                }
            )
        )
        # Check that response successfull
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_another_user_cant_change_comment(
        self, authenticated_api_client_not_author,
        create_data_structure, creation_comment_for_data_structure,
        data_for_creation_comment_for_data_structure
    ):
        new_data = data_for_creation_comment_for_data_structure.copy()
        new_data['text'] = 'text for trying change comment by not author'
        response = authenticated_api_client_not_author.patch(
            reverse(
                'data_structures_comments-detail',
                kwargs={
                    'data_structure_slug': create_data_structure.slug,
                    'id': creation_comment_for_data_structure.id
                }
            ), data=new_data
        )
        # Check that resposne code recieved as excepcted
        assert response.status_code == status.HTTP_403_FORBIDDEN
