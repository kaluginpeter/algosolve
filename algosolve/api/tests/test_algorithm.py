from django.urls import reverse
from rest_framework import test, status

from algorithm import models as algorithm_models
from api import serializers as api_serializers


class AlgorithmTest(test.APITestCase):

    def setUp(self):
        self.category_algorithm = algorithm_models.Category.objects.create(
            title='Test title for category algorithm',
            description='Testing description for category algorithm'
        )
        self.algorithm1 = algorithm_models.Algorithm.objects.create(
            category=self.category_algorithm,
            title='Test algorithm title1',
            description='Test description of algorithm1',
            theory='Test theory of algorithm1',
            realization='Test realization of algorithm1',
            example='Test example of algorithm1'
        )
        self.algorithm2 = algorithm_models.Algorithm.objects.create(
            category=self.category_algorithm,
            title='Test title for algorithm2',
            description='Test description for algorithm2',
            theory='Test theory for algorithm2',
            realization='Test realization for algorithm2',
            example='Test example of algorithm2'
        )
        self.algorithm3 = algorithm_models.Algorithm.objects.create(
            category=self.category_algorithm,
            title='Test title for algorithm3',
            description='Test description for algorithm3',
            theory='Test theory for algorithm3',
            realization='Test realization for algorithm3',
            example='Test example for algorithm 3'
        )
        self.fields_in_algorithm = list(
            api_serializers.FullAlgorithmSerializer.Meta.fields
        )

    def test_algorithm_list(self):
        response = self.client.get(reverse('algorithms-list'))
        # Testing successfully http request
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Testing that database have new successfully creation algorithms
        algorithms_in_database: int = algorithm_models \
            .Algorithm.objects.count()
        self.assertEqual(algorithms_in_database, 3)
        # Testing that response data have all algorithms
        self.assertEqual(
            response.json().get('count', None), algorithms_in_database
        )

    def test_algorithm_detail(self):
        response = self.client.get(
            reverse('algorithms-detail', kwargs={'slug': self.algorithm1.slug})
        )
        # Testing successfully http request
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Testing that response data have all required fields
        self.assertEqual(
            list(response.json().keys()), self.fields_in_algorithm
        )
