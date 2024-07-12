import unittest
from table_search_utils import upload_file, query_uploaded_table, transform_data_to_dict


class TestConnection(unittest.TestCase):

    # test uploading existing file
    def test_upload_file(self):
        response = upload_file('datasets/IMDb_Dataset.csv')
        self.assertEqual(response.status_code, 200)

    # test querying existing dataset
    def test_query_connection(self):
        response = query_uploaded_table('IMDb_Dataset.csv', '')
        self.assertEqual(type(response), dict)


class TestQueries(unittest.TestCase):

    def setUp(self) -> None:
        self.dataset = 'IMDb_Dataset_2.csv'

    """
    Test 1:
    
    """
    def test1(self):

        query = 'comedies with rating > 8'

        data = query_uploaded_table(self.dataset, query)
        transformed_data = transform_data_to_dict(data)

        genre_to_test = transformed_data['Genre'][0]
        IMDb_Rating_to_test = transformed_data['IMDb Rating'][0]

        self.assertEqual(genre_to_test, 'Comedy')
        self.assertGreater(float(IMDb_Rating_to_test),  8.0)

    """
    Test 2:

    """

    def test2(self):

        query = 'scary movies released before 2000'

        data = query_uploaded_table(self.dataset, query)
        transformed_data = transform_data_to_dict(data)

        genre_to_test = transformed_data['Genre'][0]
        year_to_test = transformed_data['Year'][0]

        self.assertEqual(genre_to_test, 'Horror')
        self.assertLess(int(year_to_test), 2000)

    """
    Test 3:
    
    """
    def test3(self):
        query = 'has no certificates'

        data = query_uploaded_table(self.dataset, query)
        transformed_data = transform_data_to_dict(data)

        certificates_to_test = transformed_data['Certificates'][0]

        self.assertEqual(certificates_to_test, 'Not Rated')
