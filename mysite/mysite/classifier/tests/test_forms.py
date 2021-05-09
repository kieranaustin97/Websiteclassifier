"""Django Form Test File"""
from django.test import TestCase
from classifier.forms import URLForm

class TestForms(TestCase):
    """Tests for URLForm"""
    def test_url_form_data(self):
        """Testing form is valid when supplied real data"""
        test_form = URLForm(data={
            'url': 'testurl'
        })

        self.assertTrue(test_form.is_valid())

    def test_url_form_no_data(self):
        """Testing form is not valid when supplied no data"""
        test_form = URLForm(data={})

        self.assertFalse(test_form.is_valid())
        self.assertEqual(len(test_form.errors),1)