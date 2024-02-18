from django.urls import reverse
from rest_framework import test, status

from algorithm import models as algorithm_models
from api import serializers as api_serializers


class ProfileTest(test.APITestCase):

    def setUp(self):
        self.data_for_creation_profile = {
            'username': 'TestUser',
            'password': 'Q1w2e3r4T5',
            'email': 'testemail@test.com'
        }
        self.user_in_database = 1

    def test_user_creation(self, data=None):
        url = reverse('profile-list')
        response = self.client.post(
            url,
            data=data if data else self.data_for_creation_profile,
            format='json'
        )
        # Testing successfully http request
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Testing that response data have all required fields
        self.assertEqual(
            list(response.json().keys()),
            list(api_serializers.FullUserSerializer.Meta.fields)
        )
        # Testing that user create profile in database
        if not data:
            # We use "data" when create multi users,
            # otherwise we create single user
            # and check that its successfully create in database
            self.assertEqual(
                algorithm_models.User.objects.count(), self.user_in_database
            )

    def test_profile_list(self):
        # Creation 10 users in database
        for i in range(1, 11):
            data = self.data_for_creation_profile.copy()
            data['username'] = data.get('username') + str(i)
            self.test_user_creation(data=data)
        # Check that we successfully create users
        self.assertEqual(algorithm_models.User.objects.count(), 10)
        response = self.client.get(reverse('profile-list'))
        # Testing successfully http request
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Testing that response data have 10 items
        self.assertEqual(response.json().get('count'), 10)

    def test_profile_detail(self):
        # Intially create profile in database
        data_for_profile_creation = self.data_for_creation_profile.copy()
        intial_name = data_for_profile_creation.get('username')
        self.test_user_creation(data=data_for_profile_creation)
        # Check that's all is fine and profile in database
        self.assertEqual(algorithm_models.User.objects.count(), 1)
        # Send request to create jwt access token
        jwt_response = self.client.post(
            '/auth/jwt/create/',
            data={
                'username': intial_name,
                'password': data_for_profile_creation.get('password')
            }
        )
        # Check that we successfully send request
        self.assertEqual(jwt_response.status_code, status.HTTP_200_OK)
        # Authorize client
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + jwt_response.json().get('access')
        )
        # Create http request to profile detail endpoint
        response = self.client.get(
            reverse('profile-detail', kwargs={'username': intial_name})
        )
        # Check thats http resposne successfully sended
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that resposne data have all required fields
        required_fields = list(api_serializers.FullUserSerializer.Meta.fields)
        self.assertEqual(list(response.json().keys()), required_fields)

    def test_author_can_edit_your_profile_patch(self):
        data_for_profile = self.data_for_creation_profile.copy()
        initial_name = data_for_profile.get('username')
        self.test_user_creation(data=data_for_profile)
        # Check that user create in database
        self.assertEqual(algorithm_models.User.objects.count(), 1)
        # Sending http request to create jwt token
        jwt_access = self.client.post(
            '/auth/jwt/create/',
            data={
                'username': data_for_profile.get('username'),
                'password': data_for_profile.get('password')
            }
        )
        # Testing that we successfully send response from jwt creation endpoint
        self.assertEqual(jwt_access.status_code, status.HTTP_200_OK)
        # Take from response jwt data access token
        jwt_access = jwt_access.json().get('access')
        # Authorize client
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_access)
        # Set new username in data
        new_username = 'new_username'
        data_for_profile['username'] = new_username
        # Create url to change profile
        url = reverse('profile-detail', kwargs={'username': initial_name})
        # Making request to change profile with new data
        response = self.client.patch(url, data=data_for_profile, format='json')
        # Test that we successfull send http request
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Test that username has been changed
        self.assertNotEqual(response.json().get('username'), initial_name)
        # Test that usernmae has been changed
        self.assertEqual(response.json().get('username'), new_username)

    def test_author_can_edit_profile_put(self):
        data_for_profile = self.data_for_creation_profile.copy()
        initial_name = data_for_profile.get('username')
        self.test_user_creation(data=data_for_profile)
        # Check that user create in database
        self.assertEqual(algorithm_models.User.objects.count(), 1)
        # Sending http request to create jwt token
        jwt_access = self.client.post(
            '/auth/jwt/create/',
            data={
                'username': data_for_profile.get('username'),
                'password': data_for_profile.get('password')
            }
        )
        # Testing that we successfully send response from jwt creation endpoint
        self.assertEqual(jwt_access.status_code, status.HTTP_200_OK)
        # Take from response jwt data access token
        jwt_access = jwt_access.json().get('access')
        # Authorize client
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_access)
        # Set new username in data
        new_username = 'new_username'
        data_for_profile['username'] = new_username
        # Create url to change profile
        url = reverse('profile-detail', kwargs={'username': initial_name})
        # Making request to change profile with new data
        response = self.client.put(url, data=data_for_profile, format='json')
        # Test that we successfull send http request
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Test that username has been changed
        self.assertNotEqual(response.json().get('username'), initial_name)
        # Test that usernmae has been changed
        self.assertEqual(response.json().get('username'), new_username)

    def test_another_user_cant_change_profile_another_user(self):
        data_for_profile = self.data_for_creation_profile.copy()
        initial_name = data_for_profile.get('username')
        # Create profile
        self.test_user_creation(data=data_for_profile)
        # Check that all is fine and profile create in database
        self.assertEqual(algorithm_models.User.objects.count(), 1)
        # Making data for creation another user
        initial_name_another_user = 'Another_username'
        data_for_profile_another_user = self.data_for_creation_profile.copy()
        data_for_profile_another_user['username'] = initial_name_another_user
        # Create another profile
        self.test_user_creation(data=data_for_profile_another_user)
        # Check that all is fine and second user had been added in database
        self.assertEqual(algorithm_models.User.objects.count(), 2)
        # Create url request to jwt creation for second user
        jwt_response_another_user = self.client.post(
            '/auth/jwt/create/',
            data={
                'username': data_for_profile_another_user.get('username'),
                'password': data_for_profile_another_user.get('password')
            }
        )
        # Check that request successfully sended
        self.assertEqual(
            jwt_response_another_user.status_code, status.HTTP_200_OK
        )
        # Authorize second (another) user
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' +
            jwt_response_another_user.json().get('access')
        )
        # Trying send patch request to change profile name
        # of first user on new username
        new_username_for_first_user = 'new_first_name'
        response_to_change_name_first_user = self.client.patch(
            reverse(
                'profile-detail',
                kwargs={'username': data_for_profile.get('username')}
            ),
            data={'username': new_username_for_first_user}, format='json'
        )
        print(response_to_change_name_first_user.json())
        # Check that status code of response is not 2xx
        self.assertEqual(
            response_to_change_name_first_user.status_code,
            status.HTTP_403_FORBIDDEN
        )
        # Checking that name first user has not changed
        first_user = algorithm_models.User.objects.get(
            username=data_for_profile.get('username')
        )
        self.assertEqual(first_user.username, initial_name)
        # Check that username first name not equal new username
        self.assertNotEqual(initial_name, new_username_for_first_user)
