import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

url = 'https://yoursiteurl/'

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    about_section = soup.find('section', id='about')

    if about_section:
        os.makedirs('siteFiles', exist_ok=True)

        # Find CSS, JS, Images and other files find and download
        def download_file(url, folder):
            local_filename = os.path.join(folder, os.path.basename(urlparse(url).path))
            with requests.get(url, stream=True) as r:
                with open(local_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            return local_filename

        css_links = []
        js_links = []
        image_links = []

        # CSS files
        for link in soup.find_all('link', rel='stylesheet'):
            css_url = urljoin(url, link['href'])
            local_css_file = download_file(css_url, 'siteFiles')
            css_links.append(local_css_file)
            print(f"CSS dosyası indirildi: {css_url}")

        # JS files
        for script in soup.find_all('script', src=True):
            js_url = urljoin(url, script['src'])
            local_js_file = download_file(js_url, 'siteFiles')
            js_links.append(local_js_file)
            print(f"JS dosyası indirildi: {js_url}")

        # Other files & images
        for img in about_section.find_all('img'):
            img_url = urljoin(url, img['src'])
            local_img_file = download_file(img_url, 'siteFiles')
            img['src'] = local_img_file
            image_links.append(local_img_file)
            print(f"Resim dosyası indirildi: {img_url}")

        # HTML content
        html_content = about_section.prettify()

        # CSS and JS files add in HTML files
        css_imports = ''.join([f'<link rel="stylesheet" href="{css}">\n' for css in css_links])
        js_imports = ''.join([f'<script src="{js}"></script>\n' for js in js_links])

        final_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>About Section</title>
            {css_imports}
        </head>
        <body>
            {html_content}
            {js_imports}
        </body>
        </html>
        """

        # Save HTML files
        with open('about_section.html', 'w', encoding='utf-8') as file:
            file.write(final_html)
        print("HTML files created: about_section.html")

    else:
        print('<section id="about"> not found.')
else:
    print('Web site downloaded.')