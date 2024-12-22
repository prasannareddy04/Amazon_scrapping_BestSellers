# Amazon Product Scraper

This project is a Python-based scraper designed to extract product details from Amazon's Best Sellers pages using Selenium. The script logs into Amazon, navigates through specified product categories, and collects information such as product titles, prices, discounts, images, and seller details. The scraped data is then saved in JSON format.

## Features
- **Automated Login**: Logs into Amazon using environment variables for secure credential management.
- **Category Scraping**: Scrapes product data from multiple predefined categories.
- **Data Extraction**: Extracts product title, price, discount, image URL, description, shipping details, and seller information.
- **Error Handling**: Handles missing elements and avoids crashes during data extraction.
- **Data Export**: Saves the scraped data into JSON or CSV format for further analysis.

## Prerequisites
### Software Requirements
- Python 3.7 or higher
- Mozilla Firefox browser
- Geckodriver (managed automatically via `webdriver_manager`)

### Python Libraries
Install the required libraries using the following command:
```bash
pip install selenium webdriver-manager pandas
```

## Setup Environment
1. **Set Up Python Environment**:
   - Ensure Python 3.7 or higher is installed on your system. You can download it from [python.org](https://www.python.org/).
   - Optionally, create a virtual environment for the project:
     ```bash
     python -m venv env
     source env/bin/activate  
     ```

2. **Install Required Libraries**:
   - Install the dependencies listed in the prerequisites section:
     ```bash
     pip install selenium webdriver-manager pandas
     ```

3. **Set Environment Variables**:
   - Create a `.env` file in the project directory or set environment variables directly in your operating system.
   - Add the following lines to your `.env` file:
     ```env
     EMAIL=your_amazon_email
     PASSWORD=your_amazon_password
     ```
   - Replace `your_amazon_email` and `your_amazon_password` with your Amazon account credentials.

4. **Verify Firefox Installation**:
   - Ensure that Mozilla Firefox is installed on your system. You can download it from [mozilla.org](https://www.mozilla.org/).
   - No need to manually install Geckodriver, as it will be managed automatically by `webdriver_manager`.

## How to Use

### Step 1: Clone the Repository
Clone the project repository to local machine

### Step 2: Run the Script
Run the script using the following command:
```bash
python scrappingamazon.py
```

### Step 3: View the Output
The script will save the scraped data in two formats:
- `amazon_products.json`


Both files will be located in the script’s directory.

## Project Structure
```
.
├── scrappingamazon.py     # Main script containing the scraper logic
├── amazon_products.json   # Output JSON file
├── README.md              # Documentation file
```

## Code Overview
### Key Functions
1. `init_firefox_driver`: Initializes a headless Firefox browser for Selenium.
2. `login_amazon`: Logs into Amazon using the provided credentials.
3. `get_products_from_page`: Scrapes product data from a given category URL.
4. `parse_product_data`: Extracts detailed product information from a web element.
5. `save_to_json`: Saves data to a JSON file.

## Error Handling
The script includes robust error handling to deal with missing or stale elements during scraping. Missing elements are logged, and scraping continues without interruptions.

## Developed By
**Prasanna Reddy Avula**

