# Fetch the webpage
url = 'https://wildcat.arizona.edu/category/opinions/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

def fetch_articles(url):
    # Send a GET request to the webpage
    response = requests.get(url)
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Initialize lists to store the extracted information
    titles = []
    authors = []
    dates = []
    abstracts = []
    columns = []
    urls = []
    
    # Extract the information
    for article in soup.select('.catlist-tile-inner'):
        title_tag = article.select_one('h2 a.homeheadline')
        title = title_tag.get_text(strip=True) if title_tag else 'N/A'
        url = title_tag['href'] if title_tag else 'N/A'
        
        author_tag = article.select_one('.catlist-writer a')
        author = author_tag.get_text(strip=True) if author_tag else 'N/A'
        
        date_tag = article.select_one('.catlist-date .time-wrapper')
        date = date_tag.get_text(strip=True) if date_tag else 'N/A'
        
        abstract_tag = article.select_one('.catlist-tile-textarea-with-media p')
        abstract = abstract_tag.get_text(strip=True) if abstract_tag else 'N/A'
        
        # Assuming "column" is the category of the article, using title tag text for now
        column = 'Opinion'
        
        titles.append(title)
        authors.append(author)
        dates.append(date)
        abstracts.append(abstract)
        columns.append(column)
        urls.append(url)
    
    return titles, authors, dates, abstracts, columns, urls

# Initialize the lists to store the data from all pages
all_titles = []
all_authors = []
all_dates = []
all_abstracts = []
all_columns = []
all_urls = []

# Base URL for pagination
base_url = 'https://wildcat.arizona.edu/category/opinions/page/'

# Number of articles per page (Assuming it's 10, adjust as needed)
articles_per_page = 10

# Number of pages needed to get 500 articles
total_pages = 500 // articles_per_page

for page in range(1, total_pages + 1):
    url = base_url + str(page) + '/'
    titles, authors, dates, abstracts, columns, urls = fetch_articles(url)
    all_titles.extend(titles)
    all_authors.extend(authors)
    all_dates.extend(dates)
    all_abstracts.extend(abstracts)
    all_columns.extend(columns)
    all_urls.extend(urls)

# Create a DataFrame
df = pd.DataFrame({
    'title': all_titles,
    'author': all_authors,
    'date': all_dates,
    'abstract': all_abstracts,
    'column': all_columns,
    'url': all_urls
})

# Display the DataFrame
print(df)

# Save to CSV if needed
df.to_csv('wildcat.csv', index=False)
