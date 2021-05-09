"""Django URLs Test File"""
from django.test import TestCase
from django.urls import reverse, resolve
from classifier.views import index, showresults

class TestUrls(TestCase):
    """Tests for URLs"""
    def test_index_url_resovles(self):
        url = reverse('index')
        self.assertEqual(resolve(url).func, index)

    def test_showresults_url_resolves(self):
        url = reverse('showresults')
        self.assertEqual(resolve(url).func, showresults)
