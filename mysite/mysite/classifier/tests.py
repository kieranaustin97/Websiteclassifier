"""Django Test File"""
from unittest.mock import patch
from unittest import mock
from django.test import TestCase

import numpy

from classifier.scripts.website_classification import WebsiteClassification

## Tests for website_classification (Must)
### Only test methods written not imported such as requests library functions
class WebsiteClassificationMethods(TestCase):
    """Tests for website_classification script"""
    testWebsiteClassifier = WebsiteClassification()

    def test_clean_html_text(self):
        input_html_string = "This is the \n correctly cleaned string"
        cleaned_string = self.testWebsiteClassifier.clean_html_text(input_html_string)

        expected_clean_string = "this is the correctly cleaned string"
        self.assertEqual(cleaned_string, expected_clean_string)

    def test_class_collect_website(self):
        with patch.object(self.testWebsiteClassifier, 'collect_html', return_value="website_html"):
            test_class_name = "site_class"
            test_url = "https://www.url.com"
            classified_message_data = self.testWebsiteClassifier.class_collect_website(test_class_name,test_url)

        expected_classified_data = {'classification': 'site_class', 'message': 'website_html'}
        self.assertEqual(classified_message_data, expected_classified_data)

    def test_list_possible_classes(self):
        unique_class_values = self.testWebsiteClassifier.list_possible_classes().tolist()
        expected_classes = ['News', 'Banking', 'Cooking Recipes', 'Video Streaming', 'Shopping and Bookings', 'Gambling', 'Job Search', 'Health and lifestyle']
        self.assertEqual(unique_class_values, expected_classes)

## Tests for models (Maybe, currently no Django stored models, This may be changed when storing additional user classifications)

## Tests for views (Should)

## Tests for forms (Should)

## Tests for user experience (Maybe)
