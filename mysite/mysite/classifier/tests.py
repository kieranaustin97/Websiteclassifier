"""Django Test File"""
from unittest.mock import patch
from unittest import mock
from django.test import TestCase

#Change to import one at a time, in order of test usage
#from classifier.scripts.website_classification import (clean_html_text, class_collect_website)

from classifier.scripts import website_classification
# Create your tests here.

## Tests for website_classification (Must)
### Only test methods written not imported such as requests library functions
class WebsiteClassificationMethods(TestCase):
    """Tests for website_classification script"""
    testWebsiteClassifierObject = website_classification
   
    def test_clean_html_text(self):
        input_html_string = "This is the \n correctly cleaned string"
        cleaned_string = self.testWebsiteClassifierObject.clean_html_text(input_html_string)

        expected_clean_string = "this is the correctly cleaned string"
        self.assertEqual(cleaned_string, expected_clean_string)

    @mock.patch('classifier.scripts.website_classification.collect_html', return_value="website_html")
    def test_class_collect_website(self):
        test_class_name = "site_class"
        test_url = "https://www.url.com"

        classified_message_data = self.testWebsiteClassifierObject.class_collect_website(test_class_name, test_url)

        expected_classified_data = {'classification': 'site_class', 'message': 'website_html'}
        self.assertEqual(classified_message_data, expected_classified_data)
       
## Tests for models (Maybe, currently no Django stored models, This may be changed when storing additional user classifications)

## Tests for views (Should)

## Tests for forms (Should)

## Tests for user experience (Maybe)
