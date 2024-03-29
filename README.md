# Image Scraper

This Python script is designed to scrape images from a website and save them locally. Here's a breakdown of its functionality:

## Dependencies
To run this script, you need to install the following Python libraries:
- `hashlib`
- `io`
- `pandas`
- `requests`
- `os`
- `logging`
- `bs4` (BeautifulSoup)
- `pathlib`
- `PIL` (Pillow)
- `selenium`

You can install these using pip:
```bash
pip install pandas requests beautifulsoup4 Pillow selenium
```

## CSVManager Class
This class manages the CSV file where the image URLs will be stored. It opens the file in write mode if it doesn't exist, otherwise it opens it in append mode.

## get_content_from_url Function
This function uses Selenium's webdriver to navigate to a given URL and return the page's HTML content.

## parse_image_urls Function
This function uses BeautifulSoup to parse the HTML content, find the image URLs based on the provided classes, location, and source, and return them along with their custom names.

## sanitize_filename Function
This function replaces any forbidden characters in the filename with a space to ensure the filename is valid.

## get_and_save_image_to_file Function
This function retrieves the image from the given URL, converts it to RGB format, and saves it locally. If a custom filename is provided, it sanitizes the filename and uses it. Otherwise, it generates a filename using a hash of the image content.

## get_website_urls Function
This function generates a list of website URLs based on the number of pages provided.

## main Function
This function orchestrates the entire process. It retrieves the website URLs, gets the content of each URL, parses the image URLs, saves the image URLs to a CSV file, and then retrieves and saves each image locally.

## Running the Script
To run the script, simply execute the Python file. The script will scrape images from the specified website and save them locally in a directory named "Pictures". It will also save the image URLs in a CSV file named "links.csv".

```bash
python script_name.py
```
Replace `script_name.py` with the name of your Python file. After the script finishes running, you should see a "Done" message printed to the console.