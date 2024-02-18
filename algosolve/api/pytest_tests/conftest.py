from django.urls import reverse
from django.test import Client
from rest_framework import test
import pytest

from algorithm import models as algorithm_models
from structure import models as structure_models
from api import serializers as api_serializers


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def create_algorithm_category(data=None):
    return algorithm_models.Category.objects.create(
        title='Test title' + data if data else 'Test title',
        description='Test descsription'
    )


@pytest.fixture
def create_data_structure_category(data=None):
    return structure_models.CategoryDateStructure.objects.create(
        title='Test title' + data if data else 'Test title',
        description='Test description'
    )


@pytest.fixture
def create_five_algorithm_categories():
    algorithm_models.Category.objects.bulk_create(
        [
            algorithm_models.Category(
                title='title' + str(i),
                description='Test description',
                slug='title' + str(i)
            ) for i in range(5)
        ]
    )
    return 5


@pytest.fixture
def create_five_data_structure_categories():
    structure_models.CategoryDateStructure.objects.bulk_create(
        [
            structure_models.CategoryDateStructure(
                title='title' + str(i),
                description='test description',
                slug='title' + str(i)
            ) for i in range(5)
        ]
    )
    return 5


@pytest.fixture
def fields_in_detail_algorithm_category():
    return list(api_serializers.FullCategoryAlgorithmSerializer.Meta.fields)


@pytest.fixture
def fields_in_detail_data_structure_category():
    return list(
        api_serializers.FullCategoryDataStructureSerializer.Meta.fields
    )


@pytest.fixture
def fields_in_detail_algorithm():
    return list(api_serializers.FullAlgorithmSerializer.Meta.fields)


@pytest.fixture
def fields_in_detail_data_structure():
    return list(api_serializers.FullDataStructureSerializer.Meta.fields)


@pytest.fixture
def fields_in_user_detail_for_author():
    return list(api_serializers.FullUserSerializer.Meta.fields)


@pytest.fixture
def create_algorithm(create_algorithm_category):
    return algorithm_models.Algorithm.objects.create(
        category=create_algorithm_category,
        title='Title for algorithm in category 1',
        description='Test description of algorithm in category 1',
        theory='Test theory for algorithm in category 1',
        realization='Test realization for algorithm in category 1',
        example='Test example for algorithm in category 1'
    )


@pytest.fixture
def create_five_algorithms(create_algorithm_category):
    algorithm_models.Algorithm.objects.bulk_create(
        algorithm_models.Algorithm(
            category=create_algorithm_category,
            title='Title for algorithm in category' + str(i),
            description='Test description of algorithm in category' + str(i),
            theory='Test theory for algorithm in category' + str(i),
            realization='Test realization for algorithm in category' + str(i),
            example='Test example for algorithm in category' + str(i),
            slug='title_for_algorithm_in_category' + str(i)
        ) for i in range(5)
    )
    return 5


@pytest.fixture
def create_data_structure(create_data_structure_category):
    return structure_models.DataStructure.objects.create(
        category=create_data_structure_category,
        title='Title for data_structure in category 1',
        description='Test description of data_structure in category 1',
        theory='Test theory for data_structure in category 1',
        realization='Test realization for data_structure in category 1',
        example='Test example for data_structure in category 1'
    )


@pytest.fixture
def create_five_data_structures(create_data_structure_category):
    structure_models.DataStructure.objects.bulk_create(
        [
            structure_models.DataStructure(
                category=create_data_structure_category,
                title='Title for data_structure in category'
                + str(i),
                description='Test description of data_structure in category'
                + str(i),
                theory='Test theory for data_structure in category'
                + str(i),
                realization='Test realization for data_structure in category'
                + str(i),
                example='Test example for data_structure in category'
                + str(i),
                slug='title_for_data_structure_in_category'
                + str(i)
            ) for i in range(5)
        ]
    )
    return 5


