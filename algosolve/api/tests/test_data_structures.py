from django.urls import reverse
from rest_framework import test, status

from structure import models as structure_models
from api import serializers as api_serializers


class DataStructureTest(test.APITestCase):

    def setUp(self):
        self.category_data_structure = structure_models.CategoryDateStructure \
            .objects.create(
                title='Test title for category data structure',
                description='Test description for category data structure'
            )
        self.data_structure1 = structure_models.DataStructure.objects.create(
            category=self.category_data_structure,
            title='Test title for data structure1',
            description='Test description for data structure1',
            theory='Test theory for data structure1',
            realization='Test realization for data structure1',
            example='Test example for data structure1'
        )
        self.data_structure2 = structure_models.DataStructure.objects.create(
            category=self.category_data_structure,
            title='Test title for data structure2',
            description='Test description for data structure2',
            theory='Test theory for data structure2',
            realization='Test realization for data structrue2',
            example='Test example for data structure2'
        )
        self.data_structure3 = structure_models.DataStructure.objects.create(
            category=self.category_data_structure,
            title='Test title for data structure3',
            description='Test description for data structure3',
            theory='Test theory for data structure3',
            realization='Test realization for data structure3',
            example='Test example for data structure3'
        )
        self.data_structures_in_database: int = 3
        self.fields_in_data_structure_detail = list(
            api_serializers.FullDataStructureSerializer.Meta.fields
        )

    def test_data_structure_list(self):
        response = self.client.get(reverse('data_structures-list'))
        # Check that http response will successfully revieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that will already have data structures in database
        data_structures_in_database: int = structure_models.DataStructure.objects.count()
        self.assertEqual(
            data_structures_in_database,
            self.data_structures_in_database
        )
        # Check that in response data we have all data structures
        self.assertEqual(
            response.json().get('count'),
            data_structures_in_database
        )

    def test_data_structure_detail(self):
        response = self.client.get(
            reverse(
                'data_structures-detail',
                kwargs={'slug': self.data_structure1.slug}
            )
        )
        # Check that http request will successfull
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that response data have all required fields
        self.assertEqual(
            list(response.json().keys()),
            self.fields_in_data_structure_detail
        )
