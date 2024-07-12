import re
import pandas as pd
from tabulate import tabulate
import json
import os

import boto3


kendra = boto3.client("kendra")


def display_results(response: dict, user_profile: str = None) -> None:
    results = []
    for i, item in enumerate(response['ResultItems']):
        score = item['ScoreAttributes']['ScoreConfidence']
        text = item['DocumentExcerpt']['Text'].replace('\n', '')
        results.append(f"{i}. [{score}] [{text}]")
    if not results:
        print("no data found for this query")
    extracted_data = []
    for string in results:
        title = re.search(r'title": "([^"]+)', string).group(1)
        year = int(re.search(r'year": (\d+)', string).group(1))
        rating = float(re.search(r'rating": ([\d.]+)', string).group(1))
        certificates = re.search(r'certificates": "([^"]+)', string).group(1)
        genre = re.search(r'genre": "([^"]+)', string).group(1)

        extracted_data.append({
            "title": title,
            "year": year,
            "rating": rating,
            "certificates": certificates,
            "genre": genre
        })

    # Convert to DataFrame
    extracted_df = pd.DataFrame(extracted_data)

    # Display the DataFrame using tabulate
    print(tabulate(extracted_df, headers='keys', tablefmt='psql'))


def batch_document(index_id, text, title):
    document = {
        "Id": "2",
        "Blob": text,
        "ContentType": "PLAIN_TEXT",
        "Title": title
    }

    result = kendra.batch_put_document(
        IndexId=index_id,
        Documents=[document]
    )
    print(result)


def query_index(index_id, query, print_results=True):
    response = kendra.query(
        QueryText=query,
        IndexId=index_id
    )
    if print_results:
        display_results(response)
    return response


def upload_metadata(json_folder, bucket):
    s3 = boto3.resource('s3')

    json_folder1 = 'jsons'

    for filename in os.listdir(json_folder):
        if filename.endswith('.json') and not filename.endswith('.metadata.json'):
            filepath = os.path.join(json_folder, filename)

            # read jsons
            with open(filepath, 'r') as file:
                data = json.load(file)

            # create metadata
            metadata = {
                "DocumentId": filename,
                "Attributes": {
                    "year": data["year"],
                    "rating": data["rating"],
                    "certificates": data.get("certificates", "Not provided"),
                    "genre": data["genre"]
                },
                "Title": data["title"],
            }

            metadata_filename = f'{filename}.metadata.json'
            metadata_filepath = os.path.join(json_folder, metadata_filename)

            with open(metadata_filepath, 'w') as metadata_file:
                json.dump(metadata, metadata_file, indent=4)

            # upload metadata to  S3
            s3.meta.client.upload_file(metadata_filepath, bucket, f'metadata/{metadata_filename}')
