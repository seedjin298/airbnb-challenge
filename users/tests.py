from rest_framework.test import APITestCase
from .models import User
from tweets.models import Tweet


class TestUsersView(APITestCase):

    USERNAME = "Test User"
    NAME = "Test Name"
    GENDER = "male"
    URL = "/api/v1/users/"

    def setUp(self):
        user = User.objects.create(
            username=self.USERNAME,
            name=self.NAME,
            gender=self.GENDER,
        )
        user.set_password("123")
        user.save()
        self.user = user

    def test_all_users(self):

        response = self.client.get(self.URL)
        data = response.json()
        # print(data)
        # [{'username': 'Test User', 'gender': 'male'}]

        self.assertEqual(
            response.status_code,
            200,
            "Status code isn't 200",
        )

        self.assertIsInstance(
            data,
            list,
        )
        self.assertEqual(
            len(data),
            1,
        )
        self.assertEqual(
            data[0]["username"],
            self.USERNAME,
        )
        self.assertEqual(
            data[0]["gender"],
            self.GENDER,
        )

    def test_create_user(self):
        test_username = "test_username"
        test_password = "test_password"

        response = self.client.post(self.URL)

        self.assertEqual(
            response.status_code,
            400,
        )

        response = self.client.post(
            self.URL,
            data={
                "username": test_username,
                "password": test_password,
                "gender": self.GENDER,
            },
        )

        self.assertEqual(
            response.status_code,
            200,
            "Status code isn't 200",
        )

        data = response.json()
        # print(data)
        # {'id': 2, 'username': 'test_username', 'name': '', 'first_name': '', 'last_name': '', 'email': '', 'gender': 'male'}

        self.assertEqual(
            data["username"],
            test_username,
        )
        self.assertEqual(
            data["gender"],
            self.GENDER,
        )


class TestUserView(APITestCase):

    USERNAME = "Test User"
    NAME = "Test Name"

    DIFF_USERNAME = "Diff User"
    DIFF_NAME = "Diff Name"

    GENDER = "male"
    URL = "/api/v1/users/"

    def setUp(self):
        user = User.objects.create(
            username=self.USERNAME,
            name=self.NAME,
            gender=self.GENDER,
        )
        user.set_password("123")
        user.save()
        self.user = user

        diff_user = User.objects.create(
            username=self.DIFF_USERNAME,
            name=self.DIFF_NAME,
            gender=self.GENDER,
        )
        diff_user.set_password("123")
        diff_user.save()
        self.diff_user = diff_user

    def test_user_not_found(self):
        response = self.client.get(self.URL + "3/")

        self.assertEqual(response.status_code, 404)

    def test_get_user(self):
        response = self.client.get(self.URL + "1/")

        self.assertEqual(response.status_code, 200)

        data = response.json()
        # print(data)
        # {'id': 1, 'username': 'Test User', 'name': 'Test Name', 'first_name': '', 'last_name': '', 'email': '', 'gender': 'male'}

        self.assertEqual(
            data["username"],
            self.USERNAME,
        )
        self.assertEqual(
            data["name"],
            self.NAME,
        )
        self.assertEqual(
            data["gender"],
            self.GENDER,
        )

    def test_put_user(self):
        new_username = "new_username"
        new_name = "new_name"
        new_email = "newemail@gmail.com"
        new_gender = "female"
        wrong_data = "Wrong Data"

        response = self.client.put(self.URL + "1/")
        self.assertEqual(response.status_code, 403)

        self.client.force_login(
            self.diff_user,
        )
        response = self.client.put(self.URL + "1/")
        self.assertEqual(response.status_code, 403)

        self.client.force_login(
            self.user,
        )
        response = self.client.put(
            self.URL + "1/",
            data={
                "wrong_data": wrong_data,
            },
        )
        self.assertEqual(response.status_code, 400)

        response = self.client.put(
            self.URL + "1/",
            data={
                "username": new_username,
                "name": new_name,
                "email": new_email,
                "gender": new_gender,
            },
        )
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(
            data["username"],
            new_username,
        )
        self.assertEqual(
            data["name"],
            new_name,
        )
        self.assertEqual(
            data["gender"],
            new_gender,
        )
        self.assertEqual(
            data["email"],
            new_email,
        )


