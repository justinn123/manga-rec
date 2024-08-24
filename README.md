# Manga Recommendation System
Script that collects data on the best rated manga (> 7/10 rating) and based on my current preferences of manga, will recommend similar manga with
a decent rating.

## Technology 
The API of the manga website was not very useful as it did not provide the required data for the dataset I was looking for. 
Because of this, I had to manually scrape the data myself using BeautifulSoup. Currently the scraper gets the manga in order of the Bayesian Average rating
but I am just using the user rating average listed on the site. 
