from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import EbookModel, CategoryModel
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Import mimetypes module
from django.http import FileResponse
import mimetypes
# import os module
import os
# Import HttpResponse module
from django.http.response import HttpResponse


def home(request):
    context = cache.get('context')
    if not context:
        context = {}
        results = []
        ebooks = EbookModel.objects.all()
        if ebooks.count() > 5:
            popular_ebooks = ebooks.order_by('views_count')[:5]
            context['popular_ebooks'] = popular_ebooks.values('title', 'slug', 'cover_image')

        categories = CategoryModel.objects.filter(parent=None)[:5]
        for category in categories:
            result = category.ebooks.all()
            if result.count() >= 5:
                results.append({category: [result[:5].values('title', 'slug', 'cover_image')]})
            else:
                pass
        context['results'] = results
        cache.set('context', context, timeout=60*60*24)
    return render(request, 'home.html', context)


def filter_ebook_view(request):
    ebooks = None
    context = {'ebooks': ebooks}
    is_popular = request.GET.get('is_popular')
    if is_popular == 'True':
        ebooks = EbookModel.objects.all()
        ebooks = ebooks.order_by('views_count')[:12]
    browse = request.GET.get('browse')
    if browse:
        new_ones = CategoryModel.objects.filter(title__icontains=browse)
        if new_ones:
            first_one = new_ones.first()
            ebooks = first_one.ebooks.all()
    categories = CategoryModel.objects.all()
    context['results'] = categories
    search = request.GET.get('search')
    if search:
        ebooks = EbookModel.objects.filter(Q(title__icontains=search) | Q(authors__icontains=search))
    categories = request.GET.getlist('categories')
    if categories:
        ebooks = EbookModel.objects.filter(category__id__in=categories).order_by('title').distinct('title')
    if ebooks:
        page_number = request.GET.get('page', 1)
        paginator = Paginator(ebooks, 12)
        try:
            ebooks = paginator.page(page_number)
        except PageNotAnInteger:
            ebooks = paginator.page(1)
        except EmptyPage:
            ebooks = paginator.page(paginator.num_pages)
        context['ebooks'] = ebooks
    return render(request, 'ebook.html', context)


class EbookDetailView(View):

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        print(slug)
        try:
            ebook = EbookModel.objects.get(slug=slug)
        except EbookModel.DoesNotExist:
            return redirect('home')
        return render(request, 'ebook_detail.html', {'ebook': ebook})

@login_required
def read_pdf(request):
    pdf_path = request.GET.get('pdf_path')
    if pdf_path:
        return render(request, 'read_online.html', {'pdf_path': pdf_path})
    else:
        redirect('home')

@login_required
def download_file(request):
    pdf_path = request.GET.get('pdf_path')
    if pdf_path:
        return FileResponse(open(pdf_path, 'rb'), as_attachment=True)
