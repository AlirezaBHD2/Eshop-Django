# Import the necessary module from Django
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm, EditUserForm
from django.contrib.auth import login, get_user_model, authenticate, logout
from django.contrib.auth.models import User


# Define the views
def login_user(request):
    # Redirect to home page if user is already authenticated
    if request.user.is_authenticated:
        return redirect('/')

    # Create login form object
    login_form = LoginForm(request.POST or None)
    if login_form.is_valid():
        # Authenticate user with entered credentials
        user_name = login_form.cleaned_data.get('user_name')
        password = login_form.cleaned_data.get('password')
        user = authenticate(request, username=user_name, password=password)
        # If user is authenticated, log them in and redirect to home page
        if user is not None:
            login(request, user)
            return redirect('/')
        # If user is not authenticated, add error message to login form
        else:
            login_form.add_error('user_name', 'کاربری با مشخصات وارد شده یافت نشد')

    context = {
        'login_form': login_form
    }
    # Render the login page with the login form
    return render(request, 'account/login.html', context)


def register(request):
    # Redirect to home page if user is already authenticated
    if request.user.is_authenticated:
        return redirect('/')
    # Create register form object
    register_form = RegisterForm(request.POST or None)
    if register_form.is_valid():
        # Create new user with entered credentials and redirect to login page
        user_name = register_form.cleaned_data.get('user_name')
        password = register_form.cleaned_data.get('password')
        email = register_form.cleaned_data.get('email')
        User.objects.create_user(username=user_name, email=email, password=password)
        return redirect('/login')

    context = {
        'register_form': register_form
    }
    # Render the register page with the register form
    return render(request, 'account/register.html', context)


def log_out(request):
    # Log the user out and redirect to login page
    logout(request)
    return redirect("/login")


@login_required(login_url='/login')
def user_account_main_page(request):
    # Get the username and email of the logged-in user and render the user account main page with that info
    username = request.user.username
    email = request.user.email
    context = {"username": username, "email": email}
    return render(request, "account/user_account_main.html", context)


# This decorator requires the user to be logged in before accessing the view.
# If not logged in, the user will be redirected to the login page specified in the argument.
@login_required(login_url='/login')
def edit_user_profile(request):
    # Get the ID of the current user from the request.
    user_id = request.user.id
    # Get the user object with the retrieved ID.
    user = User.objects.get(id=user_id)

    # If the user object does not exist, raise a 404 error.
    if user is None:
        raise Http404("کاربر یافت نشد")

    # Create an instance of the EditUserForm with initial data from the retrieved user.
    edit_user_form = EditUserForm(request.POST or None,
                                  initial={'first_name': user.first_name, 'last_name': user.last_name})

    # If the form is valid, update the user's first and last names and save the changes.
    if edit_user_form.is_valid():
        first_name = edit_user_form.cleaned_data.get("first_name")
        last_name = edit_user_form.cleaned_data.get("last_name")
        user.first_name = first_name
        user.last_name = last_name
        user.save()

    # Create a context dictionary to pass the form to the template.
    context = {'edit_user_form': edit_user_form}

    # Render the template with the form and context data.
    return render(request, "account/edit-profile.html", context)


# This view renders a user sidebar template with no context data.
def user_sidebar(request):
    return render(request, "account/user-sidebar.html", {})
