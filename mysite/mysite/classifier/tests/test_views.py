"""Django Views Test File"""
from django.test import TestCase, Client
from django.urls import reverse
from classifier.models import PredictedWebsites
#from classifier.view import index, showresults

import datetime

class TestViews(TestCase):
    """Tests for Views"""
    def test_index_GET(self):
        client = Client()

        responce = client.get(reverse('index'))

        self.assertEqual(responce.status_code,200)
        self.assertTemplateUsed(responce, 'classifier/home.html')

    def test_index_POST(self):
        client = Client()

        responce = client.post(reverse('index'),{
            'url':'https://www.google.com'
        })

        self.assertEqual(responce.status_code,200)
        self.assertTemplateUsed(responce, 'classifier/output.html')
        self.assertEqual(PredictedWebsites.objects.count(), 1)
        

    def test_showresults_empty_GET(self):
        client = Client()

        responce = client.get(reverse('showresults'))

        self.assertEqual(responce.status_code,200)
        self.assertTemplateUsed(responce, 'classifier/noResults.html')
        self.assertEqual(PredictedWebsites.objects.count(), 0)

    def test_showresults_GET(self):
        client = Client()
        PredictedWebsites.objects.create(
            url="https://www.test.com",
            classification="test_classification",
            datestamp=datetime.datetime.now()
        )

        responce = client.get(reverse('showresults'))

        self.assertEqual(responce.status_code,200)
        self.assertTemplateUsed(responce, 'classifier/results.html')

    def test_showresults_DELETE(self):
        client = Client()
        PredictedWebsites.objects.create(
            url="https://www.test.com",
            classification="test_classification",
            datestamp=datetime.datetime.now()
        )

        responce = client.post(reverse('showresults'), {
            'id': 1
        })

        self.assertEqual(responce.status_code,200)
        self.assertTemplateUsed(responce, 'classifier/noResults.html')
        self.assertEqual(PredictedWebsites.objects.count(), 0)
        