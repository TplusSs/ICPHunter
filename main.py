import requests
from bs4 import BeautifulSoup
import click
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import uuid
from urllib.parse import urlparse
import pandas as pd


def get_uuid():
    return str(uuid.uuid4())


def get_root_domain(input_url):
    if not input_url.startswith(('http://', 'https://')):
        input_url = f'http://{input_url}'
    parsed_url = urlparse(input_url)
    host = parsed_url.netloc
    parts = host.split('.')
    if len(parts) >= 2:
        return f'{parts[-2]}.{parts[-1]}'
    return host


def contains_chinese(s):
    for ch in s:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


def build_url_xpath(input):
    if not contains_chinese(input):
        index = get_root_domain(input)
    else:
        index = input
    return f"https://www.beianx.cn/search/{index}"


def fetch_data(url):
    uuid_value = get_uuid()
    cookie_str = f"machine_str={uuid_value}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "Cookie": cookie_str
    }
    try:
        response = requests.get(url, headers=headers)
        print(f"Request URL: {url}, Status Code: {response.status_code}")
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None


def handle_data_xpath(data, output_filename):
    soup = BeautifulSoup(data, 'html.parser')
    tr_elements = soup.select('table tr')[1:]  # 排除表头行
    results = []
    for tr in tr_elements:
        tds = tr.find_all('td')
        if len(tds) >= 7:
            unit = tds[1].text.strip()
            type_ = tds[2].text.strip()
            icp_code = tds[3].text.strip()
            domain = tds[5].text.strip()
            pass_time = tds[6].text.strip()
            results.append([unit, type_, icp_code, domain, pass_time])
        else:
            print("[Error] IPC filing query failed! Skipping!")

    if results:
        df = pd.DataFrame(results, columns=['主办单位名称', '主办单位性质', '网站备案号', '网站首页地址', '审核日期'])
        df.to_excel(f'{output_filename}.xlsx', index=False)
        print(f"结果已保存到 {output_filename}.xlsx")


def fetch_and_handle_data_xpath(url, output_filename):
    data = fetch_data(url)
    if data:
        handle_data_xpath(data, output_filename)


def process_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        urls = [build_url_xpath(line.strip()) for line in lines]
        unique_urls = list(set(urls))

        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = []
            for url in unique_urls:
                input_name = url.split('/')[-1]
                futures.append(executor.submit(fetch_and_handle_data_xpath, url, input_name))
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Error: {e}")
        print("Data processing completed.")
    except Exception as e:
        print(f"Error: {e}")


@click.command()
@click.option('-d', '--domain', help='Domain name Or Company name Or URL to lookup')
@click.option('-f', '--file', help='A file containing the domain or business name or url to be found')
def main(domain, file):
    if domain:
        url = build_url_xpath(domain)
        fetch_and_handle_data_xpath(url, domain)
        print("Data processing completed.")
    elif file:
        process_file(file)
    else:
        print("Invalid option.")


if __name__ == "__main__":
    main()