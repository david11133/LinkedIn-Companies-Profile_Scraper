import json
import scrapy
from scrapy.http import Request
import re
from scrapy.utils.project import get_project_settings
import random
import time

input_file = 'companies2.json'
company_urls = []

def get_urls_from_file():
    try:
        with open(input_file, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            for company_data in data:
                for name, url in company_data.items():
                    company_urls.append(url)
    except FileNotFoundError:
        print(f"Error: JSON file '{input_file}' not found.")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON file. Check the file's format.")
    except Exception as e:
        print(f"An error occurred while reading JSON file: {str(e)}")

# Populate company_urls from the input file
get_urls_from_file()

class CompanyProfileScraperSpider(scrapy.Spider):
    name = 'company_profile_scraper'

    custom_settings = {
        'LOG_LEVEL': 'DEBUG',  # Set logging level to DEBUG to capture detailed logs
        'LOG_FILE': 'scrapy_debug.log',  # Log output will be saved in this file
        'DOWNLOAD_DELAY': 2,  # Delay in seconds between requests
        'DOWNLOAD_DELAY_VARIATION': 1,  # Variation in the delay to make it more unpredictable
        'CONCURRENT_REQUESTS': 1,  # Number of concurrent requests (can be adjusted based on your needs)
    }

    def start_requests(self):
        if not company_urls:
            self.logger.error("No company URLs found. Exiting.")
            return

        self.logger.info(f"Starting requests for {len(company_urls)} URLs.")

        for index, url in enumerate(company_urls):
            self.logger.info(f"Requesting URL: {url}")
            yield Request(url=url, callback=self.parse_response,
                          errback=self.handle_error,
                          meta={'company_index_tracker': index})
            # Adding a delay between requests
            delay = self.get_download_delay()
            self.logger.info(f"Sleeping for {delay} seconds")
            time.sleep(delay)

    def get_download_delay(self):
        """Return a random download delay within the specified range."""
        return self.settings.get('DOWNLOAD_DELAY') + random.uniform(0, self.settings.get('DOWNLOAD_DELAY_VARIATION'))

    def parse_response(self, response):
        company_index_tracker = response.meta['company_index_tracker']
        self.logger.info(f'Scraping page: {company_index_tracker + 1} of {len(company_urls)}')

        company_item = {}
        company_name = response.css('.top-card-layout__entity-info h1::text').get(default='not-found')
        self.logger.info(f"Company Name: {company_name}")

        company_item['company_name'] = company_name.strip()

        try:
            company_item['linkedin_followers_count'] = int(response.xpath(
                '//h3[contains(@class, "top-card-layout__first-subline")]/span/following-sibling::text()').get().split()[
                0].strip().replace(',', ''))
        except (AttributeError, ValueError) as e:
            self.logger.error(f"Error extracting LinkedIn followers count: {e}")
            company_item['linkedin_followers_count'] = 'not-found'

        company_item['company_logo_url'] = response.css(
            'div.top-card-layout__entity-image-container img::attr(data-delayed-url)').get('not-found')

        company_item['about_us'] = response.css('.core-section-container__content p::text').get(
            default='not-found').strip()

        try:
            followers_num_match = re.findall(r'\d{1,3}(?:,\d{3})*',
                                             response.css('a.face-pile__cta::text').get(default='not-found').strip())
            if followers_num_match:
                company_item['num_of_employees'] = int(followers_num_match[0].replace(',', ''))
            else:
                company_item['num_of_employees'] = 'not-found'
        except Exception as e:
            self.logger.error(f"Error occurred while getting number of employees: {e}")
            company_item['num_of_employees'] = 'not-found'

        try:
            company_details = response.css('.core-section-container__content .mb-2')

            company_item['website'] = company_details[0].css(
                'a::text').get(default='not-found').strip()

            company_industry_line = company_details[1].css(
                '.text-md::text').getall()
            company_item['industry'] = company_industry_line[1].strip()

            company_size_line = company_details[2].css(
                '.text-md::text').getall()
            company_item['company_size_approx'] = company_size_line[1].strip().split()[0]

            company_headquarters = company_details[3].css(
                '.text-md::text').getall()
            if company_headquarters[0].lower().strip() == 'headquarters':
                company_item['headquarters'] = company_headquarters[1].strip()
            else:
                company_item['headquarters'] = 'not-found'

            company_type = company_details[4].css('.text-md::text').getall()
            company_item['type'] = company_type[1].strip()

            unsure_parameter = company_details[5].css('.text-md::text').getall()
            unsure_parameter_key = unsure_parameter[0].lower().strip()
            company_item[unsure_parameter_key] = unsure_parameter[1].strip()

            if unsure_parameter_key == 'founded':
                company_specialties = company_details[6].css('.text-md::text').getall()
                if company_specialties[0].lower().strip() == 'specialties':
                    company_item['specialties'] = company_specialties[1].strip()
                else:
                    company_item['specialties'] = 'not-found'
            elif unsure_parameter_key != 'specialties' or unsure_parameter_key == 'founded':
                company_item['founded'] = 'not-found'
                company_item['specialties'] = 'not-found'

            company_item['funding'] = response.css(
                'p.text-display-lg::text').get(default='not-found').strip()
            company_item['funding_total_rounds'] = int(response.xpath(
                '//section[contains(@class, "aside-section-container")]/div/a[contains(@class, "link-styled")]//span[contains(@class, "before:middot")]/text()').get(
                'not-found').strip().split()[0])
            company_item['funding_option'] = response.xpath(
                '//section[contains(@class, "aside-section-container")]/div//div[contains(@class, "my-2")]/a[contains(@class, "link-styled")]/text()').get(
                'not-found').strip()
            company_item['last_funding_round'] = response.xpath(
                '//section[contains(@class, "aside-section-container")]/div//div[contains(@class, "my-2")]/a[contains(@class, "link-styled")]//time[contains(@class, "before:middot")]/text()').get(
                'not-found').strip()

        except IndexError as e:
            self.logger.error(f"Error: Skipped index due to missing details: {e}")

        yield company_item

    def handle_error(self, failure):
        self.logger.error(f"Request failed: {repr(failure)}")
        self.logger.error(f"Failed URL: {failure.request.url}")
