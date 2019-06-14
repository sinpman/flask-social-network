import datetime
from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('social.db')
class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)
    vip_member = CharField(max_length=100)
    class Meta:
        database = DATABASE
        order_by = ('-joined_at',)

    def get_posts(self):
        print(self)
        print('self')
        return Post.select().where(Post.user == self)
    def get_stream(self):
        return Post.select().where(
            (Post.user << self.following()) |
            (Post.user == self)
        )

    def get_curr_posts(self):
        return Post.select().where(Post.user == self)

    def get_stream(self):

        return Post.select().where(
            (Post.user << self.following()) |
            (Post.user == self)
        )
    
    def following(self):
        """The users that we are following."""
        print('following')
        return (
            User.select().join(
                Relationship, on=Relationship.to_user
            ).where(
                Relationship.from_user == self
            )
        )

    def current_user_post(self,post_id):
        """The users that we are following."""
        print('following')
        return Post.select().where(
            (Post.post_id == post_id) |
            (Post.user == self)
        )

    def followers(self):
        """Get users following the current user"""
        return (
            User.select().join(
                Relationship, on=Relationship.from_user
            ).where(
                Relationship.to_user == self
            )
        )

    @classmethod
    def create_user(cls, username, email, password, admin=False):

        try:
            with DATABASE.transaction():
                cls.create(
                    username=username,
                    email=email,
                    password=generate_password_hash(password),
                    is_admin=admin)
        except IntegrityError:
            raise ValueError("User already exists")



class user_profile(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(
        rel_model=User,
        related_name='user_id',
        model=""
    )
    user_id = TextField()
    username = TextField()
    profile_pic_path = TextField()
    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)



class Post(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(
        rel_model=User,
        related_name='posts',
        model=""
    )
    content = TextField()
    filename = TextField()
    filepath = TextField()
    profile_pic_path = TextField()
    user_id = TextField()
    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)

class Relationship(Model):
    from_user = ForeignKeyField(User, related_name='relationships')
    to_user = ForeignKeyField(User, related_name='related_to')
    
    class Meta:
        database = DATABASE
        indexes = (
            (('from_user', 'to_user'), True),
        )

class Relationship(Model):
    from_user = ForeignKeyField(User, related_name='relationships')
    to_user = ForeignKeyField(User, related_name='related_to')

    class Meta:
        database = DATABASE
        indexes = (
            (('from_user', 'to_user'), True),
        )

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Post, Relationship,], safe=True)
    DATABASE.close()