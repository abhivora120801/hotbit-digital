from distutils.command import upload
from fileinput import filename
from xml import dom
import boto3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from io import BytesIO
from PIL import Image
import time
import csv
from bs4 import BeautifulSoup 
from credentials import *

def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    # options.add_argument("--headless")
    driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    driver.maximize_window()
    return driver

def login_apollo(driver,user):
    email,password=get_apollo_creds(user)
    driver.get("https://app.apollo.io")
    time.sleep(5)

    driver.find_element(By.NAME,'email').send_keys(email)
    driver.find_element(By.NAME, 'password').send_keys(password)
    submit_btn = driver.find_element(By.CSS_SELECTOR,"[type = 'submit']").click()

def login_semrush(driver,user):
    username, password = get_sales_navigator_creds(user)
    driver.get("https://proseotools.us/user/login.php")
    time.sleep(2)

    driver.find_element(By.ID,'inputEmail').send_keys(username)
    driver.find_element(By.ID,'inputPassword').send_keys(password)
    driver.find_element(By.XPATH,'/html/body/div[2]/form/button').click()
    #add driver delay
    time.sleep(15)
    driver.get('https://proseotools.us/user/in/access_semrush.php')

def init_s3():
    id,key = get_s3_creds()
    s3 = boto3.client('s3', region_name='us-east-1',aws_access_key_id=id,aws_secret_access_key=key)
    return s3

def go_to_lists(driver):
    driver.get("https://app.apollo.io/#/people/tags?teamListsOnly[]=no")

def get_page_count(driver):
    page_count = driver.find_element(By.XPATH,"/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div[4]/div/div/div/div/div[3]/div/div[1]/span").text
    page_count = int(page_count.split(" ")[-1].replace(",",""))
    if page_count%25==0:
        pages=page_count/25
    else:
        pages=page_count/25+1

    return int(pages)

def sort_by_name(driver):
    url = driver.current_url+"&sortByField=person_name.raw&sortAscending=true"
    driver.get(url)

def extract_data(row,bucket_name,competitor_domain,competitor_name):
    com_linked_in=''
    linked_in=''
    name = row.findAll('td')[0].text.split(' ')[0]
    # error handling for linkedin
    try:
        linked_in = row.findAll('td')[0].select('a[href]')[0].get('href')
        if 'linkedin' not in linked_in:
            linked_in = row.findAll('td')[0].select('a[href]')[1].get('href')
            if 'linkedin' not in linked_in:
                linked_in = row.findAll('td')[0].select('a[href]')[2].get('href')
                if 'linkedin' not in linked_in:
                    linked_in = row.findAll('td')[0].select('a[href]')[3].get('href')
    except:
        pass    
    title = row.findAll('td')[1].text
    company = row.findAll('td')[2].text
    # error handling for company linkedin
    company_website = row.findAll('td')[2].select('a[href]')[1].get('href')

    try:
        com_linked_in = row.findAll('td')[2].select('a[href]')[1].get('href')
        if 'linkedin' not in com_linked_in:
            com_linked_in = row.findAll('td')[2].select('a[href]')[2].get('href')
            if 'linkedin' not in com_linked_in:
                com_linked_in = row.findAll('td')[2].select('a[href]')[3].get('href')
                if 'linkedin' not in com_linked_in:
                    com_linked_in = row.findAll('td')[2].select('a[href]')[4].get('href')
    except:
        pass
    email = row.findAll('td')[4].text
    industry = row.findAll('td')[6].text
    contact_loc = row.findAll('td')[8].text
    company_loc = row.findAll('td')[7].text.replace('N/A',contact_loc)
    
    company_domain = company_website.replace('https://','').replace('http://','').replace('/','')
    
    # print(name,linked_in,title,company,contact_loc,industry,email)
    return {'Name': name,
            'Email':email,
            'linked_in':linked_in,
            'company':company,
            'com_linked_in':com_linked_in,
            'title': title,
            'industry':industry,
            'contact_loc':contact_loc,
            'company_loc':company_loc,
            'company_domain':company_domain
            }

def get_data(driver,page_count,competitor_domain,competitor_name,industry,country,date):
    industry = industry.lower().replace(' ','-')
    country = country.lower().replace(' ','-')
    date = date.replace('_','-').replace('/','-')
    csv_filename = f"{industry}-{country}-{date}.csv"
    bucket_name = f"{industry}-{country}-{date}"
    data = []
    for i in range(1,page_count+1):
        time.sleep(5)
        the_soup = BeautifulSoup(driver.page_source, 'html.parser')
        table=the_soup.findAll('tbody')
        for row in table:
            data.append(extract_data(row,bucket_name,competitor_domain,competitor_name))
        if i<page_count:
            driver.find_element(By.XPATH,"/html/body/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div[2]/div/div[3]/div/div/div/div/div[3]/div/div[2]/button[2]").click()
    return data,bucket_name,csv_filename

