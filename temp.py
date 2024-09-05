import json

# File paths
companies_file = 'company_data_scraper\\companies.json'
company_profile_file = 'companies_profile.json'
output_file = 'companies2.json'

def load_json_file(file_path):
    """Load JSON data from a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_json_file(file_path, data):
    """Save JSON data to a file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def main():
    # Load data from JSON files
    companies_data = load_json_file(companies_file)
    company_profile_data = load_json_file(company_profile_file)

    # Create a set of company names from the company_profile_data
    existing_companies = set(item['company_name'] for item in company_profile_data)

    # Create a dictionary to hold companies that need to be added to the new file
    companies_to_add = {}

    # Flatten companies_data into a dictionary for easy lookup
    companies_dict = {name: url for company_dict in companies_data for name, url in company_dict.items()}

    # Iterate through companies_dict and find companies not in existing_companies
    for company_name, url in companies_dict.items():
        if company_name not in existing_companies:
            companies_to_add[company_name] = url

    # Save the results to the output file
    save_json_file(output_file, [companies_to_add])

    print(f"Companies that are in {companies_file} but not in {company_profile_file} have been added to {output_file}.")

if __name__ == '__main__':
    main()
