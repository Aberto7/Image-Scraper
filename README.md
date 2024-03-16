# Web Scraping and Image Download Script

This Python script allows you to scrape image URLs from a webpage and download the images to your local system. It utilizes Selenium for web scraping and Beautiful Soup for HTML parsing.

## Usage

### Setup

- Make sure you have Python installed on your system.
- Install the required Python libraries by running: 

pip install selenium beautifulsoup4 pandas Pillow

- Download and install the appropriate Microsoft Edge WebDriver from [here](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) based on your system configuration.


### Clone the repository

```bash
git clone https://github.com/your_username/web-scraping.git

### Navigate
cd web-scraping

### Run the Script
python main.py

# Customization
You can modify the url variable in the main() function to specify the webpage from which you want to scrape images.
Adjust the classes, location, and source parameters in the parse_image_urls() function to match the HTML structure of the webpage you're scraping.
Customize the output directory by changing the output_directory variable in the main() function.
You can specify a custom name for downloaded images by passing the custom_name_location parameter to the parse_image_urls() function and adjusting the get_and_save_image_to_file() function accordingly.

# Contributing
Contributions are welcome! If you'd like to contribute to this project, feel free to open an issue or submit a pull request.

# License
This project is licensed under the MIT License. See the LICENSE file for details.