def create_s3_bucket(s3,bucket_name):
    s3.create_bucket(Bucket=bucket_name,ObjectOwnership='BucketOwnerPreferred')
    s3.put_public_access_block(Bucket=bucket_name, PublicAccessBlockConfiguration={'BlockPublicAcls': False,'IgnorePublicAcls': False,'BlockPublicPolicy': True,'RestrictPublicBuckets': True})
    s3.put_bucket_acl(ACL='public-read',Bucket=bucket_name)
    return True

def write_to_csv(data,filename,bucket_name):
    with open("/tmp/"+filename, mode='w',newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    s3=init_s3()
    create_s3_bucket(s3,bucket_name)
    s3.upload_file("/tmp/"+filename,bucket_name,filename,ExtraArgs={'ACL':'public-read'})
    return f"https://{bucket_name}.s3.amazonaws.com/{filename}"

def screenshot_to_s3(s3,driver,bucket_name,domain,region='us'):
    domain = domain
    driver.get(f"https://sm.proseotools.us/analytics/overview/?searchType=domain&q={domain}&db={region}")
    time.sleep(5)

    #highlight borders
    driver.execute_script("arguments[0].style.border='3px solid red'", driver.find_element(By.XPATH,'/html/body/div[2]/main/div/div/div[1]/section/div/div[2]/div[1]/h1/div[2]'))
    driver.execute_script("arguments[0].style.border='3px solid red'", driver.find_element(By.XPATH,'/html/body/div[2]/main/div/div/div[2]/div/section[1]/div/div/div[1]'))
    driver.execute_script("arguments[0].style.border='3px solid red'", driver.find_element(By.XPATH,'/html/body/div[2]/main/div/div/div[2]/div/section[1]/div/div/div[2]'))
    driver.execute_script("arguments[0].style.border='3px solid red'", driver.find_element(By.XPATH,'/html/body/div[2]/main/div/div/div[2]/div/section[1]/div/div/div[3]'))
    driver.execute_script("arguments[0].style.border='3px solid red'", driver.find_element(By.XPATH,'/html/body/div[2]/main/div/div/div[2]/div/section[1]/div/div/div[4]'))


    time.sleep(1)    # take screenshot
    screenshot1 = driver.find_element(By.XPATH,'/html/body/div[2]/main/div/div/div[1]').screenshot_as_png
    screenshot2 = driver.find_element(By.XPATH,'/html/body/div[2]/main/div/div/div[2]/div/section[1]').screenshot_as_png

        # add both images in vertical order
    img1 = Image.open(BytesIO(screenshot1))
    img2 = Image.open(BytesIO(screenshot2))

    # resize images to same width
    img1 = img1.resize((img2.width, img1.height))
    img2 = img2.resize((img1.width, img2.height))

    # create a new image with the same size
    new_img = Image.new('RGB', (img1.width, img1.height + img2.height))
    new_img.paste(img1, (0, 0))
    new_img.paste(img2, (0, img1.height))

    # upload image to s3
    object_name = f"{domain}.png"
    new_img.save("/tmp/"+object_name)
    s3.upload_file("/tmp/"+object_name, bucket_name, object_name,ExtraArgs={'ACL': 'public-read'})

    return True

def update_screenshots_to_s3(s3,driver,bucket_name,data,region='us'):
    for item in data:
        domain = item['company_domain']
        screenshot_to_s3(s3=s3,driver=driver,bucket_name=bucket_name,domain=domain,region=region)
        
    return True

def update_competitor_details(data,competitor_name,competitor_domain,bucket_name):
    for i in range(len(data)):
        data[i]['competitor_name']=competitor_name
        data[i]['competitor_semrush']=f"https://real-estate-ny-us-20-02-2024.s3.amazonaws.com/{competitor_domain}.png"
    return data

def update_competitor_and_company_details(data,competitor_name,competitor_domain,bucket_name):
    for i in range(len(data)):
        data[i]['competitor_name']=competitor_name
        data[i]['competitor_semrush']=f"https://{bucket_name}.s3.amazonaws.com/{competitor_domain}.png"
        data[i]['company_semrush']=f"https://{bucket_name}.s3.amazonaws.com/{data[i]['company_domain']}.png"
    return data

def read_from_csv(filename):
    with open(filename) as file:
        data = file.read()
    return data