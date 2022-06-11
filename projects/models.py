from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.http import Http404
from django.db.models import ObjectDoesNotExist
from django_countries.fields import CountryField


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,)
    bio = models.CharField(default="My bio", max_length = 40)
    picture = CloudinaryField('images', default='http://res.cloudinary.com/dim8pysls/image/upload/v1639001486/x3mgnqmbi73lten4ewzv.png')
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
class Projects(models.Model):
    project_title = models.CharField(max_length=255)
    project_image = CloudinaryField('images', default='')
    project_description = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    Author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    author_profile = models.ForeignKey(Profile,on_delete=models.CASCADE, blank=True, default='1')
    country = CountryField(blank_label='(select country)', default='KE')
    link = models.URLField()
    
    def save_project(self):
        self.save()
    
    def delete_project(self):
        self.delete()
        
    @classmethod
    def get_projects(cls):
        projects = cls.objects.all()
        return projects
    
    @classmethod
    def search_projects(cls, search_term):
        projects = cls.objects.filter(project_title__icontains=search_term)
        return projects
    
    
    @classmethod
    def get_by_author(cls, Author):
        projects = cls.objects.filter(Author=Author)
        return projects
    
    
    @classmethod
    def get_project(request, id):
        try:
            project = Projects.objects.get(pk = id)
            
        except ObjectDoesNotExist:
            raise Http404()
        
        return project
    
    def __str__(self):
        return self.project_title
    
    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'My Project'
        verbose_name_plural = 'Projects'
    