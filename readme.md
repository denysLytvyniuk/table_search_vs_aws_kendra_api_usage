# Comparison of Table Search and Amazon Kendra

This project compares the effectiveness of **Table Search** and **Amazon Kendra** by querying an IMDb dataset.

## Setup

### Prerequisites

1. Python 3.x
2. pip
3. AWS CLI installed and configured ([AWS CLI configuration guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html))
4. `.env` file with necessary environment variables

### Dependencies

Install the required Python packages:

```sh
pip install -r requirements.txt
```

### Environment Variables

Create a .env file in the root directory and add the following variable:

```sh
INDEX_json=<your_kendra_index_id>
```

### Conclusion

By running the provided script, you can compare the performance of Table Search and Amazon Kendra, determining which tool best meets your semantic search needs. The results will highlight the strengths and weaknesses of each approach, guiding your choice of search tool for different applications.