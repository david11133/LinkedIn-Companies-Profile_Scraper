# LinkedIn Company Data Scraping System

This project, LinkedIn Company Data Scraping System, is a Python-based tool built using the Scrapy framework to scrape data from LinkedIn. It is designed to extract detailed information about companies from LinkedIn, including both directory listings and individual company profiles.

## Key Components and Functionality

1. **LinkedIn Directory Scraper**:

- **Purpose**: This component scrapes a directory of company names and their LinkedIn URLs from LinkedIn's company directory.
- **Output**: The output is a JSON file containing a list of company names and their associated LinkedIn URLs. The format looks like this:

```json
[
  {"company_name_1": "url_of_the_company"},
  {"company_name_2": "url_of_the_company"},
  ...
]
```

2. **LinkedIn Company Profile Scraper**:

- Purpose: This component digs deeper by scraping detailed information from the LinkedIn profiles of the companies listed in the directory.
- Input: It takes the LinkedIn URLs extracted by the Directory Scraper and uses them to visit each company's LinkedIn page.
- Output: The output is a JSON file containing extensive details about each company, including:
- Company name
- Number of LinkedIn followers
- Company logo URL
- About Us section
- Number of employees
- Website URL
- Industry
- Company size
- Headquarters location
- Type (e.g., Partnership, Public Company)
- Founding year
- Specialties
- Funding information (including total rounds and last round details)

**Installation and Setup**

Here’s how to install and run the project:

1. **Clone the Repository**:

- **Open your terminal and clone the repository using**:

```bash
git clone https://github.com/KarthikDani/LinkedIn-Company-Data-Scraping-System.git
```

- **Navigate into the cloned repository**:

```bash
cd LinkedIn-Company-Data-Scraping-System
```

2. **(Optional) Create a Virtual Environment**:

- It’s a good practice to create a virtual environment to avoid conflicts with other Python packages:

```bash
python3 -m venv venv
```
- Activate the virtual environment:
On Linux/macOS:
```bash
source venv/bin/activate
```
On Windows:
```bash
venv\Scripts\activate
```

3. **Install Required Packages**:

- Install the dependencies needed for the project:
```bash
pip install scrapy requests
```

## Running the Scrapers
1. **LinkedIn Directory Scraper**:

- To run the scraper that collects company names and URLs:
```bash
scrapy crawl linkedin_directory_scraper -O directory_data.
```

- This will output a JSON file (`directory_data.json`) containing the directory of companies and their LinkedIn URLs.

2. **LinkedIn Company Profile Scraper**:

- Populate the desired_company_names list in the company_profile_scraper.py file with the names of the companies you want detailed information about:
```python
desired_company_names = ["Microsoft", "OpenAI"]
```

- Run the scraper to collect detailed company profiles:
```bash
scrapy crawl company_profile_scraper -O company_profile_data.
```

- This will output a JSON file (company_profile_data.json) containing detailed information about each company.