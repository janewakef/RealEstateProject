import bs4
import urllib
import pandas as pd
import datetime

# returns the soup based on the url and headers given.
# Prints error message if website recognizes us as bot.
def get_soup(url, headers):
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
def get_page_links(city_url, num_pages):
    page_list = []
    i = 1
    while i - 1 < num_pages:
        page_list.append(city_url + "/pg-" + str(i))
        i = i + 1

    return page_list



# process the house given the url to the house's entry, headers, and the dataframe (df). adds info as row to df.
def process_page(page_url, headers, df):
    soup = get_soup(page_url, headers)
    
    houses = [house for house in soup.find_all('li', {'class', "component_property-card js-component_property-card"})]


    for house in houses:
        listing_id = house.get("data-listingid").strip()
        latlong = house.find_all("meta")
        if latlong != None:
            latitude = latlong[0].get("content").strip()
            longitude = latlong[1].get("content").strip()
        sold_date = house.find("span", {"class","label c_label label-gray-darker"})
        if sold_date != None:
            sold_date = sold_date.text.split("on ")[1].strip()
        url = "https://www.realtor.com" + house.get("data-url").strip()
        image = house.find("img")
        if image != None:
            image = image.get("src").strip()
        price = house.find("span", {"class","data-price"})
        if price != None:
            price = price.text.strip().replace("$", "").replace(",", "")

        stAdd = house.find("span", {'itemprop':'streetAddress'})
        if stAdd != None:
            stAdd = stAdd.text.strip()
        city = house.find("span", {'itemprop':'addressLocality'})
        if city != None:
            city = city.text.strip()
        region = house.find("span", {'itemprop':'addressRegion'})
        if region != None:
            region = region.text.strip()
        postalCode = house.find("span", {'itemprop':'postalCode'})
        if postalCode != None:
            postalCode = postalCode.text.strip()
        bed = house.find("span", {"class":"data-value meta-beds"})
        if bed != None:
            bed = bed.text.strip()
        bath = house.find("li", {"data-label":"property-meta-baths"})
        if bath != None:
            bath = bath.span.text.strip()
        sqft = house.find("li", {"data-label":"property-meta-sqft"})
        if sqft != None:
            sqft = sqft.span.text.strip().replace(",", "")
        garage = house.find("li", { "data-label":"property-meta-garage"})
        if garage != None:
            garage = garage.span.text.strip()
        prop_type = soup.find("div",  {"class":"property-type"})
        if prop_type != None:
            prop_type = prop_type.text.strip()
        info_list = [listing_id, url, image, prop_type, stAdd, city, region, postalCode, latitude, longitude, price, sold_date, bed, bath, sqft, garage]
        df.loc[df.shape[0]] = info_list


                

def main():


    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"}
    city_url = "https://www.realtor.com/soldhomeprices/Columbus_OH"
    names  = ["listing id", "url", "image", "prop type", "street address", "city", "state", "postal code", "latitude", "longitude", "price", "sold_date",  "bed", "bath", "sqft", "garage"]
  
    # create dataframe
    sold_houses = pd.DataFrame(columns= names)
    #fill dataframe
    pages = get_page_links(city_url, 5)
    for page in pages:
        process_page(page, headers, sold_houses)
    #print dataframe
    print(sold_houses)

    #dataframe to excel to save it
    pd.DataFrame.to_excel(excel_writer = r"Documents\RealEstate" + str(datetime.date.today()) + ".xlsx", index = False, self=sold_houses)




if __name__ == "__main__":
    main()

