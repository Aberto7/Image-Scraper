import hashlib, io, pandas as pd, requests
from bs4 import BeautifulSoup
from pathlib import Path
from PIL import Image
from selenium import webdriver
from selenium.webdriver import EdgeOptions



def get_content_from_url(url):
    options = EdgeOptions()
    options.add_argument("--headless=new")
    with webdriver.Edge(options=options) as driver:
        driver.get(url)
        page_content = driver.page_source
    return page_content


def parse_image_urls(content, classes, location, source, custom_name_location=None):
    soup = BeautifulSoup(content, "html.parser")
    results = []
    custom_names = []

    for i in soup.findAll(attrs={'class':classes}):
        name = i.find(location)
        custom_name = i.find(custom_name_location)['title'] if custom_name_location and i.find(custom_name_location) else None


        if name:
            image_url = name.get(source) 
            if image_url and image_url not in results:
                results.append(image_url)
                custom_names.append(custom_name.strip() if custom_name else None)
    
    return results, custom_names


def save_urls_to_csv(image_urls):
    df = pd.DataFrame({"links": image_urls})
    df.to_csv("links.csv", index=False, encoding="utf-8")


def get_and_save_image_to_file(image_url, output_dir, custom_filename=None):
    try:
        image_content = requests.get(image_url).content
        image_file =io.BytesIO(image_content)
        image = Image.open(image_file).convert("RGB")
    
        if custom_filename:
            filename = custom_filename + ".jpg"
        else:
            filename = hashlib.sha1(image_content).hexdigest()[:10] + ".jpg"

        file_path = output_dir / filename
        image.save(file_path, "JPEG", quality=80)
    except Exception as e:
        print(f"Error saving image {image_url}: {e}")





def main():
    url = "https://asuratoon.com/"
    content = get_content_from_url(url)
    image_urls, custom_names = parse_image_urls(
        content=content, classes="imgu", location="img", source="src", custom_name_location="a"
        )
    
    save_urls_to_csv(image_urls) 
    
    output_directory = Path("./Pictures")
    output_directory.mkdir(parents=True, exist_ok=True)
    
    for image_url, custom_name in  zip(image_urls, custom_names):
        get_and_save_image_to_file(
            image_url, output_dir=output_directory, custom_filename=custom_name
            )



if __name__ == "__main__":
    main()
    print("Done")