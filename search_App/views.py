from operator import pos
from typing import final
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
# from requests.compat import quote_plus
from .models import Search


BASE_CRAIGLIST_URL = 'https://losangeles.craigslist.org/search/?query={}'

# Create your views here.
def home(request):
    return render(request, 'index.html')

def new_search(request):
    search = request.POST.get('search')
    Search.objects.create(search=search)
    
    response = requests.get(BASE_CRAIGLIST_URL.format(search))
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    post_listings = soup.find_all('li', class_='result-row')
    post_listings = soup.find_all('li', class_='result-row')

    final_postings = []
    for post in post_listings:

        post_title = post.find(class_='result-title').text
        post_link = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'Unknown'    

        BASE_IMG_URL = 'https://images.craigslist.org/{}_600x450.jpg'

        if  post.find(class_='result-image').get('data-ids'):
            post_img_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_img_url = BASE_IMG_URL.format(post_img_id)

        else:
            post_img_url = 'https://yt3.ggpht.com/ytc/AAUvwngR70SiNXkKcYMaGbtp2wC7BFyikeMPJBNCVHkQWg=s176-c-k-c0x00ffffff-no-rj'

        final_postings.append((post_title, post_link, post_price, post_img_url))
   
    stuff_for_frontend = {
        'search':search,
        'final_postings' :  final_postings,
        }

    return render(request, 'new_search.html', stuff_for_frontend)    
