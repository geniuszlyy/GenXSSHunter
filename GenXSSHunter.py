from colorama import init, Fore, Style
from bs4 import BeautifulSoup
import aiohttp
import asyncio
from urllib.parse import urljoin
from pprint import pprint
import os
import sys

# Инициализация Colorama
init(autoreset=True)

# Константы и настройки
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
}
XSS_TEST_SCRIPT = "<Script>alert('XSS')</scripT>"
MAX_CONCURRENT_REQUESTS = 10  # Максимальное количество одновременных запросов

# Асинхронный запрос и обработка ответа
async def fetch(session, url, method='get', data=None):
    try:
        if method == 'post':
            async with session.post(url, data=data) as response:
                return await response.text()
        else:
            async with session.get(url, params=data) as response:
                return await response.text()
    except Exception as e:
        print(f"Ошибка при запросе {url}: {e}")
        return None

# Извлекает детали формы
def extract_form_details(form):
    action = form.attrs.get("action")
    method = form.attrs.get("method", "get").lower()
    inputs = [{"type": inp.attrs.get("type", "text"), "name": inp.attrs.get("name")} for inp in form.find_all("input")]
    if not inputs:
        print(f"{Fore.LIGHTYELLOW_EX}[ {Fore.LIGHTRED_EX}GenXSSHunter {Fore.LIGHTYELLOW_EX}] {Fore.LIGHTBLUE_EX}» Форма при действии {Fore.LIGHTGREEN_EX}{action} {Fore.LIGHTBLUE_EX}не содержит данных, пропускаем")
        return None
    return {"action": action, "method": method, "inputs": inputs}

# Асинхронное тестирование XSS уязвимости
async def test_xss(session, form_details, base_url):
    target_url = urljoin(base_url, form_details["action"])
    data = {inp["name"]: XSS_TEST_SCRIPT for inp in form_details["inputs"] if inp["type"] in ["text", "search"]}
    response = await fetch(session, target_url, method=form_details["method"], data=data)
    if response and XSS_TEST_SCRIPT in response:
        print(f"{Fore.LIGHTYELLOW_EX}[ {Fore.LIGHTRED_EX}GenXSSHunter {Fore.LIGHTYELLOW_EX}] {Fore.LIGHTBLUE_EX}» {Fore.LIGHTYELLOW_EX} XSS обнаружен в {Fore.LIGHTGREEN_EX}{target_url} {Fore.LIGHTYELLOW_EX}с данными {Fore.LIGHTGREEN_EX}{data}")
        return True
    print(f"{Fore.LIGHTYELLOW_EX}[ {Fore.LIGHTRED_EX}GenXSSHunter {Fore.LIGHTYELLOW_EX}] {Fore.LIGHTBLUE_EX}» {Fore.LIGHTYELLOW_EX} не обнаружен XSS в {Fore.LIGHTRED_EX}{target_url}")
    return False

# Сканирует URL на наличие XSS уязвимостей
async def scan_xss(session, url):
    try:
        response = await fetch(session, url)
        if response is None:
            print(f"{Fore.LIGHTYELLOW_EX}[ {Fore.LIGHTRED_EX}GenXSSHunter {Fore.LIGHTYELLOW_EX}] {Fore.LIGHTBLUE_EX}» {Fore.LIGHTYELLOW_EX} Нет ответа от {Fore.LIGHTRED_EX}{url}")
            return
        soup = BeautifulSoup(response, "html.parser")
        forms = soup.find_all("form")
        if not forms:
            print(f"{Fore.LIGHTYELLOW_EX}[ {Fore.LIGHTRED_EX}GenXSSHunter {Fore.LIGHTYELLOW_EX}] {Fore.LIGHTBLUE_EX}» {Fore.LIGHTYELLOW_EX} Не найдено форм на {Fore.LIGHTRED_EX}{url}")
        for form in forms:
            form_details = extract_form_details(form)
            if form_details and form_details["action"] and not form_details["action"].startswith("javascript"):
                if await test_xss(session, form_details, url):
                    save_vulnerable_site(url)
                    print(f"{Fore.LIGHTYELLOW_EX}[ {Fore.LIGHTRED_EX}GenXSSHunter {Fore.LIGHTYELLOW_EX}] {Fore.LIGHTBLUE_EX}» XSS обнаружен на {Fore.LIGHTGREEN_EX}{url}{Style.RESET_ALL}\n[*] Детали формы:")
                    pprint(form_details)
                else:
                    print(f"{Fore.LIGHTYELLOW_EX}[ {Fore.LIGHTRED_EX}GenXSSHunter {Fore.LIGHTYELLOW_EX}] {Fore.LIGHTBLUE_EX}»  {Fore.LIGHTYELLOW_EX}XSS не обнаружен на {Fore.LIGHTRED_EX}{url} {Fore.LIGHTYELLOW_EX}с формой {Fore.LIGHTRED_EX}{form_details}")
    except Exception as e:
        print(f"{Fore.LIGHTYELLOW_EX}[ {Fore.LIGHTRED_EX}GenXSSHunter {Fore.LIGHTYELLOW_EX}] {Fore.LIGHTBLUE_EX}» {Fore.LIGHTYELLOW_EX}Ошибка при сканировании {Fore.LIGHTGREEN_EX}{url}: {Fore.LIGHTRED_EX}{e}")

