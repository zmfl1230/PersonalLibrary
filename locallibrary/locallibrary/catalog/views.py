from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import generic
from django.utils import timezone
from .models import Book, Author, BookInstance, Genre, Language, Already_read
from django.db.models import Q
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.core.files.storage import FileSystemStorage
from .forms import *

# ctrl + alt + L


class TemplateView(generic.TemplateView):
    model = Book
    template_name = "catalog/about.html"


def search_base(request):
    value = request.GET.get('search_value', '')
    # print(value, "몇번째?")

    if value:
        book_all = Book.objects.filter(
            Q(bookname__contains=value) | Q(author__first_name__contains=value) | Q(
                author__last_name__contains=value))
        book_paginator = Paginator(book_all, 5)

        book_page = request.GET.get('page', 1)
        # print(type(book_page)) str

        try:
            contacts = book_paginator.page(book_page)

        except PageNotAnInteger:
            contacts = book_paginator.page(1)

        except EmptyPage:
            contacts = book_paginator.page(book_paginator.num_pages)

        return JsonResponse({
            'html': render_to_string('catalog/components/_book_list.html',
                                     {'book_all': book_all, 'contacts': contacts, 'value': value}),

        })
    book_all = Book.objects.all()
    return render(request, 'catalog/base_generic.html', {'book_all': book_all})


def autocomplete_tags(request):
    if request.is_ajax():
        queryset = Book.objects.filter(bookname__startswith=request.GET.get('search', ''))
        dict = {}
        for i in queryset:
            dict[i.bookname] = ''

        return JsonResponse(dict)


def index(request):  # views.index의 요청이오면.

    num_books = Book.objects.all().count()
    num_novel = Genre.objects.filter(name='소설').count()
    # genre = Genre.objects.all()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_novel': num_novel,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'catalog/index.html', context=context)


def book_list(request):
    book_all = Book.objects.all()
    num_book_available = BookInstance.objects.filter(status='a').count()

    value = request.GET.get('search_value', '')
    # print(type(book_page)) str
    print(value)
    if value:
        print(value)
        book_all = Book.objects.filter(
            Q(bookname__contains=value) | Q(author__first_name__contains=value) | Q(
                author__last_name__contains=value))
    print(book_all)
    book_paginator = Paginator(book_all, 5)

    book_page = request.GET.get('page', 1)
    try:
        contacts = book_paginator.page(book_page)

    except PageNotAnInteger:
        contacts = book_paginator.page(1)

    except EmptyPage:
        contacts = book_paginator.page(book_paginator.num_pages)

    return render(request, 'catalog/book_list.html',
                  {'book_all': book_all, 'num_book_available': num_book_available, 'contacts': contacts,
                   'value': value})


class Bookdetail(generic.DetailView):
    model = Book
    template_name = 'catalog/book_detail.html'
    context_object_name = 'book'


class Authorlist(generic.ListView):
    template_name = 'catalog/author_list.html'
    context_object_name = 'author_list'

    def get_queryset(self):
        return Author.objects.order_by('last_name')


def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    books_of_author = Book.objects.filter(author=author)
    author_num = str(author.id)

    return render(request, 'catalog/author_detail.html', {
        'author': author,
        'books_of_author': books_of_author,
        'author_num': author_num
    })


def read(request):
    # read = Book.objects.get(pk = pk)
    # #add the data
    # readbook = Already_read( book = read, read_or_not = True , due_date =timezone.now())
    # readbook.save()
    #
    # book_list = Already_read.objects.all()
    # books = Book.objects.all()
    #
    # # print (book_list.filter(book = read).count())
    #
    # return render(request, 'catalog/readList.html',{'book_list':book_list ,'books':books})
    #
    pk = request.POST.get('pk', None)  # ajax 통신을 통해서 template에서 POST방식으로 전달//
    read_book = Book.objects.get(pk=pk)

    book_already_read, book_already_read_created = read_book.already_read_set.get_or_create(book=read_book,
                                                                                            read_or_not=True,
                                                                                            due_date=timezone.now())

    if not book_already_read_created:
        book_already_read.delete()

    message = book_already_read_created

    context = {"message": message}

    return JsonResponse(context)


class Readlist(generic.ListView):
    model = Book
    template_name = 'catalog/readList.html'
    context_object_name = 'book_list'

    def get_queryset(self):
        return Already_read.objects.order_by('due_date')


def add_book(request):
    authors = Author.objects.all()
    languages = Language.objects.all()
    genres = Genre.objects.all()

    if request.method == "POST":
        bookname = request.POST['bookname']
        author_id = request.POST['author_id']
        author = Author.objects.get(id=author_id)
        summary = request.POST['summary']
        genre_id = request.POST['genre']
        genre = Genre.objects.get(id=genre_id)
        wrote_language_id = request.POST['wrote_language']
        wrote_language = Language.objects.get(id=wrote_language_id)

        book = Book.objects.create(bookname=bookname, author=author, summary=summary,
                                   wrote_language=wrote_language)
        book.save()
        book.genre.add(genre)

        context = dict()
        context['url'] = reverse('add_book')
        context['success'] = True
        return JsonResponse(context)
    else:
        return render(request, 'catalog/add_book.html', {'authors': authors, 'languages': languages, 'genres': genres})


def add_author(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        author = Author.objects.create(first_name=first_name, last_name=last_name)

        author.save()

        context = dict()
        context['url'] = reverse('add_book')
        context['success'] = True
        return JsonResponse(context)


def add_author_detail(request):
    # print("111")
    # if request.method == 'POST':
    #     # and request.POST['myfile']:
    #     print("222")
    #     print(request.POST['myfile'])
    #     print(request.FILES)
    #     myfile = request.FILES['myfile']
    #     print(myfile)
    #     fs = FileSystemStorage()
    #     filename = fs.save(myfile.name, myfile)
    #     uploaded_file_url = fs.url(filename)
    #     return render(request, 'catalog/add_author_detail.html', {
    #         'uploaded_file_url': uploaded_file_url
    #     })
    if request.method == 'POST':
        form = AuthorimageForm(request.POST, request.FILES)
        print(request.FILES)

        if form.is_valid():
            form.save()
            return JsonResponse({'error': False, 'message': 'Uploaded Successfully'})
        else:
            return JsonResponse({'error': True, 'errors': form.errors})
    else:
        form = AuthorimageForm()
        return render(request, 'catalog/add_author_detail.html', {'form': form})

    # return render(request, 'catalog/add_author_detail.html', {})


def add_language(request):
    if request.method == "POST":
        l_type = request.POST['L_type']

        language = Language.objects.create(L_type=l_type)
        language.save()

        context = dict()
        context['success'] = True
        return JsonResponse(context)
