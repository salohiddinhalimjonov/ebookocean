from django.template.defaultfilters import slugify
from django.db import models
from src.common.models import BaseModel
from src.user.models import UserModel
from django.conf import settings
from src.common.services import compress_image


class CategoryModel(BaseModel):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.title


class EbookModel(BaseModel):
    title = models.CharField(max_length=128)
    authors = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    publisher = models.CharField(max_length=128, null=True, blank=True)
    views_count = models.PositiveIntegerField(default=0)
    downloads_count = models.PositiveIntegerField(default=0)
    published_year = models.DateField(null=True, blank=True)
    price = models.DecimalField(max_digits=21, decimal_places=2, null=True, blank=True)
    is_free = models.BooleanField(default=False)
    cover_image = models.ImageField(upload_to='images/ebook/Ebook/')
    file = models.FileField(upload_to='files/ebook/Ebook/')
    pages = models.PositiveIntegerField(default=0)
    slug = models.SlugField(null=True, blank=True, unique=True)
    category = models.ManyToManyField(CategoryModel, related_name='ebooks')


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        media = self.cover_image
        if media:
            if media.size > settings.IMAGE_SIZE_TO_COMPRESS:
                self.media = compress_image(media)
        if self.is_free is True:
            self.price = 0
        super(EbookModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class EbookFavouritesModel(BaseModel):
    ebook = models.ForeignKey(EbookModel, related_name='favourites', on_delete=models.CASCADE)
    favourite = models.ForeignKey(UserModel, related_name='ebooks', on_delete=models.CASCADE)
