from django.shortcuts import render
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
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin





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
    fields = ['user', 'polish', 'brand', 'image', 'review']
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