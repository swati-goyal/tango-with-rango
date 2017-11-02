from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext
# from django.views.decorators.csrf import ensure_csrf_cookie, requires_csrf_token
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from rango.models import Category, Page


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, "authorname": "Swati Goyal", "pages": page_list, 'user': request.user}
    for category in category_list:
        category.url = category.name.replace(' ', '_')
    return render_to_response('rango/index.html', context_dict, RequestContext(request, {}))


def about(request):
    context = RequestContext(request)
    context_dict = {'boldaboutmessage': "This is about page!"}
    return render_to_response('rango/about.html', context_dict, context)


def category(request, category_name_url):
    context = RequestContext(request)
    category_name = category_name_url.replace('_', ' ')
    context_dict = {'category_name': category_name, 'category_name_url': category_name_url}
    try:
        category = Category.objects.get(name=category_name)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass

    return render_to_response('rango/category.html', context_dict, context)


# @ensure_csrf_cookie
# @requires_csrf_token
def add_category(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        # Have we been provided with a valid form?
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    else:
        form = CategoryForm()

    return render_to_response('rango/add_category.html', {'form': form, }, RequestContext(request))


def add_page(request, category_name_url):
    context = RequestContext(request)
    category_name = category_name_url.replace('_', ' ')
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            cat = Category.objects.get(name=category_name)
            page.category = cat
            page.views = 0
            page.save()
            return category(request, category_name_url)
        else:
            print(form.errors)
    else:
        form = PageForm()

    return render_to_response('rango/add_page.html', {'category_name_url': category_name_url,
                                                      'category_name': category_name, 'form': form}, context)


def register(request):
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True

        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render_to_response('rango/register.html', {'user_form': user_form, 'profile_form': profile_form,
                                                      'registered': registered}, context)


def user_login(request):
    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                # context.update(request)
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse('Invalid username or password enter, please go back and login with correct credentials.')
    else:
        return render_to_response('rango/login.html', {}, context)


@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect('/rango/')
