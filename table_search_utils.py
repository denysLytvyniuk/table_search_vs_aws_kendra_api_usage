import requests
import pandas as pd
from tabulate import tabulate


# upload file to table search
def upload_file(file_path,
                api_url="https://www.share-my-list.com/upload_647ngiuon550e840e29b41d4637644665544asdf00.html"):
    try:
        # Open the file in binary mode
        with open(file_path, 'r') as file:
            # Use requests.post to send a POST request with the file
            response = requests.post(api_url, files={'file': file})

            # Check if the request was successful
            if response.status_code == 200:
                print("File uploaded successfully!")
            else:
                print("Failed to upload file. Status code:", str(response.status_code))
            return response
    except requests.RequestException as e:
        print("Error: uploading file." + str(e))
        return None
    except FileNotFoundError as e:
        print("Error: opening file." + str(e))
        return None


def query_uploaded_table(file_name, query):
    try:
        url = "https://www.share-my-list.com/all_query_company_ds35647ngiuon550e840e29b41d46376446655440000.html"
        post_data = {"query_param": query, "db_name": file_name}
        response = requests.post(url, data=post_data)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print("Data read successfully!")
            return response.json()
        else:
            print("Error: reading data.")
    except requests.RequestException as e:
        print("Error: reading data." + str(e))
        return None


# table search api response data transforming to dictionary
def transform_data_to_dict(query_result: dict) -> dict[int: list]:
    try:

        companies = query_result['result']['companies']
        fields = query_result['result']['fields']
        # Initialize the dictionary to store the extracted data
        data = {field[0]: [] for field in fields}
        # Fill the dictionary with data from each company
        for company in companies:
            for field_name, _ in fields:
                if field_name in company['loaded_data_categories']:
                    data[field_name].append(company['loaded_data_categories'][field_name])
                elif field_name in company['company_numeric_data']:
                    data[field_name].append(company['company_numeric_data'][field_name])
                elif field_name in company['loaded_data_ids']:
                    data[field_name].append(company['loaded_data_ids'][field_name])
                elif field_name in company['company_dates_data']:
                    data[field_name].append(company['company_dates_data'][field_name])
                elif field_name in company['company_location_data']:
                    data[field_name].append(company['company_location_data'][field_name])
                elif field_name in company['company_text_data']:
                    data[field_name].append(company['company_text_data'][field_name])

        return data
    except Exception as e:
        print("Error: extracting data." + str(e))
        return None


# func to take fields needed
def IMDB_dataset_data_transforming(data: dict[str:list]):

    result_data = {'Title': data['Title'],
                   'Year': data['Year'],
                   'IMDb Rating': data['IMDb Rating'],
                   'Certificates': data['Certificates'],
                   'Genre': data['Genre'],
                   }

    return result_data


def print_query_result(query_result):
    try:
        # transform data
        data = transform_data_to_dict(query_result)
        data = IMDB_dataset_data_transforming(data)  # delete if you want to see all rows!!!!!!!!!

        # Convert the dictionary to a DataFrame for a better visualization
        extracted_df = pd.DataFrame(data)

        # Display the DataFrame using tabulate
        print(tabulate(extracted_df, headers='keys', tablefmt='psql'))
    except Exception as e:
        print("Error: printing data." + str(e))
        return None
