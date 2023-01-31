from django.urls import path
from . import views

# this like app.use() in express
urlpatterns = [
    path('', views.BrandList.as_view(), name='home'),
    path('about/', views.About.as_view(), name='about'),
    # path('brands/', views.BrandList.as_view(), name="brand_list"),
    path('polishes/', views.PolishList.as_view(), name='polish_list'),
    # path('polishes/<int:pk>/', views.PolishReviewsList.as_view(), name="artist_detail")
    path('reviews/', views.ReviewList.as_view(), name='review_list'),
    path('reviews/new/', views.CreateReview.as_view(), name='create_review'),
    path('reviews/<int:pk>/', views.ReviewDetail.as_view(), name='review_detail'),
    path('reviews/<int:pk>/update', views.UpdateReview.as_view(), name='update_review'),
    
]