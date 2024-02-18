from django.urls import reverse
from rest_framework import status


class TestCategoryInDataStructure:
    def test_category_list(
            self, client, create_five_data_structure_categories
    ):
        response = client.get(reverse('data_structure_categories-list'))
        # Test that response will successfull
        assert response.status_code == status.HTTP_200_OK
        # Check that response data have all categories
        assert response.json().get('count') == \
            create_five_data_structure_categories

    def test_category_detail(
            self, client, create_data_structure_category,
            fields_in_detail_data_structure_category
    ):
        response = client.get(reverse(
            'data_structure_categories-detail',
            kwargs={'slug': create_data_structure_category.slug}
            )
        )
        correct_data = response.json()
        # Check that response will successfull
        assert response.status_code == status.HTTP_200_OK
        # Check that response data have all required fields
        assert list(correct_data.keys()) == \
            fields_in_detail_data_structure_category

    def test_data_structures_in_category_detail(
        self, client, create_data_structure_category,
        create_data_structure
    ):
        response = client.get(reverse(
            'data_structure_categories-detail',
            kwargs={'slug': create_data_structure_category.slug}
            )
        )
        # Check that response will successfull
        assert response.status_code == status.HTTP_200_OK
        # Check that category have algorithms in response data
        assert len(response.json().get('data_structures')) > 0
