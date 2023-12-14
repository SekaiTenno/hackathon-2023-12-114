import requests
from bs4  import BeautifulSoup as bs
import csv
import time
import schedule

def write_to_csv(data):
    with open('data.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow([data['title'], data['price'], data['img']])
        

def get_html(url):
    response = requests.get(url)
    print(response.status_code)
    return response.text


def get_data(html):
    soup = bs(html, 'lxml')
    product_list = soup.find_all('div', class_='row')
    # print(product_list)
    for product in product_list:
        title = product.find('div', class_='rows').find('a').text
        
        price = product.find('span', class_='price').text
        # print(price)

        img = product.find('a', class_='product-image-link').find('img').get('src')
        img = 'https://enter.kg' + img 
        # print(img)

        data = {
            'title': title,
            'price': price,
            'img': img
        }
        write_to_csv(data)

def get_last_page(html):
    soup = bs(html, 'lxml')
    last_page = soup.find('li', class_='pagination-end').find('a').get('href')
    last_page = last_page.split('-')[-1]

    return int(last_page)


def main():
    url = 'https://enter.kg/computers/noutbuki_bishkek'
    html = get_html(url)
    get_data(html)

    total_pages = get_last_page(html)
    for i in range(100, total_pages + 1, 100):
        page_url = url + '/results,' + str(i + 1) + str(i)
        html = get_html(page_url)
        get_data(html)


with open('data.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(['title      ', 'price     ', 'image     '])

main()




# import requests
# from bs4 import BeautifulSoup as bs
# import csv
# import schedule
# import time

# def write_to_csv(data):
#     with open('data.csv', 'a') as file:
#         writer = csv.writer(file)
#         writer.writerow([data['title'], data['price'], data['img']])

# def get_html(url):
#     response = requests.get(url)
#     print(response.status_code)
#     return response.text

# def get_data(html):
#     soup = bs(html, 'lxml')
#     product_list = soup.find_all('div', class_='row')
    
#     for product in product_list:
#         title = product.find('div', class_='rows').find('a').text
#         price = product.find('span', class_='price').text
#         img = product.find('a', class_='product-image-link').find('img').get('src')
#         img = 'https://enter.kg' + img 

#         data = {
#             'title': title,
#             'price': price,
#             'img': img
#         }
#         write_to_csv(data)

# def get_last_page(html):
#     soup = bs(html, 'lxml')
#     last_page = soup.find('li', class_='pagination-end').find('a').get('href')
#     last_page = last_page.split('-')[-1]

#     return int(last_page)

# def job():
#     print("Running the job...")
#     url = 'https://enter.kg/computers/noutbuki_bishkek'
#     html = get_html(url)
#     get_data(html)

#     total_pages = get_last_page(html)
#     for i in range(100, total_pages + 1, 100):
#         page_url = url + '/results,' + str(i + 1) + str(i)
#         html = get_html(page_url)
#         get_data(html)

# # Определение задачи по расписанию
# schedule.every(5).minutes.do(job)

# # Запуск бесконечного цикла для выполнения задач по расписанию
# while True:
#     schedule.run_pending()
#     time.sleep(1)
