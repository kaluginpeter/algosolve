from random import randint

from django.urls import reverse
from rest_framework import test, status

from algorithm import models as algorithm_models
from api import serializers as api_serializers
from . import test_profile


class CommentInAlgorithmTest(test.APITestCase):

    def setUp(self):
        self.data_for_user_creation = {
            'username': 'TestUsername',
            'password': 'Q1W2E3R4T5',
            'email': 'testemail@test.com'
        }
        self.category = algorithm_models.Category.objects.create(
            title='Test title for category algorithm',
            description='Test description for category algorithm'
        )
        self.algorithm = algorithm_models.Algorithm.objects.create(
            category=self.category,
            title='Test title for algorithm',
            description='Test description for algorithm',
            theory='Test theory for algorithm',
            realization='Test realization for algorithm',
            example='Test example for algorithm'
        )
        self.data_for_creation_comment = {
            'author': None,
            'text': 'Test text for comment on algorithm',
            'algorithm': self.algorithm
        }

    def test_authentication_jwt(self, data=None):
        if data:
            data['username'] = data.get('username') + str(randint(1, 10000))
        test_profile.ProfileTest.test_user_creation(
            self, data=self.data_for_user_creation if not data else data
        )
        response = self.client.post(
            '/auth/jwt/create/',
            data={
                'username': self.data_for_user_creation.get('username')
                if not data else data.get('username'),
                'password': self.data_for_user_creation.get('password')
                if not data else data.get('password')
            }
        )
        # Check that response will successfull
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Authorize client
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + response.json().get('access')
        )
        return algorithm_models.User.objects.last()

    def test_comment_create(self, data_comment=None, data_user=None):
        initial_commets_in_database = algorithm_models.Comment.objects.count()
        # Create and authenticate user
        user = self.test_authentication_jwt(
            self.data_for_user_creation if not data_user
            else data_user
        )
        # Create comment
        data_for_creation_comment = self.data_for_creation_comment.copy() \
            if not data_comment else data_comment
        data_for_creation_comment['author'] = user
        response = self.client.post(reverse(
            'algorithm_comments-list',
            kwargs={'algorithm_slug': self.algorithm.slug}
            ),
            data=data_for_creation_comment
        )
        # Check that http request successfull
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check that comment create in database
        self.assertGreater(
            algorithm_models.Comment.objects.count(),
            initial_commets_in_database
        )
        return algorithm_models.Comment.objects.last()

    def test_comment_list(self):
        count_comments: int = 5
        for _ in range(count_comments):
            self.test_comment_create()
        # Check that all users create in database
        self.assertEqual(
            algorithm_models.Comment.objects.count(), count_comments
        )
        response = self.client.get(
            reverse(
                'algorithm_comments-list',
                kwargs={'algorithm_slug': self.algorithm.slug}
            )
        )
        # Check that response to endpoint will successfull
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that resposne data have all created comments
        self.assertEqual(response.json().get('count'), count_comments)

    def test_comment_detail(self):
        comment = self.test_comment_create()
        response = self.client.get(
            reverse(
                'algorithm_comments-detail',
                kwargs={
                    'algorithm_slug': self.algorithm.slug,
                    'id': comment.id
                }
            )
        )
        # Check that response will successfull
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_author_can_edit_comment_patch(self):
        comments_in_database_before_creation: int = algorithm_models. \
            Comment.objects.count()
        author = {
            'username': 'authorofmessage',
            'password': 'q1w2we3r',
            'email': 'author@comment.com'
        }
        initial_data_of_comment = self.data_for_creation_comment.copy()
        comment = self.test_comment_create(
            data_comment=initial_data_of_comment, data_user=author
        )
        # Check that comment create in database
        self.assertGreater(
            algorithm_models.Comment.objects.count(),
            comments_in_database_before_creation
        )
        new_data_for_comment = initial_data_of_comment.copy()
        new_data_for_comment['text'] = 'new text'
        response = self.client.patch(
            reverse(
                'algorithm_comments-detail',
                kwargs={
                    'algorithm_slug': self.algorithm.slug,
                    'id': comment.id
                }
            ),
            data=new_data_for_comment
        )
        # Check that patch resposne will successfull
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that that text will changed
        new_comment = algorithm_models.Comment.objects.get(id=comment.id)
        self.assertNotEqual(
            new_comment.text,
            initial_data_of_comment.get('text')
        )
        self.assertEqual(new_comment.text, new_data_for_comment.get('text'))

    def test_author_can_edit_comment_put(self):
        comments_in_database_before_creation: int = algorithm_models. \
            Comment.objects.count()
        author = {
            'username': 'authorofmessage',
            'password': 'q1w2we3r',
            'email': 'author@comment.com'
        }
        initial_data_of_comment = self.data_for_creation_comment.copy()
        comment = self.test_comment_create(
            data_comment=initial_data_of_comment, data_user=author
        )
        # Check that comment create in database
        self.assertGreater(
            algorithm_models.Comment.objects.count(),
            comments_in_database_before_creation
        )
        new_data_for_comment = initial_data_of_comment.copy()
        new_data_for_comment['text'] = 'new text'
        response = self.client.put(
            reverse(
                'algorithm_comments-detail',
                kwargs={
                    'algorithm_slug': self.algorithm.slug,
                    'id': comment.id
                }
            ),
            data=new_data_for_comment
        )
        # Check that patch resposne will successfull
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that that text will changed
        new_comment = algorithm_models.Comment.objects.get(id=comment.id)
        self.assertNotEqual(
            new_comment.text,
            initial_data_of_comment.get('text')
        )
        self.assertEqual(new_comment.text, new_data_for_comment.get('text'))

    def test_author_can_delete_comment(self):
        comments_in_database_before_creation: int = algorithm_models. \
            Comment.objects.count()
        author = {
            'username': 'authorofmessage',
            'password': 'q1w2we3r',
            'email': 'author@comment.com'
        }
        initial_data_of_comment = self.data_for_creation_comment.copy()
        comment = self.test_comment_create(
            data_comment=initial_data_of_comment, data_user=author
        )
        # Check that comment create in database
        comments_in_database_before_deleting: int = algorithm_models. \
            Comment.objects.count()
        self.assertGreater(
            comments_in_database_before_deleting,
            comments_in_database_before_creation
        )
        # Deleting comment
        response = self.client.delete(
            reverse(
                'algorithm_comments-detail',
                kwargs={
                    'algorithm_slug': self.algorithm.slug,
                    'id': comment.id
                }
            )
        )
        # Check that delete response will successfull
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Check that comment deleted from database
        comment_in_database_after_deleting: int = algorithm_models \
            .Comment.objects.count()
        self.assertLess(
            comment_in_database_after_deleting,
            comments_in_database_before_deleting
        )
        self.assertEqual(
            comment_in_database_after_deleting,
            comments_in_database_before_creation
        )
