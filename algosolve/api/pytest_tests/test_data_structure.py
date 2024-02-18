from django.urls import reverse
from rest_framework import status


class TestDataStructure:
    def test_data_structure_list(
        self, client, create_five_data_structures
    ):
        response = client.get(reverse('data_structures-list'))
        # Check that http response will successfull
        assert response.status_code == status.HTTP_200_OK
        # Check that response data contains all algorithms in database
        assert response.json().get('count') == create_five_data_structures

    def test_data_structure_detail(
        self, client, create_data_structure,
        fields_in_detail_data_structure
    ):
        response = client.get(
            reverse(
                'data_structures-detail',
                kwargs={'slug': create_data_structure.slug}
            )
        )
        # Check that response successfull
        assert response.status_code == status.HTTP_200_OK
        # Check that response body have all required fields
        assert list(response.json().keys()) == fields_in_detail_data_structure