@pytest.fixture
def create_five_profiles():
    algorithm_models.User.objects.bulk_create(
        [
            algorithm_models.User(
                username='username' + str(i),
                password='1q2w3e4r' + str(i),
                email=f'test{str(i)}@email.com'
            ) for i in range(5)
        ]
    )
    return 5


@pytest.fixture
def author_authenticated(creation_profile):
    return algorithm_models.User.objects.get(
        username=creation_profile.get('username')
    )


@pytest.fixture
def create_five_comments_on_algorithm(
    create_algorithm, author_authenticated
):
    algorithm_models.Comment.objects.bulk_create(
        [
            algorithm_models.Comment(
                author=author_authenticated,
                algorithm=create_algorithm,
                text=f'Test{str(i)} text for multi create comment in algorithm'
            ) for i in range(5)
        ]
    )
    return 5


@pytest.fixture
def create_five_comments_on_data_structure(
    create_data_structure, author_authenticated
):
    structure_models.CommentDataStructure.objects.bulk_create(
        [
            structure_models.CommentDataStructure(
                author=author_authenticated,
                data_structure=create_data_structure,
                text=f'Test{str(i)} text for multi create \
                    comment in data structure'
            ) for i in range(5)
        ]
    )
    return 5


@pytest.fixture
def data_for_creation_profile():
    return {
        'username': 'testusername',
        'password': 'q1w2we3r4',
        'email': 'test@email.com'
    }


@pytest.fixture
def data_for_creation_profile_not_author(data_for_creation_profile):
    not_author = data_for_creation_profile.copy()
    not_author['username'] = 'notauthorusername'
    return not_author


@pytest.fixture
def data_for_creation_comment_for_algorithm(
    create_algorithm, author_authenticated
):
    return {
        'author': author_authenticated,
        'algorithm': create_algorithm,
        'text': 'Test text for comment in algorithm'
    }


@pytest.fixture
def data_for_creation_comment_for_data_structure(
    create_data_structure, author_authenticated
):
    return {
        'author': author_authenticated,
        'data_structure': create_data_structure,
        'text': 'Test text for comment in data structure'
    }


@pytest.fixture
def creation_profile(client, data_for_creation_profile):
    response = client.post(
        reverse('profile-list'),
        data={**data_for_creation_profile}
    )
    return response.json()


@pytest.fixture
def creation_comment_for_algorithm(data_for_creation_comment_for_algorithm):
    return algorithm_models.Comment.objects.create(
        **data_for_creation_comment_for_algorithm
    )


@pytest.fixture
def creation_comment_for_data_structure(
    data_for_creation_comment_for_data_structure
):
    return structure_models.CommentDataStructure.objects.create(
        **data_for_creation_comment_for_data_structure
    )


@pytest.fixture
def creation_profile_not_author(client, data_for_creation_profile_not_author):
    response = client.post(
        reverse('profile-list'),
        data={**data_for_creation_profile_not_author}
    )
    return response


@pytest.fixture
def api_client(client):
    client = test.APIClient()
    return client


@pytest.fixture
def authenticated_api_client(
    api_client, data_for_creation_profile,
    creation_profile
):
    response = api_client.post(
        '/auth/jwt/create/',
        data={
                'username': data_for_creation_profile.get('username'),
                'password': data_for_creation_profile.get('password')
            }
    )
    api_client.credentials(
        HTTP_AUTHORIZATION='Bearer ' + response.json().get('access')
    )
    return api_client


@pytest.fixture
def authenticated_api_client_not_author(
    api_client, data_for_creation_profile_not_author,
    creation_profile_not_author
):
    response = api_client.post(
        '/auth/jwt/create/',
        data={
            'username': data_for_creation_profile_not_author.get('username'),
            'password': data_for_creation_profile_not_author.get('password')
        }
    )
    api_client.credentials(
        HTTP_AUTHORIZATION='Bearer ' + response.json().get('access')
    )
    return api_client
