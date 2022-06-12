from django.test import TestCase
from .models import *

# Create your tests here.
class ProfileTest(TestCase):
    def setUp(self):
        self.user = User(id=1, username='raine', password='gift1234')
        self.user.save()
        
    def test_instance(self):
        self.assertTrue(isinstance(self.user, User))

    def test_save_user(self):
        self.user.save()

    def test_delete_user(self):
        self.user.delete()
        
class ProjectsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create( username='raine',password='gift1234')
        self.project = Projects.objects.create(id=1, project_title='test post', project_image='https://ucarecdn.com/0ccf61ff-508e-46c6-b713-db51daa6626e', project_description='desc',
                                        Author=self.user, link='http://ur.coml')
        
    def test_instance(self):
        self.assertTrue(isinstance(self.project, Projects))
        
    def test_save_project(self):
        self.project.save_project()
        project = Projects.objects.all()
        self.assertTrue(len(project) > 0)

    def test_get_projects(self):
        self.project.save_project()
        projects = Projects.all_posts()
        self.assertTrue(len(projects) > 0)

    def test_search_project(self):
        self.project.save_project()
        project = Projects.search_project('test')
        self.assertTrue(len(project) > 0)

    def test_delete_project(self):
        self.project.delete_post()
        project = Projects.search_project('test')
        self.assertTrue(len(project) < 1)
