from django.db import models
from ckeditor.fields import RichTextField
from django.template.defaultfilters import slugify


class BaseModel(models.Model):
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class BlogModel(BaseModel):
    title = models.CharField(max_length=512)
    description = RichTextField()
    slug = models.SlugField(null=True, blank=True, unique=True, max_length=512)
    views_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class AddEbookModel(BaseModel):
    ebook_title = models.CharField(max_length=512)
    ebook_link = models.URLField()
    full_name = models.CharField(max_length=128)
    email = models.EmailField()
    checked = models.BooleanField(default=False)

    def __str__(self):
        return self.ebook_title


class CommentModel(BaseModel):
    user = models.ForeignKey('user.UserModel', on_delete=models.SET_NULL, null=True)
    ebook = models.ForeignKey('ebook.EbookModel', on_delete=models.CASCADE)
    description = models.TextField()
    rate = models.IntegerField(null=True, blank=True)
