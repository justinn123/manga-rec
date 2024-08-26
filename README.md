# Manga Recommendation System
Script that collects data on the best rated manga (> 7/10 rating) and based on my current preferences of manga, will recommend similar manga with
a decent rating.

## Technology 
The API of the manga website was not very useful as it did not provide the required data for the dataset I was looking for.
Because of this, I had to manually scrape the data myself using BeautifulSoup.

## Issues
Currently, after about 100 mangas, I am getting status code 503 meaning that I am overloading the server. This means that I will need to space out the requests of each manga making the scraping time much longer. Fortunately, the scraping should only be done occasionally as most mangas on the list do not update that often, since a lot of them have already ended.
