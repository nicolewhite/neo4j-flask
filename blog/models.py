from py2neo import Graph, Node, Relationship, authenticate
from passlib.hash import bcrypt
from datetime import datetime
import os
import uuid

url = os.environ.get('NEO4J_URL', 'http://localhost:7474')
username = os.environ.get('NEO4J_USERNAME')
password = os.environ.get('NEO4J_PASSWORD')

if username and password:
    authenticate(url.strip('http://'), username, password)

graph = Graph(url + '/db/data/')

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
        if not self.find():
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
        MATCH (you:User)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag:Tag),
              (they:User)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag)
        WHERE you.username = {username} AND you <> they
        WITH they, COLLECT(DISTINCT tag.name) AS tags, COUNT(DISTINCT tag) AS len
        ORDER BY len DESC LIMIT 3
        RETURN they.username AS similar_user, tags
        """

        return graph.cypher.execute(query, username=self.username)

    def get_commonality_of_user(self, username):
        # Find how many of the logged-in user's posts the other user
        # has liked and which tags they've both blogged about.
        query = """
        MATCH (they:User {username:{they}}),
              (you:User {username:{you}})
        OPTIONAL MATCH (they)-[:LIKED]->(post:Post)<-[:PUBLISHED]-(you)
        OPTIONAL MATCH (they)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag:Tag),
                       (you)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag)
        RETURN COUNT(DISTINCT post) AS likes, COLLECT(DISTINCT tag.name) AS tags
        """

        return graph.cypher.execute(query, they=username, you=self.username)[0]


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

    return graph.cypher.execute(query, username=username)

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

    return graph.cypher.execute(query, today=date())

def timestamp():
    epoch = datetime.utcfromtimestamp(0)
    now = datetime.now()
    delta = now - epoch
    return delta.total_seconds()

def date():
    return datetime.now().strftime('%F')