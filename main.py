import os

from table_search_utils import query_uploaded_table, print_query_result
from kendra_utils import query_index
from dotenv import load_dotenv


if __name__ == '__main__':

    load_dotenv()

    file_name = "IMDb_Dataset_2.csv"

    # path_to_file = "datasets/" + file_name
    # upload_response = upload_file(path_to_file)
    # print("Response code: " + str(upload_response.status_code))

    query1 = "comedies with rating > 8"
    query2 = "has no certificates"
    query3 = "scary movies released before 2000"
    query4 = "scary movies "

    # table search querying
    query_response = query_uploaded_table(file_name, query2)
    print_query_result(query_response)

    # aws kendra querying
    index = os.getenv('INDEX_json')
    query_index(index, query2)