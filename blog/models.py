from py2neo import Graph, Node, Relationship
from passlib.hash import bcrypt
import os

graph = Graph(os.environ.get('GRAPHENEDB_URL', 'http://localhost:7474') + '/db/data/')

## The User class.
## This class is for handling the currently-logged-in user.
class User:
    def __init__(self, username):
        self.username = username

    def find(self):
        user = graph.find_one("User", "username", self.username)
        return user

    def set_password(self, password):
        self.password = bcrypt.encrypt(password)
        return self

    def register(self):
        if not self.password:
            return False
        elif not self.find():
            user = Node("User", username=self.username, password=self.password)
            graph.create(user)
            return True
        else:
            return False

    def verify_password(self, password):
        user = self.find()
        if user:
            return bcrypt.verify(password, user['password'])
        else:
            return False

    def add_post(self, title, tags, text):
        import uuid

        user = self.find()
        post = Node(
            "Post",
            id=str(uuid.uuid4()),
            title=title,
            text=text,
            timestamp=timestamp(),
            date=date()
        )
        rel = Relationship(user, "PUBLISHED", post)
        graph.create(rel)

        tags = [x.strip() for x in tags.lower().split(',')]
        for t in tags:
            tag = graph.merge_one("Tag", "name", t)
            rel = Relationship(tag, "TAGGED", post)
            graph.create(rel)

    def like_post(self, post_id):
        user = self.find()
        post = graph.find_one("Post", "id", post_id)
        graph.create_unique(Relationship(user, "LIKED", post))

    def get_similar_users(self):
        # Find three users who are most similar to the logged-in user
        # based on tags they've both blogged about.
        query = """
        MATCH (u1:User)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag:Tag),
              (u2:User)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag)
        WHERE u1.username = {username} AND u1 <> u2
        WITH u2, COLLECT(DISTINCT tag.name) AS tags, COUNT(DISTINCT tag) AS len
        ORDER BY len DESC LIMIT 3
        RETURN u2.username AS similar_user, tags
        """

        similar = graph.cypher.execute(query, username=self.username)
        return similar

    def get_commonality_of_user(self, username):
        # Find how many of the logged-in user's posts the other user
        # has liked and which tags they've both blogged about.
        query = """
        MATCH (user1:User {username:{user_viewing}}),
              (user2:User {username:{user_loggedin}})
        OPTIONAL MATCH (user1)-[:LIKED]->(post:Post)<-[:PUBLISHED]-(user2)
        OPTIONAL MATCH (user1)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag:Tag),
                       (user2)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag)
        RETURN COUNT(DISTINCT post) AS likes, COLLECT(DISTINCT tag.name) AS tags
        """

        result = graph.cypher.execute(query,
                                      user_viewing=username,
                                      user_loggedin=self.username)

        result = result[0]
        common = dict()
        common['likes'] = result.likes
        common['tags'] = result.tags if len(result.tags) > 0 else None
        return common

## Various functions.
## These are for the views.

# For the profile/<username> view.
def get_users_recent_posts(username):
    query = """
    MATCH (:User {username:{username}})-[:PUBLISHED]->(post:Post),
          (tag:Tag)-[:TAGGED]->(post)
    RETURN post.id AS id,
           post.date AS date,
           post.timestamp AS timestamp,
           post.title AS title,
           post.text AS text,
           COLLECT(tag.name) AS tags
    ORDER BY timestamp DESC
    LIMIT 5
    """

    posts = graph.cypher.execute(query, username=username)
    return posts

# For the / view.
def get_todays_recent_posts():
    query = """
    MATCH (post:Post {date: {today}}),
          (user:User)-[:PUBLISHED]->(post),
          (tag:Tag)-[:TAGGED]->(post)
    RETURN user.username AS username,
           post.id AS id,
           post.date AS date,
           post.timestamp AS timestamp,
           post.title AS title,
           post.text AS text,
           COLLECT(tag.name) AS tags
    ORDER BY timestamp DESC
    LIMIT 5
    """

    posts = graph.cypher.execute(query, today = date())
    return posts

## Helper functions.
from datetime import datetime

def timestamp():
    unix = int(datetime.now().strftime('%s'))
    return unix

def date():
    today = datetime.now().strftime('%Y-%m-%d')
    return today
