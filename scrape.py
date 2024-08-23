from bs4 import BeautifulSoup
import requests

URL = "https://www.mangaupdates.com/series.html?orderby=rating&perpage=100"

response = requests.get(URL)

if response.status_code == 200:
    webpage = response.text

    soup = BeautifulSoup(webpage, 'html.parser')
    mangas = soup.find_all(class_="col-12 col-lg-6 p-3 text")
    count = 0

    for manga in mangas:
        if count == 10:
            break
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
                print(f"Title: {title.get_text()}")

                #Get categories of manga
                category_list = next_soup.find(class_="tags")
                category_list = category_list.find_all('li')
                print(f"Categories:")
                for item in category_list:
                    print(f"\t{item.get_text()}")

                #Get genre of manga
                genre = next_soup.find(class_ = "col-6 p-2 text")
                genre = genre.find_next_sibling('div')
                genre = genre.find('div')
                genre = genre.find_next_sibling('div').find_next_sibling('div').find_next_sibling('div')
                genre = genre.find_all('u')
                print(f"Genres:")
                for item in genre[:-1]:
                    print(f"\t{item.get_text()}")

                #Get rating of manga
                rating = next_soup.find('div', string='User Rating')
                rating = rating.find_next_sibling('div')
                first_line = rating.get_text().splitlines()[0]
                rating = first_line.split()[1]
                print(f"Rating: {rating}")


            else:
                print(f"Failed to retrieve the page. Status code: {new_response.status_code}")
        else:
            print("No link found on the page.")
        count += 1
else:
    print(f"Failed to retrieve website. Status code: {response.status_code}")







