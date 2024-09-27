# EN
**GenXSSHunter** is an asynchronous script designed to scan websites for XSS vulnerabilities by examining forms on the webpages. This tool is useful for web developers and security researchers to identify and mitigate XSS threats.

## Features
- **Asynchronous Scanning**: Utilizes `aiohttp` for efficient and fast scanning.
- **Form Analysis**: Extracts and analyzes form details to test for XSS vulnerabilities.
- **Customizable**: Supports modification of headers and scanning parameters.

## Usage
1. **Installation**:\
    Ensure Python 3.x and required libraries are installed. Install dependencies using:
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the Script**:
   ```bash
   python GenXSSHunter.py [file_with_urls]
   ```
   Replace `[file_with_urls]` with the path to your text file containing URLs to scan.
3. **Example**:
   ```bash
   python GenXSSHunter.py sites_to_scan.txt
   ```

## Instructions
- Ensure URLs in the text file are accessible.
- Customize scan duration and timeout settings as needed.
- Results will be saved in `vulnerable_sites.txt`.

# RU
**GenXSSHunter** — это асинхронный скрипт, предназначенный для сканирования сайтов на наличие XSS уязвимостей путем анализа форм на веб-страницах. Этот инструмент полезен для веб-разработчиков и специалистов по безопасности для выявления и устранения угроз XSS.

## Особенности
- **Асинхронное сканирование**: Использует aiohttp для эффективного и быстрого сканирования.
- **Анализ форм**: Извлекает и анализирует детали форм для тестирования на XSS уязвимости.
- **Настраиваемость**: Поддерживает изменение заголовков и параметров сканирования.

## Использование
1. **Установка**:\
   Убедитесь, что установлены Python 3.x и необходимые библиотеки. Установите зависимости с помощью:
   ```bash
   pip install -r requirements.txt
   ```
2. **Запуск скрипта**:
   ```bash
   python GenXSSHunter.py [file_with_urls]
   ```
   Замените `[file_with_urls]` на путь к вашему текстовому файлу с URL для сканирования.
3. **Пример**:
   ```bash
   python GenXSSHunter.py sites_to_scan.txt
   ```

## Инструкции
- Убедитесь, что URL-адреса в текстовом файле доступны.
- При необходимости настройте длительность сканирования и тайм-аут.
- Результаты будут сохранены в файле `vulnerable_sites.txt`.
