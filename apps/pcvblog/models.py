from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.db import models

from taggit.managers import TaggableManager

from apps.worldmap import data_options
from apps.pcvcore.models import PCVProfile

class Entry(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to="blog-images", null=True, blank=True)
    slug = models.SlugField(db_index=True, blank=True)
    body = models.TextField()
    post_time = models.DateTimeField(auto_now_add=True)
    grade_level = models.CharField(choices=data_options.GRADES, max_length=128, blank=True, null=True, default="")
    tags = TaggableManager(blank=True)

    @property
    def permalink(self):
        return reverse("blog_permalink",
            args=[self.author.username, self.pk, self.slug])

    @property
    def abstract(self):
        return self.body[:30] + "..."

    def save(self, *args, **kwargs):
        ## TODO: Should slug be unique? If so we need db constraint
        #        and a check here or in ``clean``
        self.slug = slugify(self.title)
        super(Entry, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('entry_list')

    def __unicode__(self):
        return "%s - %s" % (self.title, self.author)

    def as_dict(self):
        return {
            'author': self.author.pcvprofile,
            'title': self.title,
            'image': self.image.url if self.image else None,
            'slug': self.slug,
            'body': self.body,
            'post_time': self.post_time,
            'grade_level': self.grade_level,
            'tags': self.tags.all(),
            'permalink': self.permalink,
        }
