from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from . import views

# 우리의 페이지들을 위해 필요한 URL들은:

# catalog/ — 홈/색인(index) 페이지.
# catalog/books/ — 모든 책들의 목록.
# catalog/authors/ — 모든 저자들의 목록.
# catalog/book/<id> — <id> 라는 이름의(기본값) 프라이머리 키(primary key) 필드를 가지는 특정한 책을 위한 세부 사항 뷰(detail view). 예를 들어, 목록에 추가된 세 번째 책은 /catalog/book/3이 될 것입니다. 
# catalog/author/<id> —  <id> 라는 이름의 프라이머리 키(primary key) 필드를 가지는 특정한 저자를 위한 세부 사항 뷰(detail view). 예를 들어, 목록에 추가된 11번째 저자는 /catalog/author/11이 될 것입니다.
# 처음 세 개의 URL들은 인덱스 페이지, 책 목록, 그리고 저자 목록을 반환합니다. 이것들은 아무런 추가적인 정보도 인코드하지 않고, 데이터베이스에서 데이터를 가져오는 쿼리들도 항상 똑같습니다. 그러나, 쿼리들이 반환할 결과들은 데이터베이스의 내용물에 따라 다를 것입니다.

# 그에 반해서 마지막 두 개의 URL들은 특정한 책 또는 저자에 대한 세부 정보를 나타낼 것입니다.
#  이 URL들은 표시할 항목의 ID를 인코딩합니다(위에서 <id> 로 표시). URL 매퍼는 인코딩된 정보를 추출하여 view로 전달합니다.
#  그리고 view는 데이터베이스에서 무슨 정보를 가져올지 동적으로 결정합니다. 
#  URL의 정보를 인코딩하여 우리는 모든 책들(또는 저자들)을 처리하기 위해 단일 모임의 url 매핑, 뷰, 탬플릿을 사용할 것입니다. 

urlpatterns = [
                  path('', views.index, name='index'),  # name =특정한 URL 매핑을 위한 고유 ID
                  # path('list/', views.listing, name='page_list'),
                  path('books/', views.book_list, name='book_list'),
                  path('authors/', views.Authorlist.as_view(), name='author_list'),
                  path('authors/add_detail', views.add_author_detail, name='add_author_detail'),
                  path('book/<int:pk>/', views.Bookdetail.as_view(), name='book_detail'),
                  path('readlist/', views.Readlist.as_view(), name='readlist'),
                  path('author/<int:pk>/', views.author_detail, name='author_detail'),
                  path('books/read/', views.read, name='read'),
                  path('books/add_book/', views.add_book, name='add_book'),
                  path('books/add_author/', views.add_author, name='add_author'),
                  path('books/add_language/', views.add_language, name='add_language'),
                  path('search/', views.search_base, name='search_base'),
                  path('auto/', views.autocomplete_tags, name='autocomplete_tags'),
                  # path('books/read/<int:pk>/', views.read, name='read'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
