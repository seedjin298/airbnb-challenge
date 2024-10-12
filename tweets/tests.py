from rest_framework.test import APITestCase
from . import models
from users.models import User


class TestTweetsView(APITestCase):

    USERNAME = "Test User"
    NAME = "Test Name"
    GENDER = "male"
    PAYLOAD = "Test Payload"
    URL = "/api/v1/tweets/"

    def setUp(self):
        user = User.objects.create(
            username=self.USERNAME,
            name=self.NAME,
            gender=self.GENDER,
        )
        user.set_password("123")
        user.save()
        self.user = user

        models.Tweet.objects.create(
            user=self.user,
            payload=self.PAYLOAD,
        )

    def test_all_tweets(self):
        response = self.client.get(self.URL)
        data = response.json()

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

    def test_create_tweet(self):
        new_payload = "New Payload"

        response = self.client.post(self.URL)

        self.assertEqual(
            response.status_code,
            403,
            "Status code isn't 403",
        )

        self.client.force_login(
            self.user,
        )

        response = self.client.post(self.URL)

        self.assertEqual(
            response.status_code,
            400,
            "Status code isn't 400",
        )

        response = self.client.post(
            self.URL,
            data={
                "payload": new_payload,
            },
        )
        data = response.json()
        # print(data)

        self.assertEqual(
            response.status_code,
            200,
            "Status code isn't 200",
        )

        self.assertIsInstance(
            data,
            dict,
        )
        self.assertEqual(
            data["user"]["name"],
            self.NAME,
        )
        self.assertEqual(
            data["user"]["gender"],
            self.GENDER,
        )
        self.assertEqual(
            data["payload"],
            new_payload,
        )


class TestTweetView(APITestCase):

    USERNAME = "Test User"
    NAME = "Test Name"

    DIFF_USERNAME = "Second Test User"
    DIFF_NAME = "Second Test Name"

    GENDER = "male"
    PAYLOAD = "Test Payload"
    URL = "/api/v1/tweets/"

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

        models.Tweet.objects.create(
            user=self.user,
            payload=self.PAYLOAD,
        )

    def test_tweet_not_found(self):
        response = self.client.get(self.URL + "2/")

        self.assertEqual(response.status_code, 404)

    def test_get_tweet(self):
        response = self.client.get(self.URL + "1/")

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(
            data["user"]["name"],
            self.NAME,
        )
        self.assertEqual(
            data["user"]["gender"],
            self.GENDER,
        )
        self.assertEqual(
            data["payload"],
            self.PAYLOAD,
        )

    def test_put_tweet(self):
        new_payload = "New Payload"
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
                "payload": new_payload,
            },
        )
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(
            data["payload"],
            new_payload,
        )

    def test_delete_tweet(self):
        response = self.client.delete(self.URL + "1/")
        self.assertEqual(response.status_code, 403)

        self.client.force_login(
            self.diff_user,
        )
        response = self.client.delete(self.URL + "1/")
        self.assertEqual(response.status_code, 403)

        self.client.force_login(
            self.user,
        )
        response = self.client.delete(self.URL + "1/")
        self.assertEqual(response.status_code, 204)

        response = self.client.get(self.URL + "1/")
        self.assertEqual(response.status_code, 404)
