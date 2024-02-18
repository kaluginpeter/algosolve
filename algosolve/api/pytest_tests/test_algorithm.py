from django.urls import reverse
from rest_framework import status


class TestAlgorithm:
    def test_algorithm_list(
        self, client, create_five_algorithms
    ):
        response = client.get(reverse('algorithms-list'))
        # Check that http response will successfull
        assert response.status_code == status.HTTP_200_OK
        # Check that response data contains all algorithms in database
        assert response.json().get('count') == create_five_algorithms

    def test_algorithm_detail(
        self, client, create_algorithm,
        fields_in_detail_algorithm
    ):
        response = client.get(
            reverse(
                'algorithms-detail', kwargs={'slug': create_algorithm.slug}
            )
        )
        # Check that response successfull
        assert response.status_code == status.HTTP_200_OK
        # Check that response body have all required fields
        assert list(response.json().keys()) == fields_in_detail_algorithm
