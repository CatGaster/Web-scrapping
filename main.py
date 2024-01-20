import json
import requests
import fake_headers
from bs4 import BeautifulSoup


def scraping():
    keywords = ["Python, Flask, Django"]
    url = "https://spb.hh.ru/search/vacancy?text=Python%2C+Flask+Django&salary=&ored_clusters=true&area=1&area=2&hhtmFrom=vacancy_search_list&hhtmFromLabel=vacancy_search_line"
    headers_gen = fake_headers.Headers(browser = "chrome", os = "win")
    response = requests.get(url, headers = headers_gen.generate())

    if response.status_code == 200:
        main_html = response.text
        main_soup = BeautifulSoup(main_html, "lxml")
        main_aplication_tag = main_soup.find_all("main", class_="vacancy-serp-content")
        aplication_tags = main_soup.find_all("div", class_="serp-item")
        result = []

        for aplication_tag in aplication_tags:
            link = aplication_tag.find("a", class_ = "bloko-link")["href"]
            title = aplication_tag.find("h3", class_= "bloko-header-section-3").text
            company = aplication_tag.find("a", class_ = "bloko-link bloko-link_kind-tertiary").text
            city = aplication_tag.find("div", {"data-qa": "vacancy-serp__vacancy-address"}).text
        
            salary = aplication_tag.find("span", {"data-qa": "vacancy-serp__vacancy-compensation"})
            if salary:
                salary = salary.text.strip()
            else:
                 salary = "Зарплата не указана"
        
            result.append({
                "title": title,
                "company": company,
                "city": city,
                "salary": salary,
                "link": link
            })
    return result

if __name__ == "__main__":
    result = scraping()
    print(result)

    with open("result.json", "w", encoding = "utf-8") as file:
        json.dump(result, file, indent = 4, ensure_ascii = False)


