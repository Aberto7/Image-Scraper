import hashlib, io, pandas as pd, requests, os.path, logging
from bs4 import BeautifulSoup
from pathlib import Path
from PIL import Image
from selenium import webdriver
from selenium.webdriver import EdgeOptions

# Configuring logging to write errors to a file
logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s: %(message)s')

class CSVManager:
    def __init__(self, filename) -> None:
        self.filename = filename
    
    def __enter__(self):
        # Determine if file exists to set mode for CSV writing
        self.mode = 'w' if not os.path.exists(self.filename) else 'a'
        return self
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        pass

    def save_urls_to_csv(self, image_urls):
        # Writing image URLs to a CSV file
        df = pd.DataFrame({"links": image_urls})
        df.to_csv(self.filename, mode=self.mode, index=False, header=(self.mode == 'w'), encoding="utf-8")

def get_content_from_url(url):
    try:
        # Setting up headless browser options
        options = EdgeOptions()
        options.add_argument("--headless=new")
        with webdriver.Edge(options=options) as driver:
            # Accessing URL with a headless browser and getting page content
            driver.get(url)
            page_content = driver.page_source
        return page_content
    except Exception as e:
        # Logging errors when accessing URL
        logging.error(f"Error accessing URL {url}: {e}")
        return None

def parse_image_urls(content, classes, location, source, custom_name_location=None):
    try:
        # Parsing image URLs from HTML content using BeautifulSoup
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
    except Exception as e:
        # Logging errors encountered during parsing
        logging.error(f"Error parsing content: {e}")

def sanitize_filename(filename):
    # Removing forbidden characters from a filename
    forbidden_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|', "'", '*']
    
    for char in forbidden_chars:
        filename = filename.replace(char, " ")
    
    return filename

def get_and_save_image_to_file(image_url, output_dir, custom_filename=None):
    try:
        # Getting image content from URL and saving it to a file
        image_content = requests.get(image_url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert("RGB")
    
        if custom_filename:
            # Generating a custom filename or using a hash of the image content
            sanitized_filename = sanitize_filename(custom_filename)
            filename = sanitized_filename + ".jpg"
        else:
            filename = hashlib.sha1(image_content).hexdigest()[:10] + ".jpg"

        file_path = output_dir / filename
        image.save(file_path, "JPEG", quality=80)
    except requests.exceptions.RequestException as e:
        # Logging errors related to requesting image content
        logging.error(f"Request Error saving image {image_url}: {e}")
    except IOError as e:
        # Logging errors related to file IO
        logging.error(f"IOError saving image {image_url}: {e}")
    except Exception as e:
        # Logging general errors encountered during image saving
        logging.error(f"Error saving image {image_url}: {e}")

def get_website_urls(website_pages=1):
    # Generating URLs for website pages
    website_urls = []
    for p in range(1, website_pages + 1):
        website_urls.append(f'https://asuratoon.com/manga/?page={p}&order=update')
    return website_urls

def main(classes_name, image_location, image_source, image_custom_name_location):
    # Main function to execute the scraping and saving process
    urls = get_website_urls(11)
    with CSVManager("links.csv") as csv_manager:
        for url in urls:
            content = get_content_from_url(url)
            if content:
                image_urls, custom_names = parse_image_urls(
                    content=content, classes=classes_name, location=image_location, source=image_source, custom_name_location=image_custom_name_location
                )
    
                csv_manager.save_urls_to_csv(image_urls) 
    
                output_directory = Path("./Pictures")
                output_directory.mkdir(parents=True, exist_ok=True)
    
                for image_url, custom_name in  zip(image_urls, custom_names):
                    get_and_save_image_to_file(
                        image_url, output_dir=output_directory, custom_filename=custom_name
                    )
            else: 
                # Logging when empty content is returned for a URL
                logging.warning(f"Empty content returned for URL: {url}")

if __name__ == "__main__":
    # Running main function with specified parameters and printing 'Done' upon completion
    main("bsx", "img", "src", "a")
    print("Done")
