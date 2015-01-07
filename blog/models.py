from py2neo import Graph, Node, Relationship
from passlib.hash import bcrypt
from datetime import datetime
import uuid

graph = Graph()

# The User class.
# This class if for handling the currently-logged-in user.
class User:
    def __init__(self, username):
        self.username = username

    def find(self):
        user = graph.find_one("User", "username", self.username)
        return user

    def set_password(self, password):
        self.password = bcrypt.encrypt(password)
        return self

    def verify_password(self, password):
        user = self.find()
        if user:
            return bcrypt.verify(password, user['password'])
        else:
            return False

    def register(self):
        if not self.password:
            return False
        elif not self.find():
            user = Node("User", username=self.username, password=self.password)
            graph.create(user)
            return True
        else:
            return False

    def add_post(self, title, tags, text):
        user = self.find()

        post = Node(
            "Post",
            id=str(uuid.uuid4()),
            title=title,
            text=text,
            timestamp=int(datetime.now().strftime('%s')),
            date=datetime.now().strftime('%Y-%m-%d')
        )

        rel = Relationship(user, "PUBLISHED", post)
        graph.create(rel)

        tags = tags.replace(' ', '').lower().split(',')
        for t in tags:
            tag = graph.merge_one("Tag", "name", t)
            rel = Relationship(tag, "TAGGED", post)
            graph.create(rel)

    def like_post(self, post_id):
        user = self.find()
        post = graph.find_one("Post", "id", post_id)
        graph.create_unique(Relationship(user, "LIKED", post))

    def get_similar_users(self):
        query = """
        MATCH (u1:User)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag:Tag),
              (u2:User)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag)
        WHERE u1.username = {username} AND u1 <> u2
        WITH u1, u2, COLLECT(DISTINCT tag.name) AS tags
        WITH u2, tags, LENGTH(tags) AS len
        ORDER BY len DESC
        LIMIT 3
        RETURN u2.username AS other_user, tags
        """

        similar = graph.cypher.execute(query, username=self.username)
        return similar

    def get_commonality_of_user(self, username):
        query = """
        MATCH (user1:User {username:{user_profile}}),
              (user2:User {username:{user_loggedin}})
        OPTIONAL MATCH (user1)-[:LIKED]->(post:Post)<-[:PUBLISHED]-(user2)
        OPTIONAL MATCH (user1)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag:Tag),
                       (user2)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag)
        RETURN COUNT(post) AS likes, COLLECT(DISTINCT tag.name) AS tags
        """

        result = graph.cypher.execute(query,
                                      user_profile=username,
                                      user_loggedin=self.username)

        result = result[0]
        likes = result.likes
        tags = result.tags

        response = '{} has liked {} of your posts and '.format(username, likes)

        if len(tags) == 0:
            response = response + ' does not blog about any of the same tags.'
        else:
            response = response + \
                       ' also blogs about ' + \
                        oxford_comma(tags)
        return response


## Various functions.

# For the profile/<username> view.
def get_users_recent_posts(username):
    query = """
    MATCH (:User {username:{username}})-[:PUBLISHED]->(post:Post)
    WITH post
    ORDER BY post.timestamp
    LIMIT 5
    MATCH (tag:Tag)-[:TAGGED]->(post)
    RETURN post.id AS id,
           post.date AS date,
           post.title AS title,
           post.text AS text,
           COLLECT(tag.name) AS tags
    """

    posts = graph.cypher.execute(query, username=username)
    return posts

# For the / view.
def get_global_recent_posts():
    query = """
    MATCH (post:Post)
    WITH post
    ORDER BY post.timestamp
    LIMIT 5
    MATCH (user:User)-[:PUBLISHED]->(post),
          (tag:Tag)-[:TAGGED]->(post)
    RETURN user.username AS username,
           post.id AS id,
           post.date AS date,
           post.title AS title,
           post.text AS text,
           COLLECT(tag.name) AS tags
    """

    posts = graph.cypher.execute(query)
    return posts

# Helper functions.
def oxford_comma(words):
    if len(words) == 1:
        response = words[0] + '.'
    elif len(words) == 2:
        response = ' and '.join(words) + '.'
    elif len(words) > 2:
        response = ', '.join(words[:-1]) + 'and ' + words[-1] + '.'

    return response

def timestamp_to_date(timestamp):
    date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    return date

# Uniqueness constraints.
def init_db():
    graph.schema.create_uniqueness_constraint("User", "username")
    graph.schema.create_uniqueness_constraint("Post", "id")
    graph.schema.create_uniqueness_constraint("Tag", "name")