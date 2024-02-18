from django.urls import reverse
from rest_framework import test, status

from algorithm import models as algorithm_models
from api import serializers as api_serializers


class AlgorithmCategories(test.APITestCase):

    def setUp(self) -> None:
        self.data_for_algorithm_category1 = {
            'title': 'Test category title1',
            'description': 'Test category description'
        }
        self.algorithm_category1 = algorithm_models.Category.objects.create(
            **self.data_for_algorithm_category1
        )
        self.algorithm_category2 = algorithm_models.Category.objects.create(
            title='Test category title2',
            description='Test category description'
        )
        self.algorithm_category3 = algorithm_models.Category.objects.create(
            title='Test category title3',
            description='Test category description'
        )
        self.algorithm_in_category1 = algorithm_models.Algorithm.objects \
            .create(
                category=self.algorithm_category1,
                title='Title for algorithm in category 1',
                description='Test description of algorithm in category 1',
                theory='Test theory for algorithm in category 1',
                realization='Test realization for algorithm in category 1',
                example='Test example for algorithm in category 1'
            )
        self.fields_in_category_detail = list(
            api_serializers.FullCategoryAlgorithmSerializer.Meta.fields
        )

    def test_category_list(self):
        response = self.client.get(reverse('algorithm_categories-list'))
        # Testing successfully http request
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Testing that response data have all categories
        categories_in_database: int = algorithm_models.Category.objects.count()
        self.assertEqual(
            response.json().get('count', None),
            categories_in_database
        )

    def test_category_detail(self):
        response = self.client.get(
            reverse(
                'algorithm_categories-detail',
                kwargs={'slug': self.algorithm_category1.slug}
            )
        )
        validated_json = response.json()
        # Testing successfully http request
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Testing that category has same data before creating
        self.assertEqual(
            validated_json.get('title', None),
            self.data_for_algorithm_category1.get('title')
        )
        # Testing that category has same data before creation
        self.assertEqual(
            validated_json.get('description', None),
            self.data_for_algorithm_category1.get('description')
        )
        # Testing that response query contains all fields in model
        self.assertEqual(
            list(validated_json.keys()), self.fields_in_category_detail
        )

    def test_algorithms_in_category_detail(self):
        response = self.client.get(
            reverse(
                'algorithm_categories-detail',
                kwargs={'slug': self.algorithm_category1.slug}
            )
        )
        # Testing successfully http request
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Testing that category have a one algorithm in "algorithms" field
        self.assertEqual(response.json().get('algorithms', None).__len__(), 1)