# Сохраняет уязвимый URL в файл
def save_vulnerable_site(url):
    with open("vulnerable_sites.txt", "a") as file:
        file.write(f"{url}\n")

# Основная функция, управляющая задачами сканирования
async def main(file_with_urls):
    connector = aiohttp.TCPConnector(limit_per_host=MAX_CONCURRENT_REQUESTS)
    async with aiohttp.ClientSession(headers=HEADERS, connector=connector) as session:
        with open(file_with_urls, 'r', encoding="UTF-8") as site_file:
            tasks = []
            for line in site_file:
                site_url = line.strip()
                print(f"{Fore.LIGHTYELLOW_EX}[ {Fore.LIGHTRED_EX}GenXSSHunter {Fore.LIGHTYELLOW_EX}] {Fore.LIGHTBLUE_EX}» Сканирование {Fore.LIGHTGREEN_EX}{site_url}")
                tasks.append(scan_xss(session, site_url))
            await asyncio.gather(*tasks)

if __name__ == "__main__":
    # Если нет аргументов командной строки, выводим логотип и инструкции
    if len(sys.argv) < 2:
        print(f"""{Fore.LIGHTRED_EX}
              
   _____           __   __ _____ _____ _    _             _            
  / ____|          \ \ / // ____/ ____| |  | |           | |           
 | |  __  ___ _ __  \ V /| (___| (___ | |__| |_   _ _ __ | |_ ___ _ __ 
 | | |_ |/ _ \ '_ \  > <  \___ \\___ \|  __  | | | | '_ \| __/ _ \ '__|
 | |__| |  __/ | | |/ . \ ____) |___) | |  | | |_| | | | | ||  __/ |   
  \_____|\___|_| |_/_/ \_\_____/_____/|_|  |_|\__,_|_| |_|\__\___|_|   
                                                                     
{Fore.RESET}
{Fore.LIGHTYELLOW_EX}╭──────────────────────────━━━━━━━━━━━━━━━━━━━━━━━━━━━━──────────────────────╮
| {Fore.LIGHTGREEN_EX}Использование » python {os.path.basename(__file__)} [файл_с_ссылками] {Fore.LIGHTYELLOW_EX}                  |
|                                                                            |
| {Fore.RESET}Этот скрипт сканирует сайты на наличие XSS уязвимостей,                    |
| проверяя формы с помощью простой инъекции скрипта.                         |
| Укажите текстовый файл с URL (по одному на строку) для сканирования.       |
|                                                                            |
| Примеры:                                                                   |
|     {Fore.CYAN}python {os.path.basename(__file__)} sites_to_scan.txt{Fore.RESET}                               |
|                                                                            |
| Инструкции:                                                                |
| - Убедитесь, что URL доступны.                                             |
| - При необходимости настройте длительность сканирования и таймаут запроса. |
| - Результаты будут сохранены в 'vulnerable_sites.txt'.                     |
╰──────────────────────────━━━━━━━━━━━━━━━━━━━━━━━━━━━━──────────────────────╯
""")
    else:
        # Запуск асинхронной главной функции
        asyncio.run(main(sys.argv[1]))
