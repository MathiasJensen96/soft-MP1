
import json
import requests
from bs4 import BeautifulSoup


def main():
    with open('MOCK_DATA_TEST.json') as json_file:
        persons = json.load(json_file)

    for person in persons:      #Person looks like this {"first_name":"Rand","email":"rcastellanos0@answers.com","ip_address":"40.135.99.35"}
        country = find_country(person['ip_address'])
        flag = find_flag(country['countryCode'])
        gender = find_gender(country['countryCode'], person['first_name'])

        print(country," | \n", flag," | \n", gender,)

        gender_prefix = ""
        if gender['gender'] == "female":
            gender_prefix = "Ms."
        elif gender['gender'] == "male":
            gender_prefix = "Mr."
        else:
            gender_prefix = "Mr. or Ms."

        # simulation of sending email with Mr. or Ms. their name and the flag of their country as picture attachment
        print(f"""Hello {gender_prefix} {person['first_name']}, 
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
            return response #Response looks like this {"country": "United States","countryCode": "US",}
    except:
        print("IP didn't return af response")


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


def find_gender(country_code, name):
    gender_url = f"https://api.genderize.io?name={name}&country_id={country_code}"
    try:
        response = requests.request('GET', gender_url).json()
        if response:
            return response #Response looks like this {'count': 69, 'name': 'Valaria', 'country_id': 'US', 'gender': 'female', 'probability': 1.0}
    except:
        print("Gender didnt return a response")
    


main()