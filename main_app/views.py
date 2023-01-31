from django.shortcuts import render
from django.views import View
from django.http import HttpResponse 
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from .models import Brand, Polish, Review



# Create your views here.
# class Home(TemplateView):
#     template_name = "home.html"

class About(TemplateView):
    template_name = 'about.html'


class BrandList(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get('name')
        if name != None:
            context['brands'] = Brand.objects.filter(name__icontains=name)
            context['header'] = f'Searching for {name}'
        else:
            context['brands'] = Brand.objects.all()
            context['header'] = 'Popular Brands'
        return context

class PolishList(TemplateView):
    template_name = 'polish_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['polishes'] = Polish.objects.all()
        return context

# class PolishReviewsList(TemplateView):
#     template_name='polish_review.html'

class ReviewList(TemplateView):
    template_name = 'review_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.all()
        return context

class CreateReview(CreateView):
    model = Review
    fields = ['user', 'polish', 'brand', 'image', 'review']
    template_name = "create_review.html"
    success_url = "/reviews/"
