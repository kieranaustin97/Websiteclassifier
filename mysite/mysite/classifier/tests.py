from django.test import TestCase, mock
from unittest.mock import patch

#Change to import one at a time, in order of test usage

from classifier.scripts import website_classification
# Create your tests here.

## Tests for website_classification (Must)
### Only test methods written not imported such as requests library functions
class WebsiteClassificationMethods(TestCase):

    testWebsiteClassifierObject = website_classification.WebsiteClassifier()
 
    def test_clean_html_text(self):
        input_html_string = "This is the \n correctly cleaned string"
        cleaned_string = self.testWebsiteClassifierObject.clean_html_text(input_html_string)

        expected_clean_string = "this is the correctly cleaned string"
        self.assertEqual(cleaned_string, expected_clean_string)

    #@mock.patch('classifier.scripts.website_classification.clean_html_text', return_value="output_string")
    #def test_class_collect_website(self, mock_clean_html):
   #        
  #      test_class_name = "test_site"
 #       test_url = "url"
#
 #       classifed_message_data = self.testWebsiteClassifierObject.class_collect_website(test_class_name,test_url)
#
    #    expected_classified_data = "fred"
    #    self.assertEqual(classifed_message_data, expected_classified_data)

    


## Tests for models (Maybe, currently no Django stored models, This may be changed when storing additional user classifications)

## Tests for views (Should)

## Tests for forms (Should)

## Tests for user experience (Maybe)