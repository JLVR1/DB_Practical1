import csv

"""
Reads the CSV file and returns the data as a list of dictionaries.
Uses UTF-8-SIG encoding to handle files that might have a BOM (Byte Order Mark).
"""
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

"""
Question a:
Count how many unique country names end with the letter 'a'.
Uses a set to avoid duplicates and checks if last letter is 'a'.
Returns a formatted string and the set of countries for reuse.
"""
def question_a(data):
    countries = {row['CountryName'].strip() for row in data if row['CountryName'].strip().lower().endswith('a')}
    return f"Question a:\n{len(countries)}", countries

"""
Question b:
Identify the five cities with the highest population.
For cities appearing multiple times, take the highest population value.
Sort in descending order and return the top 5 formatted as strings.
"""
def question_b(data):
    city_populations = {}
    for row in data:
        city = row['CityName'].strip()
        try:
            pop = int(row['CityPopulation'])
            city_populations[city] = max(city_populations.get(city, 0), pop)
        except ValueError:
            continue
    top_cities = sorted(city_populations.items(), key=lambda x: x[1], reverse=True)[:5]
    formatted = [f"{city}: {pop}" for city, pop in top_cities]
    return f"\nQuestion b:\n" + '\n'.join(formatted)

"""
Question c:
Find the five countries with the largest landmass.
For multiple entries of the same country, keep the maximum landmass.
Sort and return top 5 countries formatted as strings.
"""
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

"""
Question d:
Count countries that became independent between 1960 and 1980 inclusive.
Returns the count as a formatted string.
"""
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

"""
Question e:
List countries that became independent between 1830 and 1850 inclusive.
Returns a formatted string with countries sorted alphabetically.
"""
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

"""
Question f:
Find the top five African countries by highest life expectancy.
For multiple entries, keep the maximum life expectancy.
Returns formatted string with results.
"""
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

"""
Question g:
Calculate total percentages for each language and compute each language's
percentage share relative to total.
Return the top 5 languages formatted with percentage values.
"""
def question_g(data):
    language_totals = {}
    for row in data:
        lang = row.get('Language', '').strip()
        perc_str = row.get('Percentage', '').strip()
        if lang and perc_str:
            try:
                perc = float(perc_str)
                language_totals[lang] = language_totals.get(lang, 0) + perc
            except ValueError:
                continue

    total_sum = sum(language_totals.values())
    if total_sum == 0:
        language_percentages = {}
    else:
        language_percentages = {
            lang: (total / total_sum) * 100
            for lang, total in language_totals.items()
        }

    top_5_languages = sorted(language_percentages.items(), key=lambda x: x[1], reverse=True)[:5]
    formatted = [f"{lang}: {pct:.2f}%" for lang, pct in top_5_languages]
    return f"\nQuestion g:\n" + '\n'.join(formatted)

"""
Question h:
Outputs the list of countries ending with 'a' from question a, sorted alphabetically.
"""
def question_h(countries_ending_with_a):
    return f"\nQuestion h:\n{', '.join(sorted(countries_ending_with_a))}"

"""
Main function that reads data, runs all questions, collects results,
and writes them to the specified output file.
"""
def analyze_data(input_file, output_file):
    data = read_csv_data(input_file)
    if not data:
        return

    results = []

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
