from django.shortcuts import render, redirect, get_object_or_404
from django.views import View, generic
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from .models import Brand, Polish, Review, Photo
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.views import PasswordResetView
# from django.contrib.auth.views import PasswordResetConfirmView
# from django.contrib.auth.views import PasswordChangeView
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
import os
import uuid
import boto3


# Create your views here.
# class Signup(View):
#     def get(self, request):
#         form = UserCreationForm()
#         context = {'form': form}
#         return render(request, 'registration/signup.html', context)
    
#     def post(self, request):
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('home')
#         else:
#             context = {'form': form}
#             return render(request, 'registration/signup.html', context)


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
        print('context: ', context)
        name  = self.request.GET.get('name')
        if name != None:
            context['polishes'] = Polish.objects.filter(name__icontains=name)
            context['header'] = f'Searching for {name}'
        else:
            context['polishes'] = Polish.objects.all()
            context['header'] = 'Popular Polishes'
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
        return Review.objects.filter(user=self.request.user)
        

@method_decorator(login_required, name='dispatch')
class CreateReview(CreateView):
    model = Review
    fields = ['polish', 'brand', 'review']
    template_name = "create_review.html"

    def get_form(self, form_class=None):
       form = super().get_form(form_class)
       form.helper = FormHelper()
       form.helper.add_input(Submit('submit', 'Create', css_class='btn-primary'))
       return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateReview, self).form_valid(form)

    def get_success_url(self):
        print(self.kwargs)
        return reverse('add_swatch', kwargs={'pk': self.object.pk})


@method_decorator(login_required, name='dispatch')
class UpdateReview(UpdateView):
    model = Review
    fields = ['review']
    template_name = "update_review.html"
    success_url = "/myreviews/"

    def get_form(self, form_class=None):
       form = super().get_form(form_class)
       form.helper = FormHelper()
       form.helper.add_input(Submit('submit', 'Create', css_class='btn-primary'))
       return form

    def get_success_url(self):
        return reverse('review_detail', kwargs={'pk': self.object.pk})


class ReviewDetail(DetailView):
    model = Review
    template_name='review_detail.html'


class AddSwatch(DetailView):
    model = Review
    template_name='add_photo.html'


@method_decorator(login_required, name='dispatch')
class DeleteReview(DeleteView):
    model = Review
    template_name='delete_review_conf.html'
    success_url = "/myreviews/"


def add_photo(request, review_id):
    photo_file = request.FILES.get('photo-file', None)
    print('photo file: ', photo_file)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            bucket = os.environ['AWS_STORAGE_BUCKET_NAME']
            s3.upload_fileobj(photo_file, bucket, key)
            # building the full url string:
            url = f"{os.environ['BASE_URL']}/{key}"
            Photo.objects.create(url=url, review_id=review_id)
        except:
            print('An error occurred uploading file to S3')
    return redirect('my_reviews')


@ login_required
def add_favorite(request, id):
    polish = get_object_or_404(Polish, id=id)
    if polish.favorites.filter(id=request.user.id).exists():
        polish.favorites.remove(request.user.pk)
    else:
        polish.favorites.add(request.user.pk)
    return redirect('favorites_list')


@login_required
def favorites_list(request):
    favorite=Polish.objects.filter(favorites=request.user.pk)
    return render(request, 'user_favorites.html', {'favorite' : favorite})

# class MyPasswordResetView(PasswordResetView):
#     template_name = 'accounts/password_reset_form.html'
#     email_template_name = 'password_reset_email.html'
#     subject_template_name = 'password_reset_subject.txt'
#     success_url = reverse_lazy('password_reset_done')
