from bs4 import BeautifulSoup
from datetime import datetime
from utils import *
import os
import requests
import csv, json

fields = ['Title', 'Genres', 'Categories', 'Total Category Score', 'Rating']
data = []

rating = 10.0
end_loop = False

script_run = datetime.now()


URL = f"https://www.mangaupdates.com/series.html?page=1&perpage=100&orderby=rating"

while not end_loop:
    response = fetch_page(URL)

    if response.status_code == 200:
        webpage = response.text

        soup = BeautifulSoup(webpage, 'html.parser')
        mangas = soup.find_all(class_="col-12 col-lg-6 p-3 text")
        if not mangas:
            print("There was an issue retrieving data for mangas")
            break

        for manga in mangas:
            #Get rating of manga
            divs = manga.find_all(class_="text")
            rating = divs[3].find('b').get_text()
            if float(rating) < 7:
                end_loop = True
                break
            
            manga_link = manga.find(class_="col-auto align-self-center series_thumb p-0")
            manga_link = manga_link.find('a')

            if manga_link and 'href' in manga_link.attrs:
                next_url = manga_link['href']

                if not next_url.startswith('http'):
                    next_url = requests.compat.urljoin(URL, next_url)

                new_response = fetch_page(next_url)
                if not new_response:
                    continue

                if new_response.status_code == 200:
                    next_soup = BeautifulSoup(new_response.text, 'html.parser')

                    #Get title of manga
                    title = next_soup.find(class_ = "releasestitle tabletitle")
                    if title:
                        title = title.get_text()
                    else:
                        print("Could not get title of this manga")

                    #Get categories of manga
                    category_list = next_soup.find(class_="tags")
                    categories = []
                    total_score_votes = 0
                    if category_list:
                        category_list = category_list.find_all('li')
                        for item in category_list:
                            score_str = item.find(attrs={"title": True}).get('title')
                            score = score_str.split()[1]
                            categories.append({"Category": item.get_text(), "Score": score})
                            total_score_votes+=int(score)
                    else:
                        print("There was an error getting categories of this manga")

                    #Get genre of manga
                    genre = (next_soup.find(class_="col-6 p-2 text")
                    .find_next_sibling('div')
                    .find('div')
                    .find_next_sibling('div')
                    .find_next_sibling('div')
                    .find_next_sibling('div')
                    .find_all('u'))
                    genre_list = []

                    if genre:
                        for item in genre[:-1]:
                            genre_list.append(item.get_text())
                    else:
                        print("Could not get genres of this manga")

                    #Get rating of manga
                    if not rating:
                        print("Could not get rating of this manga")
                    data.append({
                        "Title": title,
                        "Genres": genre_list,
                        "Categories": categories,
                        "Total Category Score": total_score_votes,
                        "Rating": rating
                    })
            else:
                print("Could not get manga details.")
            URL = soup.find('a', string='Next Page').get('href')
    else:
        print(f"Failed to retrieve website. Status code: {response.status_code}")
    
    
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the relative path to the 'data' folder
data_folder = os.path.join(script_dir, '..', 'data')
relative_path = os.path.join(data_folder, 'manga_data.csv')


with open(relative_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(fields)
    
    for manga in data:
        title = manga["Title"]
        genres = json.dumps(manga["Genres"])
        categories = json.dumps(manga["Categories"])
        total_category_score = manga["Total Category Score"]
        rating = manga["Rating"]
        
        writer.writerow([title, genres, categories, total_category_score, rating])

script_end = datetime.now()

print(f"Time elapsed scraping: {calc_time_elapsed(script_run, script_end)}")
