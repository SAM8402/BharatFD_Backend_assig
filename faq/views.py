from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import FAQ
from .serializers import FAQSerializer


class FAQListView(APIView):
    def get(self, request):
        lang = request.query_params.get('lang', 'en')
        cache_key = f'faqs_{lang}'
        faqs = cache.get(cache_key)

        if faqs is None:  
            faqs = FAQ.objects.all()
            if not faqs.exists():  
                cache.set(cache_key, [], timeout=60 * 2)
                return Response([])  

            serializer = FAQSerializer(faqs, many=True)
            data = []
            for faq in serializer.data:
                translated_faq = {
                    'question': faq.get(f'question_{lang}', faq['question']),
                    'answer': faq.get(f'answer_{lang}', faq['answer']),
                }
                data.append(translated_faq)
            cache.set(cache_key, data, timeout=60 * 2)  
            faqs = data

        return Response(faqs)
