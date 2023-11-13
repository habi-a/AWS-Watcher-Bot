import requests
from bs4 import BeautifulSoup


AMAZON_BASE_URL="https://www.amazon.fr"

def search(search_query, search_results):
    message=""
    base_url = AMAZON_BASE_URL + "/s"
    headers = {"User-Agent": "Mozilla 5.0"}
    params = {"k": search_query}

    page = requests.get(base_url, headers=headers, params=params)

    # if page.status_code == 301:
    #     page = requests.get(page.url, headers=headers, params=params)
    #     if page.status_code != 200:
    #         return "Not found after redirect " + str(page.status_code)
    if page.status_code != 200 or page.status_code != 301:
        return "Not found " + str(page.status_code)
    
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find_all(lambda tag: tag.name == "div" and tag.get("data-asin", '') != "" and not "AdHolder" in tag.get("class", ""))[:8]

    for i, result in enumerate(results, 1):
        number = i - 4
        title = result.find("span", {"class": "a-text-normal"})
        price = result.find("span", {"class": "a-offscreen"})
        link = result.find('a', {"class": "a-link-normal"}, href=True)

        if title and price and link:
            search_results.append({"title": title.text.strip(), "price": price.text.strip(), "link": AMAZON_BASE_URL + link['href']})
            message += f"{number}. {title.text.strip()} - {price.text.strip()}\n"
    return message


def get_price(url):
    headers = {'User-Agent': 'Mozilla 5.0'}
    page = requests.get(url, headers=headers)

    # if page.status_code == 301:
    #     page = requests.get(page.url, headers=headers)
    #     if page.status_code != 200:
    #         return "Not found after redirect " + str(page.status_code)
    if page.status_code != 200 or page.status_code != 301:
        return "Not found " + str(page.status_code)

    soup = BeautifulSoup(page.content, "html.parser")
    price_int = soup.find(class_="a-price-whole")
    price_dec = soup.find(class_="a-price-fraction")

    if price_int is None or price_dec is None:
        return "Price not found " + str(page.status_code)
    return price_int.get_text() + price_dec.get_text() + '€'
