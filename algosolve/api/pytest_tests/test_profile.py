from django.urls import reverse
from rest_framework import status

from algorithm import models as algorithm_models


class TestProfile:
    def test_profile_creation(
        self, client, data_for_creation_profile,
        fields_in_user_detail_for_author
    ):
        url = reverse('profile-list')
        response = client.post(
            url,
            data=data_for_creation_profile,
            format='json'
        )
        # Check that request will successfull
        assert response.status_code == status.HTTP_201_CREATED
        # Check that user will create in database
        assert algorithm_models.User.objects.count() == 1
        # Check that response data contains all required fields
        assert list(response.json().keys()) == fields_in_user_detail_for_author

    def test_profile_list(
        self, client, create_five_profiles
    ):
        response = client.get(reverse('profile-list'))
        # Check that response will successfull
        assert response.status_code == status.HTTP_200_OK
        # Check that response body have all profiles
        assert response.json().get('count') == create_five_profiles

    def test_profile_detail(
        self, authenticated_api_client, creation_profile,
        fields_in_user_detail_for_author
    ):
        response = authenticated_api_client.get(
            reverse(
                'profile-detail',
                kwargs={'username': creation_profile.get('username')}
            )
        )
        # Check that response will successfull
        assert response.status_code == status.HTTP_200_OK
        # Check that that response contains all required fields
        assert list(response.json().keys()) == fields_in_user_detail_for_author

    def test_that_author_can_edit_your_profile_patch(
        self, authenticated_api_client, creation_profile,
        data_for_creation_profile
    ):
        new_data = data_for_creation_profile.copy()
        new_data['username'] = 'newusername'
        new_data.pop('password')
        new_data.pop('email')
        response = authenticated_api_client.patch(
            reverse(
                'profile-detail',
                kwargs={'username': data_for_creation_profile.get('username')}
            ),
            data=new_data, format='json'
        )
        # Check that response successfull recieved
        assert response.status_code == status.HTTP_200_OK
        # Check that data has been changed
        val_data = response.json()
        assert val_data.get('username') == new_data.get('username')
        assert val_data.get('password') == creation_profile.get('password')
        assert val_data.get('email') == data_for_creation_profile.get('email')

    def test_that_author_can_edit_your_profile_put(
        self, authenticated_api_client, creation_profile,
        data_for_creation_profile
    ):
        new_data = data_for_creation_profile.copy()
        new_data['username'] = 'newusername'
        new_data['password'] = 'newpassWord777'
        new_data.pop('email')
        response = authenticated_api_client.put(
            reverse(
                'profile-detail',
                kwargs={'username': data_for_creation_profile.get('username')}
            ),
            data=new_data, format='json'
        )
        # Check that response successfull recieved
        assert response.status_code == status.HTTP_200_OK
        # Check that data has been changed
        val_data = response.json()
        assert val_data.get('username') == new_data.get('username')
        assert val_data.get('password') != creation_profile.get('password')
        assert val_data.get('email') == data_for_creation_profile.get('email')

    def test_another_user_cant_change_profile(
        self, authenticated_api_client_not_author,
        creation_profile, data_for_creation_profile
    ):
        new_data = data_for_creation_profile.copy()
        new_data['username'] = 'newusername'
        new_data['password'] = 'newpassWord777'
        new_data.pop('email')
        response = authenticated_api_client_not_author.put(
            reverse(
                'profile-detail',
                kwargs={'username': data_for_creation_profile.get('username')}
            ),
            data=new_data, format='json'
        )
        # Check that response successfull recieved
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_author_can_delete_profile(
        self, authenticated_api_client, creation_profile
    ):
        response = authenticated_api_client.delete(
            reverse(
                'profile-detail',
                kwargs={'username': creation_profile.get('username')}
            )
        )
        # Check that response code successfull
        assert response.status_code == status.HTTP_204_NO_CONTENT
