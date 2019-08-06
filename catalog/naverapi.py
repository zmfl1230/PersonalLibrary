import urllib.request
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
import json, re

client_id = "H8CYXmu1xY1dwFjo50eB"
client_secret = "VfUlR4urMh"


def search_api(req):
    key = req.GET.get('key', None)
    print(req)
    encText = urllib.parse.quote(key)
    url = "https://openapi.naver.com/v1/search/book?query=" + encText + "&display=3&sort=count"  # json 결과
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if (rescode == 200):
        response_body = response.read().decode('utf-8')
        search_result = json.loads(response_body)
        # print(search_result)
        books = search_result['items']  # item 의 값을 가져와서 books의 담았고 이는 가져온 book들의 전체 리스트를 나타낸다.
        print(type(books))  # 그래서 이 books의 타입은 list로 가져올 수 있다.[list]
        search_book = []
        for book in books:  # list 값인 books들을 for(반복문)으로 돌리면 이는 dict의 형태로 추출이 되고
            # print('title: {}'.format(book['title']))  # 그래서 이를 dict으로 print하면 원하는 형태가 나온다.
            #
            # print('author: {}'.format(book['author']))
            #
            # print('pubdate: {}'.format(book['pubdate']))
            #
            # print('-------------------------')
            print(book)
            remove_m = re.sub('<[^>]*>', '', book['title'])
            book['title'] = remove_m
            remove_m = re.sub('<[^>]*>', '', book['author'])
            book['author'] = remove_m
            print(book)
            search_book.append(book)
            print(search_book)

        return JsonResponse({'html': render_to_string('catalog/components/_search_naver_book.html',
                                                      {'contacts': search_book})})

    else:
        print("Error Code:" + rescode)
