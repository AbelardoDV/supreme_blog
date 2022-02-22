from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Post


class TestUserMethods(unittest.TestCase):
    def setUp(self) -> None:
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            'sqlite://'
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self) -> None:
        u = User(username='test_user')
        u.set_password('123')
        self.assertTrue(u.check_password('123'))
        self.assertFalse(u.check_password('12x'))

    def test_avatar(self) -> None:
        u = User(username='test_user_2', email='hola@pucp.com')
        self.assertIsNotNone(u.get_avatar_link(128))

    def test_follow(self) -> None:
        u1 = User(username='user1')
        u2 = User(username='user2')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followed.count(), 0)

        u1.follow(u2)
        u2.follow(u1)
        db.session.commit()
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, u2.username)
        self.assertEqual(u2.followed.count(), 1)
        self.assertEqual(u2.followed.first().username, u1.username)

        u1.unfollow(u2)
        u2.unfollow(u1)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followed.count(), 0)

    def test_follow_posts(self) -> None:
        user1 = User(username='user1', email='user1@pucp.pe')
        user2 = User(username='user2', email='user2@pucp.pe')
        user3 = User(username='user3', email='user3@pucp.pe')
        user4 = User(username='user4', email='user4@pucp.pe')
        db.session.add_all([user1, user2, user3, user4])

        post1 = Post(body='body1', author=user1,
                     timestamp=datetime.utcnow()+timedelta(4))
        post2 = Post(body='body1', author=user2,
                     timestamp=datetime.utcnow()+timedelta(3))
        post3 = Post(body='body2', author=user3,
                     timestamp=datetime.utcnow()+timedelta(2))
        post4 = Post(body='body3', author=user4,
                     timestamp=datetime.utcnow()+timedelta(1))
        db.session.add_all([post1, post2, post3, post4])

        db.session.commit()

        user1.follow(user2)
        user1.follow(user3)
        user1.follow(user4)

        db.session.commit()

        self.assertEqual(user1.followed_posts().all(),
                         [post1, post2, post3, post4])


if __name__ == '__main__':
    unittest.main(verbosity=2)
