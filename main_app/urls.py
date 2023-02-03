from django.urls import path
from . import views

# this like app.use() in express
urlpatterns = [
    path('', views.BrandList.as_view(), name='home'),
    path('about/', views.About.as_view(), name='about'),
    path('brands/<int:pk>/', views.BrandDetail.as_view(), name='brand_detail'),
    path('polishes/', views.PolishList.as_view(), name='polish_list'),
    path('polishes/<int:pk>/', views.PolishReviews.as_view(), name="polish_reviews"),
    path('reviews/', views.ReviewList.as_view(), name='review_list'),
    path('reviews/new/', views.CreateReview.as_view(), name='create_review'),
    path('reviews/<int:pk>/', views.ReviewDetail.as_view(), name='review_detail'),
    path('reviews/<int:pk>/update/', views.UpdateReview.as_view(), name='update_review'),
    path('reviews/<int:pk>/delete/', views.DeleteReview.as_view(), name='delete_review'),
    path('accounts/signup/', views.Signup.as_view(), name="signup"),
    path('myreviews/', views.UserReviews.as_view(), name='my_reviews'),

    # path('reviews/add_photo', views.add_photo, name='add_photo'),
    path('reviews/add_photo', views.CreateReview.as_view(), name='add_photo'),
]