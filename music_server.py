from flask import Flask, jsonify, request # [1]
from flask_cors import CORS, cross_origin # [2]
import boto3 # [3]
from boto3.dynamodb.conditions import Attr, Key

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

dynamodb = boto3.resource("dynamodb", region_name="us-east-1") # [3]
table = dynamodb.Table("login")

# Login function verifies the user credentials
# References: [1], [3]
@app.route("/login", methods=["POST"])
@cross_origin()
def login():
    data = request.get_json() # get json data from request
    username = data.get("email")
    password = data.get("password")
    print(username, password)

    # Check if user exists in DynamoDB
    response = table.get_item( # gquery table
        Key={
            "email": username
        }
    )

    if "Item" not in response:
        return jsonify({"message": "User not found"}), 404

    user = response["Item"] # log user response

    # Check if password is correct
    if user["password"] != password:
        return jsonify({"message": "Invalid password"}), 401

    return jsonify({"message": "Login successful"})

# Register function registers a new user
# References: [1], [3]
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json() # get json data from request
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    print(email, username, password)

    # Check if user exists in DynamoDB
    response = table.get_item(
        Key={
            "email": email
        }
    )

    if "Item" in response:
        return jsonify({"message": "User already exists"}), 409

    # Add user to DynamoDB
    table.put_item(
        Item={
            "email": email,
            "user_name": username,
            "password": password
        }
    )

    return jsonify({"message": "User created successfully"}), 201

# User details function retrieves the user"s music details and subscriptions
# References: [1], [3]
@app.route("/user_details", methods=["POST"])
@cross_origin()
def user_details():
    subscription_table = dynamodb.Table("subscription")
    music_table = dynamodb.Table("music")

    data = request.get_json() # get json data from request
    email = data.get("email")

    # Check if user exists in DynamoDB
    user_response = table.get_item(
        Key={
            "email": email
        }
    )

    if "Item" not in user_response:
        return jsonify({"message": "User not found"}), 404

    user_name = user_response["Item"]["user_name"] # show username in site

    # Get subscriptions for the user
    subscription_response = subscription_table.scan(
        FilterExpression=Attr("email").eq(email)
    )

    if "Items" not in subscription_response:
        return jsonify({"message": "No subscriptions found"}), 404

    subscriptions = subscription_response["Items"]

    # Extract song titles from subscriptions
    song_titles = [subscription["title"] for subscription in subscriptions]

    # Fetch music details from the music table
    music_details = [] # list array of music details
    for title in song_titles:
        music_response = music_table.get_item(
            Key={
                "title": title
            }
        )

        if "Item" in music_response:
            music_item = {
                "title": music_response["Item"]["title"],
                "artist": music_response["Item"]["artist"],
                "img_url": music_response["Item"]["img_url"],
                "web_url": music_response["Item"]["web_url"],
                "year": music_response["Item"]["year"]
            }
            music_details.append(music_item)

    return jsonify({
        "user_name": user_name,
        "music_details": music_details
    }), 200

# Remove subscription function removes a user"s subscription to a song
# References: [1], [3]
@app.route("/remove_subscription", methods=["POST"])
@cross_origin()
def remove_subscription():
    data = request.get_json() # get json data from request
    email = data.get("email")
    title = data.get("title")
    subscription_table = dynamodb.Table("subscription")
    try:
        # Check if the subscription exists in the subscription table
        response = subscription_table.query(
            KeyConditionExpression=Key("email").eq(email) & Key("title").eq(title)
        )

        if "Items" not in response or len(response["Items"]) == 0:
            return jsonify({"message": "Subscription not found"}), 404

        # Remove the subscription from the subscription table
        subscription_table.delete_item(
            Key={
                "email": email,
                "title": title
            }
        )

        return jsonify({"message": "Subscription removed successfully"}), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"message": "Error removing subscription"}), 500

# Query function searches the music table based on the provided filters
# References: [1], [3]
@app.route("/query", methods=["POST"])
def query():
    data = request.get_json() # get json data from request
    title = data.get("title", "")
    year = data.get("year", "")
    artist = data.get("artist", "")

    music_table = dynamodb.Table("music")

    filter_expression = None

    if title:
        filter_expression = Attr("title").begins_with(title)

    if year:
        year_filter = Attr("year").begins_with(year)
        if filter_expression is not None:
            filter_expression = filter_expression & year_filter
        else:
            filter_expression = year_filter
        # filter_expression = filter_expression & year_filter if filter_expression else year_filter

    if artist:
        artist_filter = Attr("artist").begins_with(artist)
        if filter_expression is not None:
            filter_expression = filter_expression & artist_filter
        else:
            filter_expression = artist_filter
        # filter_expression = filter_expression & artist_filter if filter_expression else artist_filter

    if filter_expression:
        response = music_table.scan(
            FilterExpression=filter_expression
        )
        items = response["Items"] # if filter expression is not None, show filtered items
    else:
        response = music_table.scan() # show all items
        items = response["Items"]

    return jsonify({"results": items})

# Add subscription function adds a new subscription for the user
# References: [1], [3]
@app.route("/add_subscription", methods=["POST"])
def add_subscription():
    data = request.get_json() # get json data from request
    email = data.get("email")
    title = data.get("title")

    subscription_table = dynamodb.Table("subscription")
    # Check if subscription already exists in the "subscription" table
    response = subscription_table.get_item(
        Key={
            "email": email,
            "title": title
        }
    )

    if "Item" in response:
        return jsonify({"message": "Subscription already exists"}), 409

    # Add the subscription to the "subscription" table
    subscription_table.put_item(
        Item={
            "email": email,
            "title": title
        }
    )

    return jsonify({"message": "Subscription added successfully"}), 201


if __name__ == "__main__":
    app.run(port=8000, debug=False)

# Bibliography:
# [1] A. Ronacher, "Flask (A Python Microframework)", 2021. [Online]. Available: https://flask.palletsprojects.com/en/2.1.x/. [Accessed April 7, 2023].
# [2] C. Kief, "Flask-CORS", 2021. [Online]. Available: https://flask-cors.readthedocs.io/en/latest/. [Accessed April 7, 2023].
# [3] Amazon Web Services, "Boto3", 2021. [Online]. Available: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html. [Accessed April 7, 2023].