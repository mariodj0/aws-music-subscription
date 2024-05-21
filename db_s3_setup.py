import json # [5]
import time # [6]
import requests # [1]
import boto3 # [2]
from botocore.exceptions import ClientError

# Function to create a DynamoDB table
# Reference: [3]
def create_table(dynamodb):
    try:
        # Create a table with specified schema
        table = dynamodb.create_table(
            TableName="music",
            KeySchema=[
                {
                    "AttributeName": "title",
                    "KeyType": "HASH"
                },
            ],
            AttributeDefinitions=[
                {
                    "AttributeName": "title",
                    "AttributeType": "S"
                },
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5
            }
        )
        return table
    except ClientError as e:
        print(e.response["Error"]["Message"])

# Function to add a song to the DynamoDB table
# Reference: [3]
def load_data(song, dynamodb):
    try:
        dynamodb.put_item(TableName="music", Item=song)
        print(f"Successfully added song: {song['title']}")
    except ClientError as e:
        print(e.response["Error"]["Message"])

# Function to download an image from a URL
# Reference: [1]
def download_image(image_url):
    response = requests.get(image_url)
    return response.content  #get response content from image url

# Function to upload an image to an S3 bucket
# Reference: [4] Amazon Simple Storage Service (S3)
def upload_image_to_s3(image_data, file_name, bucket_name):
    s3 = boto3.resource("s3")
    s3_object = s3.Object(bucket_name, file_name)
    s3_object.put(Body=image_data)
    file_name = file_name.replace(" ", "+")
    url =  "https://%s.s3.amazonaws.com/%s" % (bucket_name, file_name)
    return url # return url of image in s3 bucket

# Main function
def main():
    # Set up AWS session and DynamoDB client
    # References: [2], [3], [4]
    session = boto3.Session(region_name="us-east-1")
    dynamodb = session.client("dynamodb")
    s3 = session.client("s3")

    # Check if S3 bucket already exists
    bucket_name = "mdk-music-bucket1"
    try:
        s3.head_bucket(Bucket=bucket_name)
        print(f"S3 bucket {bucket_name} already exists.")
    except ClientError:
        # Create S3 bucket
        s3.create_bucket(Bucket=bucket_name)
        print(f"S3 bucket {bucket_name} created.")

    # Create the table
    music_table = create_table(dynamodb)

    # Sleep for 10 seconds to allow table to be created
    time.sleep(10)

    # Read the JSON file with song data
    # Reference: [5]
    with open("a1.json", "r") as f:
        song_data = json.load(f)

    # Download images and upload to S3 bucket
    for song in song_data["songs"]: #iterate through each song in the json file
        image_url = song["img_url"]
        artist_name = song["artist"]
        file_name = f"{artist_name}.jpg" #file name for raw image data
        image_data = download_image(image_url)
        url = upload_image_to_s3(image_data, file_name, bucket_name)
        song["img_url"] = url
        # Create a song item with the required attributes
        song_item = {
            "title": {"S": song["title"]},
            "artist": {"S": song["artist"]},
            "year": {"S": song["year"]},
            "web_url": {"S": song["web_url"]},
            "img_url": {"S": song["img_url"]},

        }
        # Add the song item to the DynamoDB table
        load_data(song_item, dynamodb)

# Run the main function
if __name__ == "__main__":
    main()


# Bibliography:
# [1] A. Grinberg, "requests," PyPI, 2021. [Online]. Available: https://pypi.org/project/requests/. [Accessed April 7, 2023].
# [2] Amazon Web Services, "Boto3," 2021. [Online]. Available: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html. [Accessed April 7, 2023].
# [3] Amazon Web Services, "Amazon DynamoDB," 2021. [Online]. Available: https://aws.amazon.com/dynamodb/. [Accessed April 7, 2023].
# [4] Amazon Web Services, "Amazon Simple Storage Service (S3)," 2021. [Online]. Available: https://aws.amazon.com/s3/. [Accessed April 7, 2023].
# [5] K. Reitz and T. Slattery, "json," Python Standard Library, 2021. [Online]. Available: https://docs.python.org/3/library/json.html. [Accessed April 7, 2023].
# [6] G. van Rossum, F. L. Drake, and B. Cannon, "time," Python Standard Library, 2021. [Online]. Available: https://docs.python.org/3/library/time.html. [Accessed April 7, 2023].
