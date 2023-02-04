from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Brand(models.Model):

    name = models.CharField(max_length=100)
        
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Polish(models.Model):
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=400, default="https://www.dictionary.com/e/wp-content/uploads/2018/02/nail-polish-light-skin-tone.png")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='polishes')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['brand', 'name']

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='reviews')
    polish = models.ForeignKey(Polish, on_delete=models.PROTECT, related_name='reviews')
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='reviews')
    review =  models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.review

    class Meta:
        ordering = ['-created_at']

class Photo(models.Model):
    url = models.CharField(max_length=200)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for review_id: {self.review_id} @{self.url}"