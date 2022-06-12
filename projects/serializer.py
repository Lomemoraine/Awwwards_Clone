from rest_framework import serializers
from .models import *

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'bio', 'picture')
        
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ('project_title', 'project_image', 'project_description',  'pub_date','Author', 'author_profile','link', 'country')
