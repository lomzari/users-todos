from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_todos_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Don't req CSRF for testing
app.config['WTF_CSRF_ENABLED'] = False

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Make demo data."""

        User.query.delete()

        user = User(username="lester", 
            email="test@test.com", 
            first_name="lester", 
            last_name="testowitz"
        )
        db.session.add(user)

        user2 = User(username="esther", 
            email="test@test.com", 
            first_name="esther", 
            last_name="testowitz"
        )

        db.session.add(user2)
        db.session.commit()

        self.username = user.username

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_users_index(self):

        with app.test_client() as client:

            response = client.get("/users")
            html_response = response.get_data(as_text=True)

            # Is the main heading in the template?
            self.assertIn("<h1>See all the users!</h1>", html_response)

            # Is the user I create in my test, inside of this template?
            self.assertIn('<a href="/users/lester">See more about lester</a>', html_response)
            self.assertIn('<a href="/users/esther">See more about esther</a>', html_response)


    def test_user_show(self):

        with app.test_client() as client:

            response = client.get(f"/users/{self.username}")
            html_response = response.get_data(as_text=True)

            self.assertIn("<h1>See more information about lester</h1>", html_response)
            self.assertNotIn("<h1>See more information about esther</h1>", html_response)
    
    def test_user_show_not_found(self):

        with app.test_client() as client:

            response = client.get("/users/taco")
            html_response = response.get_data(as_text=True)

            self.assertIn("<h1>Not Found</h1>", html_response)
