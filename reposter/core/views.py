from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.core.files.images import ImageFile
from django.views.generic import TemplateView, ListView, DetailView
from core import models
from django.core.files.uploadedfile import InMemoryUploadedFile
from core.services import source_data, qr_service, reposters


class CreateSourceView(TemplateView):
    template_name = 'core/create_source.html'

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = source_data.get_source_data(request)

        if data.get('source_data', None):
            source = models.Source.objects.create(**data.get('source_data'))
            images = data.get('images', [])

            for index, image in enumerate(images):
                if index == 0:
                    qr_image = qr_service.create_qrcode_image(image, data['source_data']['url'])
                    source.image_set.create(
                        image=InMemoryUploadedFile(qr_image, None, 'test.jpg', 'image/jpeg', qr_image.tell, None)
                    )

                source.image_set.create(image=ImageFile(image, name='image.jpeg'))

            return JsonResponse({
                'success': True,
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Something wrong'
            })


class SourceListView(ListView):
    template_name = 'core/source_list.html'
    model = models.Source


class SourceDetailView(DetailView):
    template_name = 'core/source_detail.html'
    model = models.Source

    def post(self, request, *args, **kwargs):
        repost_to = request.META.get('QUERY_STRING').replace('repost_to=', '')
        if repost_to == 'instagram':
            if reposters.instagram_repost(self.get_object()):
                obj = self.get_object()
                obj.instagram_published = True
                obj.save()

        return HttpResponseRedirect(request.path)
