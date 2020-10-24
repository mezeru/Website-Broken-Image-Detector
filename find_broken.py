import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import xlsxwriter
from xlsxwriter import Workbook


if __name__ == "__main__":
    brokenImgs = set()
    
    print("\nEnter the Url : ",end="")

    rawurl = input()                          # The URL of the Website
    
    if(rawurl.startswith('http')):
       url = rawurl
        
    else:
        url = "https://www."+rawurl

    urlContent = requests.get(url)          # Send requests to the website
    
    html = urlContent.content               # Get the HTML content

    soup = BeautifulSoup(html,'html.parser')# Parse through the HTML

    imglinks = soup.find_all('img')         # Find all the img tags attached to the website    

    for i in imglinks:

        rawImgLink = i.get('src')           # Getting Source link for the image
        
        if rawImgLink.startswith('/'):
            rawImgLink = url + rawImgLink   # Correcting the url if it is faulty

        try:
             rem = requests.get(rawImgLink) # Requesting the image at the link
             img = Image.open(BytesIO(rem.content)) # Opening the image remotely
             img.verify()                   # Verifying the image
             
        except IOError:                     # If image is not verified 
             print("The Image at location "+ rawImgLink +" is Broken")
             brokenImgs.add(rawImgLink)

    
    if brokenImgs:
        count = 1
        wb = Workbook('BrokenLink.xlsx')        # Create a WorkBook
        ws = wb.add_worksheet()                 # Create a WorkSheet
        for i in brokenImgs:
            ws.write("A"+str(count),i)          # Write the links
            count = count + 1
        wb.close()
    else:
        print("No Broken Images") 