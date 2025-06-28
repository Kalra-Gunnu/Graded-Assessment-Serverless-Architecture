# Importing necessary libraries
import json
import boto3
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize Amazon Comprehend client
comprehend = boto3.client('comprehend')

def lambda_handler(event, context):
    """
    AWS Lambda Function: Sentiment Analysis on Product Reviews using Amazon Comprehend

    Algorithm & Working:
    1. Extract the "reviews" list from the incoming event payload.
    2. Validate that the input is a non-empty list of strings.
    3. For each valid review:
       - Use Amazon Comprehend to detect the sentiment (`Positive`, `Negative`, `Neutral`, or `Mixed`).
       - Capture sentiment and confidence scores.
       - Log and append results.
    4. Handle and log errors for individual reviews if they occur.
    5. Return all sentiment analysis results as a JSON response.

    Purpose:
    Automates the analysis of customer feedback using NLP to identify overall sentiment in real time.
    """
    
    reviews = event.get("reviews", [])

    # Validate the input
    if not reviews or not isinstance(reviews, list):
        logger.error("No valid list of reviews provided.")
        return {
            'statusCode': 400,
            'body': json.dumps("Missing or invalid 'reviews' list in input")
        }

    # List to hold the results
    results = []

    # Process each review
    for review in reviews:
        if not isinstance(review, str) or not review.strip():
            logger.warning("Skipping empty or non-string review.")
            continue

        logger.info(f"Analyzing review: {review}")
        # Analyze sentiment using Amazon Comprehend
        try:
            response = comprehend.detect_sentiment(
                Text=review,
                LanguageCode='en'
            )

            result = {
                "review": review,
                "sentiment": response["Sentiment"],
                "scores": response["SentimentScore"]
            }

            results.append(result)

        except Exception as e:
            logger.error(f"Error analyzing review: {str(e)}")
            results.append({
                "review": review,
                "error": str(e)
            })
            
    # Final results
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }
