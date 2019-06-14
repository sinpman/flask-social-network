import sqlite3
import models
import peewee
from flask_login import UserMixin

conn = sqlite3.connect('social.db')

# cur=conn.execute('SELECT "t1"."id", "t1"."timestamp", "t1"."user_id", "t1"."user_id", "t1"."username", "t1"."profile_pic_path" FROM "user_profile" AS "t1" WHERE ("t1"."username" LIKE "Karan")')
# cur=conn.execute('SELECT "t1"."id", "t1"."timestamp", "t1"."user_id", "t1"."user_id", "t1"."username", "t1"."profile_pic_path" FROM "user_profile" AS "t1" WHERE ("t1"."username" LIKE "Karan")')
# for i in cur:
#     print(i)
#
# a=models.user_profile.create(user_id='1',
#                                profile_pic_path='test',
#                                        id='1'
#                                        )
#
# print(models.user_profile.create(user_id='1',
#                                profile_pic_path='test',
#                                        id='1'
#                                        ))
# print(cur.description)

# cur1=conn.execute('update user_profile set profile_pic_path="static/img/Profile/Karan123/10703972_10203218137550234_7403270267379251558_n.jpg"')
# conn.commit()
# cur=conn.execute('select * from post ')
# for i in cur:
#     print(i)
#
#
# print(cur.description)
# a=models.user_profile.user_id.in_(models.Post.select(models.Post.user_id).order_by(models.Post.timestamp.desc()).where(models.Post.id == '1'))
# sql, param = a.sql()
# print(a.sql())


# query = models.user_profile.user_id.in_(models.Post.select(models.Post.user_id).order_by(models.Post.timestamp.desc()).where(models.Post.id == '1'))
# sql, param = query.sql()
# print(sql.replace("?","{}").format(*param))

# print(models.user_profile.create(user_id='1',
#                                profile_pic_path='test',
#                                        id='1'
#                                        ))


# query = (models.User.select(models.User.id).join(models.user_profile, on=models.user_profile.user_id))
#
# print(query)


query=models.User.select().join(peewee.JOIN.LEFT_OUTER,
    models.Relationship,  on=models.Relationship.to_user
            ).where(
    models.Relationship.from_user == '2'
            )
for i in query:
    print(i.username)