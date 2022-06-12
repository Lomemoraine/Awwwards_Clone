from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import *
import datetime as dt
from django.contrib.auth.decorators import login_required
from .models import *
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def home(request):
    date = dt.date.today()
    projects = Projects.get_projects()
    
    return render(request,'index.html',{"date": date, "projects":projects})



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})
@login_required
def profile(request, username):
    current_user = request.user
    Author = current_user
    projects = Projects.get_by_author(Author)
    #  if request.method == 'POST':
    #     u_form = UserUpdateForm(request.POST, instance=request.user)
    #     p_form = ProfileUpdateForm(request.POST,
    #                                request.FILES,
    #                                instance=request.user.profile)
    #     if u_form.is_valid() and p_form.is_valid():
    #         u_form.save()
    #         p_form.save()
    #         messages.success(request, f'Your account has been updated!')
    #         return redirect('profile')

    # else:
    #     u_form = UserUpdateForm(instance=request.user)
    #     p_form = ProfileUpdateForm(instance=request.user.profile)

    # context = {
    #     'u_form': u_form,
    #     'p_form': p_form
    # }
    
    return render(request, 'profile.html',{"projects":projects})
@login_required
def editProfile(request,username):
    user = User.objects.get(username=username)
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'You have succesfully updated your profile')
            return redirect('profile',username=username)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context={
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request, 'edit_profile.html', context)
@login_required
def new_project(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.Author = current_user
            project.save()
        return redirect('home')

    else:
        form = NewProjectForm()
    return render(request, 'new_project.html', {"form": form})

# def post(request):
#     if request.method == 'POST':
#         form = UploadForm(request.POST,request.FILES)
#         print(form.errors)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.user = request.user.profile
#             post.save()
#             return redirect('landing')
#     else:
#         form = UploadForm()
#     return render(request,'post_image.html', {"form":form})

def get_project(request, id):

    try:
        project = Projects.objects.get(pk = id)
        ratings = Rating.objects.filter(user=request.user, project=id).first()
        rating_status = None
        form = RatingsForm()
        if ratings is None:
            rating_status = False
        else:
            rating_status = True
        if request.method == 'POST':
            form = RatingsForm(request.POST)
            if form.is_valid():
                rate = form.save(commit=False)
                rate.user = request.user
                rate.project = project
                rate.save()
                project_ratings = Rating.objects.filter(project=project)
                
                design_ratings = [d.design for d in project_ratings]
                design_average = sum(design_ratings) / len(design_ratings)
                
                usability_ratings = [us.usability for us in project_ratings]
                usability_average = sum(usability_ratings) / len(usability_ratings)
                
                content_ratings = [content.content for content in project_ratings]
                content_average = sum(content_ratings) / len(content_ratings)
                
                score = (design_average + usability_average + content_average) / 3
                print(score)
                rate.design_average = round(design_average, 2)
                rate.usability_average = round(usability_average, 2)
                rate.content_average = round(content_average, 2)
                rate.score = round(score, 2)
                rate.save()
                return HttpResponseRedirect(request.path_info)
            else:
                form = RatingsForm()
                
                
                
        
        
    except ObjectDoesNotExist:
        raise Http404()
    
    
    return render(request, "project.html", {"project":project,"rating_form": form,"rating_status": rating_status})

#  post = Post.objects.get(title=post)
#     ratings = Rating.objects.filter(user=request.user, post=post).first()
#     rating_status = None
#     if ratings is None:
#         rating_status = False
#     else:
#         rating_status = True
#     if request.method == 'POST':
#         form = RatingsForm(request.POST)
#         if form.is_valid():
#             rate = form.save(commit=False)
#             rate.user = request.user
#             rate.post = post
#             rate.save()
#             post_ratings = Rating.objects.filter(post=post)

#             design_ratings = [d.design for d in post_ratings]
#             design_average = sum(design_ratings) / len(design_ratings)

#             usability_ratings = [us.usability for us in post_ratings]
#             usability_average = sum(usability_ratings) / len(usability_ratings)

#             content_ratings = [content.content for content in post_ratings]
#             content_average = sum(content_ratings) / len(content_ratings)

#             score = (design_average + usability_average + content_average) / 3
#             print(score)
#             rate.design_average = round(design_average, 2)
#             rate.usability_average = round(usability_average, 2)
#             rate.content_average = round(content_average, 2)
#             rate.score = round(score, 2)
#             rate.save()
#             return HttpResponseRedirect(request.path_info)
#     else:
#         form = RatingsForm()
#     params = {
#         'post': post,
#         'ra'rating_status': rating_statusting_form': form,
#         'rating_status': rating_status

#     }
#     return render(request, 'project.html', params)

def search_projects(request):
    if 'keyword' in request.GET and request.GET["keyword"]:
        search_term = request.GET.get("keyword")
        searched_projects = Projects.search_projects(search_term)
        message = f"{search_term}"

        return render(request, 'search.html', {"message":message,"projects": searched_projects})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html', {"message": message})