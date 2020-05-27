import bs4
import urllib
import requests
import pandas as pd
import time
import random

# returns the soup based on the url and headers given.
# Prints error message if website recognizes us as bot.
def get_soup(url, headers):
    time.sleep(random.randint(120, 400))
    request = urllib.request.Request(url, headers=headers)
    source = urllib.request.urlopen(request).read()
    soup = bs4.BeautifulSoup(source,'html.parser')
    text = ""
    for tag in soup.find_all("p"):
        text = text + tag.text
    if "something about your browser" in text:
        print("ERROR -- recognized as bot with " + url)
    else:
        print("worked for " + url)

    return soup

# creates the urls to all the pages of the city, returns these in a list
def get_page_links(city_soup, city_url):
    num_pages = 7
    # TODO: make this work
    #num_pages = city_soup.find_all("span", {"class":"page"})[1].text
    page_list = [city_url]
    i = 2
    while i - 1 < num_pages:
        page_list.append(city_url + "/pg-" + str(i))
        i = i + 1

    return page_list


# gets the links to the entry of each house on the page, returns these in a list
def get_house_links_from_page(page_soup):
    house_urls = [("https://www.realtor.com" + house.get("data-url")) for house in page_soup.find_all('li', {'class', "component_property-card js-component_property-card"})]
    return house_urls


# process the house given the url to the house's entry, headers, and the dataframe (df). adds info as row to df.
def process_house(house_url, headers, df):
    soup = get_soup(house_url, headers)

    # TODO: check if error message came up and don't continue if so

    property_id = soup.find("div", {"class":"pull-right js-tracking"})
    if property_id != None:
        property_id = property_id.get("data-propertyid") 
    

    listing_id = soup.find("div", {"class":"pull-right js-tracking"})
    if listing_id != None:
        listing_id = listing_id.get("data-listingid") 
    

    street_address = soup.find("meta", {"property":"og:street-address"})
    if street_address != None:
        street_address = street_address.get("content")

    
    city = soup.find("meta", {"property":"og:locality"})
    if city != None:
        city = city.get("content")
        
    state = soup.find("meta", {"property":"og:region"})
    if state != None:
        state = state.get("content")

    zip_code = soup.find("meta", {"property":"og:postal-code"})
    if zip_code != None:
        zip_code = zip_code.get("content")


    latitude = soup.find("meta", {"property":"place:location:latitude"})
    if latitude != None:
        latitude = latitude.get("content")

    longitude = soup.find("meta", {"property":"place:location:longitude"})
    if longitude != None:
        longitude = longitude.get("content")
    

    image = soup.find("meta", {"name":"twitter:image"})
    if image != None:
        image = image.get("content")

    
    price = soup.find("span", {"itemprop":"price"})
    if price != None:
        price = price.get("content")

    sold_date = soup.find("span", {"data-label":"property-meta-sold-date"})
    if sold_date != None:
        sold_date = sold_date.text.replace("Sold on ", "").strip()
    
    
    school_dist = soup.find('ul', {"class", "list-default list-prop-details-schools"})
    if school_dist != None:
        school_dist = school_dist.text.strip()
    
    
    # done in case other does not work for all
    beds = soup.find("li", {"data-label":"property-meta-beds"})
    if beds != None:
        beds = beds.find("span").text


    baths = soup.find("li", {"data-label":"property-meta-bath"})
    if baths != None:
        baths = baths.find("span").text
    

    lot_size = soup.find("li", {"data-label":"property-meta-lotsize"})
    if lot_size != None:
        lot_size = lot_size.find("span").text

    # this gets all the house info, we will need to see if the terms are uniform and if
    # so we can very easily just clean them up and assign them to vairables
    # TODO: look into this more
    #house_details = soup.find('ul', {'class': "list-default row"})
    #features = [feature.text for feature in house_details.find_all('li')]

    info_list = [property_id, listing_id, house_url, street_address, city, state, zip_code, latitude, longitude, image, price, sold_date, school_dist, beds, baths, lot_size]
    df.loc[df.shape[0]] = info_list


# processes a city. give basic city url, headers, and a dataframe.
# fills dataframe with info from every house on every page of the city.
def process_city(city_url, headers, df):
    city_soup = get_soup(city_url, headers)
    city_pages = get_page_links(city_soup, city_url)
    for page in city_pages:
        if page == city_url:
            page_soup = city_soup
        else:
            page_soup = get_soup(page, headers)
        house_urls = get_house_links_from_page(page_soup)
        for house in house_urls:
            process_house(house, headers, df)

            








def main():


    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"}
    city_url = "https://www.realtor.com/soldhomeprices/Columbus_OH"
    col_names = ["property id", "listing id", "url", "street address", "city", "state", "zip code", "latitude", "longitude", "image", "price", "sold date", "school district", "beds", "bath", "lotsize"]
    
    # create dataframe
    sold_houses = pd.DataFrame(columns=col_names)
    #fill dataframe
    process_city(city_url, headers, sold_houses)
    #print dataframe
    print(sold_houses)

    #dataframe to excel to save it
    pd.DataFrame.to_excel(excel_writer = r"Documents\RealEstate.xlsx", index = False, self=sold_houses)




if __name__ == "__main__":
    main()

