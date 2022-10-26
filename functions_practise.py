from bs4 import BeautifulSoup
import requests,json,pprint

def get_quotes_data():
    quotes_data=[]
    page = 1
    while page != 11:
        url = f"http://quotes.toscrape.com/page/{page}/"
        url_to_be_sent_for_quotes = url
        r = requests.get(url_to_be_sent_for_quotes)
        soup = BeautifulSoup(r.content, 'html.parser')
        page += 1
        list_of_authors =[
        {
            'quote': str(quote.find('span', {'class': 'text'}).text).replace("“","").replace('”', '').replace('’', "'").replace("′ -"," ").replace("′",""),
            'author': str(quote.find("small", {'class': "author"}).text).replace('é','e'),
            'tags': [
                tag.text
                for tag in quote.find_all('a', {'class': 'tag'})
            ]
        }
        for quote in soup.find_all('div', {'class': 'quote'})
    ]
        quotes_data.extend(list_of_authors)
    return quotes_data
def get_authors_data():
    authors_names = []
    authors_unique_list = []
    authors_data = []
    url2 = 'http://quotes.toscrape.com/'
    r = requests.get(url2)
    soup = BeautifulSoup(r.content, 'html.parser')
    temp_dict = soup.select(".col-md-8 .quote")
    for j in temp_dict:
        element2 = j
        authors_names.append(element2.select_one(".author").text)
    for i in authors_names:
        if i not in authors_unique_list:
            authors_unique_list.append(i)
    for author in authors_unique_list:
        value = str(author)
        if author == "J.K. Rowling":
            author = "J-K-Rowling"
        elif (author == "Thomas A. Edison"):
            author = "Thomas-A-Edison"
        else:
            char_to_replace = {'.': '-',
                               " ": '-',
                               'é': 'e'}
        for key, value in char_to_replace.items():
            author = author.replace(key, value)
            temp = author
            url2 = f"http://quotes.toscrape.com/author/{author}/"
            url_to_be_sent_for_author = url2
            r = requests.get(url_to_be_sent_for_author)
            soup = BeautifulSoup(r.content, 'html.parser')
        list_of_authors = [
            {
                'name': str(author).replace('é', 'e'),
                'born': str(autho.find("span", {'class': "author-born-date"}).text) + " " + str(
                    autho.find("span", {'class': "author-born-location"}).text),
                'reference': url2
            }
            for autho in soup.find_all('div', {'class': 'author-details'})
        ]
        authors_data.extend(list_of_authors)
    return authors_data
quotes=get_quotes_data()
authors=get_authors_data()
d={}
d["quotes"]=quotes
d["authors"]=authors
with open("optimized_first_assignment.json", "w") as outfile:
    json.dump(d, outfile,indent=4)





