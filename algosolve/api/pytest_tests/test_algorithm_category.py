from django.urls import reverse
from rest_framework import status


class TestCategoryInAlgorithm:
    def test_category_list(self, client, create_five_algorithm_categories):
        response = client.get(reverse('algorithm_categories-list'))
        # Test that response will successfull
        assert response.status_code == status.HTTP_200_OK
        # Check that response data have all categories
        assert response.json().get('count') == create_five_algorithm_categories

    def test_category_detail(
            self, client, create_algorithm_category,
            fields_in_detail_algorithm_category
    ):
        response = client.get(reverse(
            'algorithm_categories-detail',
            kwargs={'slug': create_algorithm_category.slug}
            )
        )
        correct_data = response.json()
        # Check that response will successfull
        assert response.status_code == status.HTTP_200_OK
        # Check that response data have all required fields
        assert list(correct_data.keys()) == \
            fields_in_detail_algorithm_category

    def test_algorithms_in_category_detail(
        self, client, create_algorithm_category,
        create_algorithm
    ):
        response = client.get(reverse(
            'algorithm_categories-detail',
            kwargs={'slug': create_algorithm_category.slug}
            )
        )
        # Check that response will successfull
        assert response.status_code == status.HTTP_200_OK
        # Check that category have algorithms in response data
        assert len(response.json().get('algorithms')) > 0
