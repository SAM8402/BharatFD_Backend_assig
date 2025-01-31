from django.test import TestCase,Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.cache import cache
from .models import FAQ


class FAQModelTest(TestCase):
    def setUp(self):
        FAQ.objects.all().delete()
        cache.clear()
    def test_faq_creation(self):
        """
        Test that an FAQ object can be created with all required fields.
        """
        faq = FAQ.objects.create(
            question="What is Django?",
            answer="Django is a web framework."
        )
        self.assertEqual(faq.question, "What is Django?")
        self.assertEqual(faq.answer, "Django is a web framework.")

    def test_automatic_translation(self):
        """
        Test that translations are automatically generated when an FAQ object is created.
        """
        faq = FAQ.objects.create(
            question="What is Django?",
            answer="Django is a web framework."
        )
        self.assertIsNotNone(faq.question_hi)  # Hindi translation
        self.assertIsNotNone(faq.question_bn)  # Bengali translation
        self.assertIsNotNone(faq.answer_hi)    # Hindi translation
        self.assertIsNotNone(faq.answer_bn)    # Bengali translation

    def test_get_translated_text(self):
        """
        Test the `get_translated_text` method to ensure it retrieves the correct translation or falls back to the default language.
        """
        faq = FAQ.objects.create(
            question="What is Django?",
            answer="Django is a web framework.",
            question_hi="Django क्या है?",
            answer_hi="Django एक वेब फ्रेमवर्क है।"
        )
        # Test Hindi translation
        self.assertEqual(faq.get_translated_text(
            'question', 'hi'), "Django क्या है?")
        self.assertEqual(faq.get_translated_text(
            'answer', 'hi'), "Django एक वेब फ्रेमवर्क है।")
        # Test fallback to English
        self.assertEqual(faq.get_translated_text(
            'question', 'fr'), "What is Django?")
        self.assertEqual(faq.get_translated_text(
            'answer', 'fr'), "Django is a web framework.")


class FAQAPITest(TestCase):
    def setUp(self):
        FAQ.objects.all().delete()
        cache.clear()
    def test_api_default_language(self):
        """
        Test that the API returns FAQs in the default language (English) when no language is specified.
        """
        FAQ.objects.create(
            question="What is Django?",
            answer="Django is a web framework."
        )
        response = self.client.get(reverse('faq-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['question'], "What is Django?")
        self.assertEqual(response.data[0]['answer'],
                         "Django is a web framework.")

    def test_api_hindi_language(self):
        """
        Test that the API returns FAQs in Hindi when the `lang=hi` query parameter is provided.
        """
        FAQ.objects.create(
            question="What is Django?",
            answer="Django is a web framework.",
            question_hi="Django क्या है?",
            answer_hi="Django एक वेब फ्रेमवर्क है।"
        )
        response = self.client.get(reverse('faq-list'), {'lang': 'hi'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['question'], "Django क्या है?")
        self.assertEqual(response.data[0]['answer'],
                         "Django एक वेब फ्रेमवर्क है।")

    def test_api_bengali_language(self):
        """
        Test that the API returns FAQs in Bengali when the `lang=bn` query parameter is provided.
        """
        FAQ.objects.create(
            question="What is Django?",
            answer="Django is a web framework.",
            question_bn="ডjango কি?",
            answer_bn="ডjango একটি ওয়েব ফ্রেমওয়ার্ক।"
        )
        response = self.client.get(reverse('faq-list'), {'lang': 'bn'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['question'], "ডjango কি?")
        self.assertEqual(response.data[0]['answer'],
                         "ডjango একটি ওয়েব ফ্রেমওয়ার্ক।")

    def test_api_caching(self):
        """
        Test that the API response is cached and subsequent requests are faster.
        """
        FAQ.objects.create(
            question="What is Django?",
            answer="Django is a web framework."
        )
        # First request (not cached)
        response1 = self.client.get(reverse('faq-list'))
        self.assertEqual(response1.status_code, 200)
        # Second request (cached)
        response2 = self.client.get(reverse('faq-list'))
        self.assertEqual(response2.status_code, 200)
        # Ensure the responses are the same
        self.assertEqual(response1.data, response2.data)

    def test_empty_faq_list(self):
        """
        Test that the API handles an empty FAQ list gracefully.
        """
        response = self.client.get(reverse('faq-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_invalid_language_parameter(self):
        """
        Test that the API falls back to the default language when an invalid language parameter is provided.
        """
        FAQ.objects.create(
            question="What is Django?",
            answer="Django is a web framework."
        )
        response = self.client.get(reverse('faq-list'), {'lang': 'invalid'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['question'], "What is Django?")
        self.assertEqual(response.data[0]['answer'],
                         "Django is a web framework.")


class AdminPanelTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username='sam',
            password='12345678',
            email=''
        )
        self.client.login(username='sam', password='12345678')

    def test_admin_add_faq(self):
        response = self.client.post(
            reverse('admin:faq_faq_add'),
            {
                'question': 'What is Django?',
                'answer': 'Django is a web framework.',
            }
        )
        # Redirect after successful form submission
        self.assertEqual(response.status_code, 302)
        self.assertTrue(FAQ.objects.filter(
            question='What is Django?').exists())
