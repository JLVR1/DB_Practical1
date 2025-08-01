import csv
from collections import defaultdict

# Reads the CSV file and returns the data as a list of dictionaries.
# Uses UTF-8-SIG encoding to handle files since BOM is needed we use SIG.
def read_csv_data(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8-sig') as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return []
    except Exception as e:
        print(f"Unexpected error reading file: {e}")
        return []

# Question a:
# Count how many unique country names end with the letter a.
# Uses a set to avoid dupes and checks if last letter is a.
def question_a(data):
    countries = {row['CountryName'].strip() for row in data if row['CountryName'].strip().lower().endswith('a')}
    return f"Question a:\n{len(countries)}", countries

# Question b:
# Identify the five cities with the highest population.
# Cities sometimes so up multiple times so we take the highest value of the multiple entries.
# We sort the city-population dictionary in descending order and take the top 5.
def question_b(data):
    city_populations = {}
    for row in data:
        city = row['CityName'].strip()
        try:
            pop = int(row['CityPopulation'])
            city_populations[city] = max(city_populations.get(city, 0), pop)
        except ValueError:
            continue
    top_cities = sorted(city_populations.items(), key=lambda x: x[1], reverse=True)[:5] #This just sorts the data in descending order
    formatted = [f"{city}: {pop}" for city, pop in top_cities]
    return f"\nQuestion b:\n" + '\n'.join(formatted)

def question_c(data):
    country_landmass = {}
    for row in data:
        country = row['CountryName'].strip()
        try:
            lm = int(row['LandMass'])
            country_landmass[country] = max(country_landmass.get(country, 0), lm)
        except ValueError:
            continue
    top_countries = sorted(country_landmass.items(), key=lambda x: x[1], reverse=True)[:5]
    formatted = [f"{country}: {lm}" for country, lm in top_countries]
    return f"\nQuestion c:\n" + '\n'.join(formatted)

def question_d(data):
    countries = set()
    for row in data:
        try:
            year = int(row['IndepYear'])
            if 1960 <= year <= 1980:
                countries.add(row['CountryName'].strip())
        except ValueError:
            continue
    return f"\nQuestion d:\n{len(countries)}"

def question_e(data):
    countries = set()
    for row in data:
        try:
            year = int(row['IndepYear'])
            if 1830 <= year <= 1850:
                countries.add(row['CountryName'].strip())
        except ValueError:
            continue
    return f"\nQuestion e:\n{', '.join(sorted(countries))}"

def question_f(data):
    life_exp = {}
    for row in data:
        if row['Continent'].strip() != 'Africa':
            continue
        try:
            le = float(row['LifeExpectancy'])
            country = row['CountryName'].strip()
            life_exp[country] = max(life_exp.get(country, 0.0), le)
        except ValueError:
            continue
    top_africa = sorted(life_exp.items(), key=lambda x: x[1], reverse=True)[:5]
    formatted = [f"{country}: {le}" for country, le in top_africa]
    return f"\nQuestion f:\n" + '\n'.join(formatted)

def question_g(data):
    language_totals = defaultdict(float)
    for row in data:
        lang = row['Language'].strip()
        try:
            pct = float(row['Percentage'])
            language_totals[lang] += pct
        except ValueError:
            continue
    top_langs = sorted(language_totals.items(), key=lambda x: x[1], reverse=True)[:5]
    formatted = [f"{lang}: {pct:.2f}%" for lang, pct in top_langs]
    return f"\nQuestion g:\n" + '\n'.join(formatted)

def question_h(countries_ending_with_a):
    return f"\nQuestion h:\n{', '.join(sorted(countries_ending_with_a))}"

def analyze_data(input_file, output_file):
    data = read_csv_data(input_file)
    if not data:
        return

    results = []
    # q_a_result is output string for a and countries_a is the set of countries
    # we store both so we dont need to rescan data 
    q_a_result, countries_a = question_a(data)
    results.append(q_a_result)
    results.append(question_b(data))
    results.append(question_c(data))
    results.append(question_d(data))
    results.append(question_e(data))
    results.append(question_f(data))
    results.append(question_g(data))
    results.append(question_h(countries_a))

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(results))
        print(f"Results written to '{output_file}'")
    except Exception as e:
        print(f"Error writing to output file: {e}")

if __name__ == "__main__":
    input_path = 'Database Prac 1/file.txt'
    output_path = 'Database Prac 1/file2.txt'
    analyze_data(input_path, output_path)
