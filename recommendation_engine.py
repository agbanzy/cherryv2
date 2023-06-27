# File: /cherryAI/recommendation_engine.py

from pymongo import MongoClient

def recommend_articles(user_id):
    """
    Recommend articles to a user based on their reading history.

    Parameters:
    user_id (str): The ID of the user.

    Returns:
    list: The recommended articles.
    """
    client = MongoClient("mongodb+srv://innoedgetech:W4UyYBXqQGRrSiNB@cluster0.mongodb.net/test")
    db = client.cherryAI
    users = db.users
    articles = db.articles

    user = users.find_one({'_id': user_id})
    if not user:
        return []

    read_articles = user.get('read_articles', [])
    read_tags = [article['tags'] for article in articles.find({'_id': {'$in': read_articles}})]

    # Flatten the list of tags
    read_tags = [tag for tags in read_tags for tag in tags]

    # Find articles with similar tags that the user hasn't read yet
    recommended_articles = articles.find({
        'tags': {'$in': read_tags},
        '_id': {'$nin': read_articles}
    })

    return list(recommended_articles)
