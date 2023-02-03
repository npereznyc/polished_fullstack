from django.shortcuts import render, redirect
from django.views import View, generic
from django.http import HttpResponse 
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from .models import Brand, Polish, Review
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
import os
import uuid
import boto3



# Create your views here.
class Signup(View):
    def get(self, request):
        form = UserCreationForm()
        context = {'form': form}
        return render(request, 'registration/signup.html', context)
    
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            context = {'form': form}
            return render(request, 'registration/signup.html', context)

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

class BrandDetail(DetailView):
    model = Brand
    template_name = 'brand_detail.html'


class PolishList(TemplateView):
    template_name = 'polish_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['polishes'] = Polish.objects.all()
        return context

class PolishReviews(DetailView):
    model = Polish
    template_name='polish_reviews.html'

class ReviewList(TemplateView):
    template_name = 'review_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.all()
        return context

class UserReviews(LoginRequiredMixin,generic.ListView):
    model = Review
    template_name = 'user_reviews.html'

    def get_queryset(self):
        user_reviews=Review.objects.filter(user=self.request.user)
        print('user reviews: ', user_reviews)
        return Review.objects.filter(user=self.request.user)
        


@method_decorator(login_required, name='dispatch')
class CreateReview(CreateView):
    model = Review
    fields = ['polish', 'brand', 'review']
    template_name = "create_review.html"
    success_url = "/reviews/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateReview, self).form_valid(form)

    def get_success_url(self):
        print(self.kwargs)
        return reverse('review_detail', kwargs={'pk': self.object.pk})

@method_decorator(login_required, name='dispatch')
class UpdateReview(UpdateView):
    model = Review
    fields = ['user', 'polish', 'brand', 'image', 'review']
    template_name = "update_review.html"
    success_url = "/reviews/"

    def get_success_url(self):
        return reverse('review_detail', kwargs={'pk': self.object.pk})


class ReviewDetail(DetailView):
    model = Review
    template_name='review_detail.html'


@method_decorator(login_required, name='dispatch')
class DeleteReview(DeleteView):
    model = Review
    template_name='delete_review_conf.html'
    success_url = "/"

def add_photo(request):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['AWS_STORAGE_BUCKET_NAME']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            image = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            Review.objects.create(url=url, image=image)
        except:
            print('An error occurred uploading file to S3')
    # return redirect('my_reviews')
