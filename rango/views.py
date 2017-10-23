from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm
from django.views.decorators.csrf import ensure_csrf_cookie, requires_csrf_token


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, "authorname": "Swati Goyal", "pages": page_list}
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


@ensure_csrf_cookie
@requires_csrf_token
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

    return render_to_response('rango/add_category.html', {'form': form,}, RequestContext(request))


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
