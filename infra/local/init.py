import boto3

def create_table():
    endpoint_url = "http://localhost:4566"
    table_name = "DevOps1_Posts"

    ddb = boto3.client(
        "dynamodb",
        region_name="us-east-1",
        aws_access_key_id="test",
        aws_secret_access_key="test",
        endpoint_url=endpoint_url,
    )

    existing_tables = ddb.list_tables()["TableNames"]
    if table_name in existing_tables:
        print(f"Table '{table_name}' already exists.")
        return

    print(f"Creating table '{table_name}'...")
    ddb.create_table(
        TableName=table_name,
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        ProvisionedThroughput={
          "ReadCapacityUnits": 5,
          "WriteCapacityUnits": 5,
        })
    print(f"Table '{table_name}' created.")

if __name__ == "__main__":
    create_table()