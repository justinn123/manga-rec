from bs4 import BeautifulSoup
import requests

rating = 10.0
curr_page = 1

while True:
    URL = f"https://www.mangaupdates.com/series.html?page={curr_page}&orderby=rating&perpage=5"

    response = requests.get(URL)

    if response.status_code == 200:
        webpage = response.text

        soup = BeautifulSoup(webpage, 'html.parser')
        mangas = soup.find_all(class_="col-12 col-lg-6 p-3 text")
        if not mangas:
            print("There was an issue retrieving data for mangas")
            exit(0)

        count = 0

        for manga in mangas:
            
            divs = manga.find_all(class_="text")
            rating = divs[3].find('b').get_text()
            if not rating or float(rating) < 8.8:
                exit()
            
            
            manga_link = manga.find(class_="col-auto align-self-center series_thumb p-0")
            manga_link = manga_link.find('a')

            if manga_link and 'href' in manga_link.attrs:
                next_url = manga_link['href']

                if not next_url.startswith('http'):
                    next_url = requests.compat.urljoin(URL, next_url)

                new_response = requests.get(next_url)

                if new_response.status_code == 200:
                    next_soup = BeautifulSoup(new_response.text, 'html.parser')

                    #Get title of manga
                    title = next_soup.find(class_ = "releasestitle tabletitle")
                    if title:
                        print(f"Title: {title.get_text()}")
                    else:
                        print("Could not get title of this manga")

                    #Get categories of manga
                    category_list = next_soup.find(class_="tags")
                    print(f"Categories:")
                    if category_list:
                        category_list = category_list.find_all('li')
                        for item in category_list:
                            print(f"\t{item.get_text()}")
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

                    if genre:
                        print(f"Genres:")
                        for item in genre[:-1]:
                            print(f"\t{item.get_text()}")
                    else:
                        print("Could not get genres of this manga")

                    #Get rating of manga
                    print(f"Rating: {rating}")
                else:
                    print(f"Failed to retrieve the page. Status code: {new_response.status_code}")
            else:
                print("No link found on the page.")
            count += 1
    else:
        print(f"Failed to retrieve website. Status code: {response.status_code}")
    curr_page += 1







