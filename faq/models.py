from django.db import models
from ckeditor.fields import RichTextField
from googletrans import Translator
from django_ckeditor_5.fields import CKEditor5Field

class FAQ(models.Model):
    question = models.TextField()
    answer = CKEditor5Field('Answer', config_name='extends')
    question_hi = models.TextField(blank=True, null=True)  # Hindi translation
    question_bn = models.TextField(
        blank=True, null=True)  # Bengali translation
    answer_hi = RichTextField(blank=True, null=True)  # Hindi translation
    answer_bn = RichTextField(blank=True, null=True)  # Bengali translation

    def __str__(self):
        return self.question

    def get_translated_text(self, field, lang):
        """Retrieve translated text dynamically."""
        translation = getattr(self, f"{field}_{lang}", None)
        return translation if translation else getattr(self, field)

    def save(self, *args, **kwargs):
        """Automate translations during object creation."""
        translator = Translator()
        if not self.question_hi:
            self.question_hi = translator.translate(
                self.question, dest='hi').text
        if not self.question_bn:
            self.question_bn = translator.translate(
                self.question, dest='bn').text
        if not self.answer_hi:
            self.answer_hi = translator.translate(self.answer, dest='hi').text
        if not self.answer_bn:
            self.answer_bn = translator.translate(self.answer, dest='bn').text
        super().save(*args, **kwargs)
