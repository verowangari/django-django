from django.shortcuts import render,redirect, get_object_or_404
from .forms import SignupForm,UserUpdateForm, ProfileUpdateForm,NewPostForm,NeighbourHoodForm,BusinessForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Post,NeighbourHood,Business
# Create your views here.
# @login_required(login_url='login')
def index(request):
    post_items = Post.objects.all()
    return render(request, 'index.html', {"post_items": post_items})
def login(request):
  return render(request, 'login.html')

def Signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
   
            
			User.objects.create_user(username=username, email=email, password=password)
			return redirect('index')
        
	else:
		form = SignupForm()
	
	context = {
		'form':form,
	}

	return render(request, 'signup.html', context)

def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile) 
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile') # Redirect back to profile page

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profile.html', context)
def NewPost(request):
    current_user=request.user
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post=form.save(commit=False)
            new_post.profile=current_user
            new_post.save()
            print('post saved')
            return redirect(index)
    else:
        form = NewPostForm()
    return render(request, 'newpost.html',{'form':form})

def CreateHood(request):
    if request.method == 'POST':
        form = NeighbourHoodForm(request.POST, request.FILES)
        if form.is_valid():
            hood = form.save(commit=False)
            hood.admin = request.user.profile
            hood.save()
            return redirect('allhoods')
    else:
        form = NeighbourHoodForm()
    return render(request, 'newhood.html', {'form': form})

def hoods(request):
    all_hoods = NeighbourHood.objects.all()
    all_hoods = all_hoods[::-1]
    context = {
        'all_hoods': all_hoods,
    }
    return render(request, 'allhoods.html', context)

def join_hood(request, id):
    neighbourhood = get_object_or_404(NeighbourHood, id=id)
    request.user.profile.neighbourhood = neighbourhood
    request.user.profile.save()
    return redirect('allhoods')


def leave_hood(request, id):
    hood = get_object_or_404(NeighbourHood, id=id)
    request.user.profile.neighbourhood = None
    request.user.profile.save()
    return redirect('allhoods')

def SingleHood(request, hood_id):
    hood = NeighbourHood.objects.get(id=hood_id)
    business = Business.objects.filter(neighbourhood=hood)
    posts = Post.objects.filter(hood=hood)
    posts = posts[::-1]
    if request.method == 'POST':
        form = BusinessForm(request.POST)
        if form.is_valid():
            b_form = form.save(commit=False)
            b_form.neighbourhood = hood
            b_form.user = request.user.profile
            b_form.save()
            return redirect('single-hood', hood.id)
    else:
        form = BusinessForm()
    params = {
        'hood': hood,
        'business': business,
        'form': form,
        'posts': posts
    }
    return render(request, 'singlehood.html', params)

# def SingleHood(request):
    
#     return render(request, 'singlehood.html')