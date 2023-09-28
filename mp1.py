import json
import timeit
from collections import defaultdict

import requests
import zeep
from bs4 import BeautifulSoup
from genderize import Genderize


def main():
    with open('test.json') as json_file:
        persons = json.load(json_file)
        # Person looks like this {"first_name":"Rand","email":"rcastellanos0@answers.com","ip_address":"40.135.99.35"}
    
    # Find countries and flags
    ips = [person['ip_address'] for person in persons]
    countries = find_countries(ips)
    unique_countries = {country['countryCode'] for country in countries if country['status'] == "success"}
    unique_countries.add("US")
    flags = {country: find_flag_zeep(country) for country in unique_countries}
    
    # Group names by country to make batch requests
    names_by_country = defaultdict(list)
    
    for person, country in zip(persons, countries):
        country_code = country['countryCode'] if country['status'] == "success" else "US"
        names_by_country[country_code].append(person['first_name'])
    
    gender_client = Genderize()
    for country_code, names in names_by_country.items():
        
        flag = flags[country_code]
        genders = gender_client.get(names, country_id=country_code)
        
        for gender in genders:
            
            title = ""
            if gender['gender'] == "female":
                title = "Ms. "
            elif gender['gender'] == "male":
                title = "Mr. "

            # simulation of sending email with Mr. or Ms. their name and the flag of their country as picture attachment
            print(f"""
                Hello {title}{gender['name']}, 
                We would like to invite you to this event ... 
                at this location ...
                at this time ...
                
                Best regards us :)
                {flag}
                """)


def find_country(ip):
    ip_url = f"http://ip-api.com/json/{ip}?fields=country,countryCode"
    try:
        response = requests.request('GET', ip_url).json()
        if response:
            return response # Response looks like this {"country": "United States","countryCode": "US",}
    except:
        print("IP didn't return af response")

# Batch request to get all countries at once
# Max 100 ips per request
def find_countries(ips):
    url = "http://ip-api.com/batch"
    r = requests.post(url, json=ips)
    r.raise_for_status()
    return r.json()

def find_flag(country_code):
    flag_url = "http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso"
    payload = f"""<?xml version=\"1.0\" encoding=\"utf-8\"?>
                <soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\">
                    <soap:Body>
                        <CountryFlag xmlns=\"http://www.oorsprong.org/websamples.countryinfo\">
                            <sCountryISOCode>{country_code}</sCountryISOCode>
                        </CountryFlag>
                    </soap:Body>
                </soap:Envelope>"""
    headers = {'Content-Type': 'text/xml; charset=utf-8'}
    try:  
        response = requests.request("POST", flag_url, headers=headers, data=payload).text
        soup = BeautifulSoup(response, features="xml").find("m:CountryFlagResult").string
        if soup:
            return soup #Soup looks like this http://www.oorsprong.org/WebSamples.CountryInfo/Flags/USA.jpg   
    except:
        print("Flag didnt return a response")

def find_flag_zeep(country_code):
    wsdl = "http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL"
    client = zeep.Client(wsdl=wsdl)
    result = client.service.CountryFlag(country_code)
    return result

def find_gender(country_code, name):
    gender_url = f"https://api.genderize.io?name={name}&country_id={country_code}"
    try:
        response = requests.request('GET', gender_url).json()
        if response:
            return response #Response looks like this {'count': 69, 'name': 'Valaria', 'country_id': 'US', 'gender': 'female', 'probability': 1.0}
    except:
        print("Gender didnt return a response")

if __name__ == "__main__":
    # print(timeit.timeit(main, number=1))
    main()
