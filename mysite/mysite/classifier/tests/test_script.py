"""Django Script Test File"""
from unittest.mock import patch, Mock
from django.test import TestCase

import requests

from classifier.scripts.website_classification import WebsiteClassification

class WebsiteClassificationMethods(TestCase):
    """Tests for website_classification script"""
    testWebsiteClassifier = WebsiteClassification()

    def test_collect_html(self):
        patch_responce_object = Mock(spec=requests.Response)
        type(patch_responce_object).text = '<!DOCTYPE html>\r\n<html>\r\n<body><p>Test HTML data</p></body>\r\n</html>'
        with patch.object(requests, 'get', return_value=patch_responce_object):
            test_url = "https://www.url.com"
            collected_html = self.testWebsiteClassifier.collect_html(test_url)
            
        expected_html = "<!DOCTYPE html>\r\n<html>\r\n<body><p>Test HTML data</p></body>\r\n</html>"
        self.assertEqual(collected_html, expected_html)

    def test_clean_html_text(self):
        input_html_string = "This is the \n correctly   cleaned string that tests for special characters such as * and ?"
        cleaned_string = self.testWebsiteClassifier.clean_html_text(input_html_string)

        expected_clean_string = "this is the correctly cleaned string that tests for special characters such as and"
        self.assertEqual(cleaned_string, expected_clean_string)
        
    def test_class_collect_website(self):
        with patch.object(self.testWebsiteClassifier, 'collect_html', return_value="website_html"):
            test_class_name = "site_class"
            test_url = "https://www.url.com"
            classified_message_data = self.testWebsiteClassifier.class_collect_website(test_class_name,test_url)

        expected_classified_data = {'classification': 'site_class', 'message': 'website_html'}
        self.assertEqual(classified_message_data, expected_classified_data)
        
    def test_predict_site_class(self):
        with patch.object(self.testWebsiteClassifier, 'collect_html', return_value="website_html"):
            test_url = "https://www.url.com"
            preditcted_class_data = self.testWebsiteClassifier.predict_site_class(test_url)

        self.assertIsInstance(preditcted_class_data,tuple)

    def test_list_possible_classes(self):
        unique_class_values = self.testWebsiteClassifier.list_possible_classes().tolist()
        expected_classes = ['News', 'Banking', 'Cooking and Recipes', 'Video Streaming', 'Shopping and Bookings', 'Gambling', 'Health and Lifestyle', 'Property Sales and Rentals', 'Computer Hardware', 'Programming', 'Online Communications']
        self.assertEqual(unique_class_values, expected_classes)