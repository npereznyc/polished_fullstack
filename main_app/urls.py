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
    path('reviews/<int:review_id>/add_photo/', views.add_photo, name='add_photo'),
    path('reviews/<int:pk>/', views.AddSwatch.as_view(), name='add_swatch'),
    path('reviews/<int:pk>/swatch', views.ReviewDetail.as_view(), name='review_detail'),
    path('reviews/<int:pk>/update/', views.UpdateReview.as_view(), name='update_review'),
    path('reviews/<int:pk>/delete/', views.DeleteReview.as_view(), name='delete_review'),
    path('myreviews/', views.UserReviews.as_view(), name='my_reviews'),

    # path('accounts/signup/', views.Signup.as_view(), name="signup"),
    
    path('favorites/<int:id>/', views.add_favorite, name='add_favorite'),
    path('myfavorites/', views.favorites_list, name='favorites_list'),
]