from django.urls import reverse
from rest_framework import test, status

from structure import models as structure_models
from api import serializers as api_serializers


class CategoryDataStructureTest(test.APITestCase):

    def setUp(self):
        self.category1 = structure_models.CategoryDateStructure.objects.create(
            title='Test title for data structure category1',
            description='Test description for data structure category1'
        )
        self.category2 = structure_models.CategoryDateStructure.objects.create(
            title='Test title for data structure category2',
            description='Test description for data structure category2'
        )
        self.data_structure_in_category1 = structure_models.DataStructure \
            .objects.create(
                category=self.category1,
                title='Test title for data structure',
                description='Test description for data structure',
                theory='Test theory for data structure',
                realization='Test realization for data structure',
                example='Test example for data structure'
            )

    def test_category_data_structure_list(self):
        response = self.client.get(reverse('data_structure_categories-list'))
        # Check that response will recieved successfully
        data_structures_categories_in_database: int = structure_models \
            .CategoryDateStructure.objects.count()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that our setUp data already in database
        self.assertEqual(
            data_structures_categories_in_database, 2
        )
        # Test that response data have all created category
        self.assertEqual(
            response.json().get('count'),
            data_structures_categories_in_database
        )
        # Check that response data have all required fields
        self.assertEqual(
            list(response.json().get('results')[0].keys()),
            list(api_serializers.CategoryDataStructureSerializer.Meta.fields)
        )

    def test_category_data_structure_detail(self):
        response = self.client.get(
            reverse(
                'data_structure_categories-detail',
                kwargs={'slug': self.category1.slug}
            )
        )
        # Check that resposne will successully recieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that reposne contains all required fields
        self.assertEqual(
            list(response.json().keys()),
            list(
                api_serializers.FullCategoryDataStructureSerializer.Meta.fields
            )
        )

    def test_data_structures_in_category(self):
        response = self.client.get(
            reverse(
                'data_structure_categories-detail',
                kwargs={'slug': self.category1.slug}
            )
        )
        # Check that response will successfully revieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that we already have data structure in database
        data_structures_in_database: int = structure_models \
            .DataStructure.objects.count()
        self.assertEqual(
            data_structures_in_database, 1
        )
        # Check that category has data structrure in data
        self.assertEqual(
            len(response.json().get('data_structures')),
            data_structures_in_database
        )