class TestUserTweetsView(APITestCase):

    USERNAME = "Test User"
    NAME = "Test Name"
    GENDER = "male"
    PAYLOAD = "Test Payload"
    URL = "/api/v1/users/1/tweets/"

    def setUp(self):
        user = User.objects.create(
            username=self.USERNAME,
            name=self.NAME,
            gender=self.GENDER,
        )
        user.set_password("123")
        user.save()
        self.user = user

        Tweet.objects.create(
            user=self.user,
            payload=self.PAYLOAD,
        )

    def test_get_user_tweet(self):
        response = self.client.get(self.URL)
        data = response.json()
        # print(data)
        # [{'id': 1, 'user': 'Test User', 'payload': 'Test Payload', 'updated_at': '2024-10-12T15:38:06.671432Z'}]

        self.assertEqual(
            response.status_code,
            200,
            "Status code isn't 200",
        )

        self.assertIsInstance(
            data,
            list,
        )
        self.assertEqual(
            len(data),
            1,
        )
        self.assertEqual(
            data[0]["user"],
            self.USERNAME,
        )
        self.assertEqual(
            data[0]["payload"],
            self.PAYLOAD,
        )


class TestUserChangePassword(APITestCase):
    USERNAME = "Test User"
    NAME = "Test Name"
    GENDER = "male"
    PASSWORD = "Test_Password"
    URL = "/api/v1/users/password/"

    def setUp(self):
        user = User.objects.create(
            username=self.USERNAME,
            name=self.NAME,
            gender=self.GENDER,
        )
        user.set_password(self.PASSWORD)
        user.save()
        self.user = user

    def test_change_password(self):
        new_password = "new_password"
        wrong_password = "wrong_passwrod"
        response = self.client.put(self.URL)
        self.assertEqual(response.status_code, 403)

        self.client.force_login(
            self.user,
        )

        response = self.client.put(self.URL)
        self.assertEqual(response.status_code, 400)

        response = self.client.put(
            self.URL,
            data={
                "old_password": self.PASSWORD,
            },
        )
        self.assertEqual(response.status_code, 400)

        response = self.client.put(
            self.URL,
            data={
                "new_password": new_password,
            },
        )
        self.assertEqual(response.status_code, 400)

        response = self.client.put(
            self.URL,
            data={
                "old_password": wrong_password,
                "new_password": new_password,
            },
        )
        self.assertEqual(response.status_code, 400)

        response = self.client.put(
            self.URL,
            data={
                "old_password": self.PASSWORD,
                "new_password": self.PASSWORD,
            },
        )
        self.assertEqual(response.status_code, 400)

        response = self.client.put(
            self.URL,
            data={
                "old_password": self.PASSWORD,
                "new_password": new_password,
            },
        )
        self.assertEqual(response.status_code, 200)

        self.client.logout()
        self.client.login(
            username=self.USERNAME,
            password=new_password,
        )


class TestUserLogIn(APITestCase):
    USERNAME = "Test User"
    NAME = "Test Name"
    PASSWORD = "123"

    DIFF_USERNAME = "Diff User"
    DIFF_NAME = "Diff Name"

    GENDER = "male"
    URL = "/api/v1/users/login/"

    def setUp(self):
        user = User.objects.create(
            username=self.USERNAME,
            name=self.NAME,
            gender=self.GENDER,
        )
        user.set_password(self.PASSWORD)
        user.save()
        self.user = user

        diff_user = User.objects.create(
            username=self.DIFF_USERNAME,
            name=self.DIFF_NAME,
            gender=self.GENDER,
        )
        diff_user.set_password(self.PASSWORD)
        diff_user.save()
        self.diff_user = diff_user

    def test_login(self):
        wrong_user = "wrong_user"
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 405)

        response = self.client.post(self.URL)
        self.assertEqual(response.status_code, 400)

        response = self.client.post(
            self.URL,
            data={
                "username": wrong_user,
                "password": wrong_user,
            },
        )
        self.assertEqual(response.status_code, 400)

        response = self.client.post(
            self.URL,
            data={
                "username": self.USERNAME,
                "password": wrong_user,
            },
        )
        self.assertEqual(response.status_code, 400)

        response = self.client.post(
            self.URL,
            data={
                "username": wrong_user,
                "password": self.PASSWORD,
            },
        )
        self.assertEqual(response.status_code, 400)

        response = self.client.post(
            self.URL,
            data={
                "username": self.USERNAME,
                "password": self.PASSWORD,
            },
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.URL,
            data={
                "username": self.DIFF_USERNAME,
                "password": self.PASSWORD,
            },
        )
        self.assertEqual(response.status_code, 200)


class TestUserLogOut(APITestCase):
    USERNAME = "Test User"
    NAME = "Test Name"
    PASSWORD = "123"

    GENDER = "male"
    URL = "/api/v1/users/logout/"

    def setUp(self):
        user = User.objects.create(
            username=self.USERNAME,
            name=self.NAME,
            gender=self.GENDER,
        )
        user.set_password(self.PASSWORD)
        user.save()
        self.user = user

    def test_logout(self):
        response = self.client.post(self.URL)
        self.assertEqual(response.status_code, 403)

        self.client.force_login(
            self.user,
        )
        response = self.client.post(self.URL)
        self.assertEqual(response.status_code, 200)
