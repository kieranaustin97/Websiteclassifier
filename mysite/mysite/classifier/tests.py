from django.test import TestCase

#Change to import one at a time, in order of test usage
from classifier.scripts.website_classification import (clean_html_text)


# Create your tests here.

## Tests for website_classification (Must)
### Only test methods written not imported such as requests library functions
class WebsiteClassificationMethods(TestCase):
    def test_clean_html_text(self):
        expected_clean_string = "this is the correctly cleaned string"
        input_html_string = "This is the \n correctly cleaned string"
        cleaned_string = clean_html_text(input_html_string)

        self.assertEqual(cleaned_string, expected_clean_string)


## Tests for models (Maybe, currently no Django stored models, This may be changed when storing additional user classifications)

## Tests for views (Should)

## Tests for forms (Should)

## Tests for user experience (Maybe)