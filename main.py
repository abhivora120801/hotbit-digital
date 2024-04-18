from ast import main
import tkinter as tk
from tkinter import ttk  # For enhanced widgets (optional)
from tkinter import filedialog  # For file selection (optional)
import datetime  # For date picker functionality
from methods import *



# Placeholder functions (replace with your scraper logic)
def initialize_driver():
     # Access global driver (if declared)
    global main_driver
    main_driver = init_driver()  # Call init_driver and store the returned value

def quit_apollo_driver():
    global main_driver
    main_driver.quit()  # Quit the driver

def login_apollo_(user):
    global main_driver
    login_apollo(main_driver, user)

def scrape_apollo(url, list_name, num_pages):
    global main_driver
    automate_prospecting_apollo(main_driver,url, list_name,num_pages)

def init_sales_navigator_driver():
    print("Initializing Sales Navigator driver...")

def quit_sales_navigator_driver():
    print("Quitting Sales Navigator driver...")

def login_sales_navigator(user):
    global main_driver
    login_linkedin_sales_navigator(main_driver, user)

def scrape_sales_navigator(url, list_name, num_pages):
    print(f"Scraping Sales Navigator: URL: {url}, List Name: {list_name}, Pages: {num_pages}")

def extract_data_gui(campaign_name, num_pages, date_picker_value, platform, country):
    if platform == "apollo":
        main_data,bucket_name,csv_file_name=get_data(main_driver,num_pages,campaign_name,country,date_picker_value)
        csv_url=write_to_csv(data=main_data,filename=csv_file_name,bucket_name=bucket_name)
        csv_url_text.insert(tk.END, csv_url)  # Insert the CSV URL (replace with actual URL)

    elif platform == "sales_navigator":
        print(f"Extracting data for Sales Navigator: Campaign Name: {campaign_name}, Pages: {num_pages}, Date: {date_picker_value}")


def copy_to_clipboard():
    # Retrieve content
    root.clipboard_clear()  # Clear any existing clipboard content (optional)
    root.clipboard_append(csv_url_text.get("1.0", tk.END).strip())  # Write csv_url to the clipboard

# Create the main window
root = tk.Tk()
root.title("Scraper Tool GUI")
root.geometry("800x600")  # Adjust window size as needed

# Chrome Driver section
chrome_driver_label = tk.Label(root, text="Chrome Driver")
chrome_driver_label.pack(pady=10)

init_driver_button = tk.Button(root, text="Start Chrome Driver", command=initialize_driver)  # Placeholder for Apollo driver
init_driver_button.pack(padx=10, pady=5)

quit_driver_button = tk.Button(root, text="Quit Chrome Driver", command=quit_apollo_driver)  # Placeholder for Apollo driver
quit_driver_button.pack(padx=10, pady=5)

# Separator
separator_1 = ttk.Separator(root, orient=tk.HORIZONTAL)
separator_1.pack(fill=tk.X, padx=10, pady=10)

# Vertical columns (Apollo and Sales Navigator)
apollo_frame = tk.Frame(root)
apollo_frame.pack(side=tk.LEFT, padx=10, pady=10)

sales_navigator_frame = tk.Frame(root)
sales_navigator_frame.pack(side=tk.RIGHT, padx=10, pady=10)

# Apollo section

apollo_label = tk.Label(apollo_frame, text="Apollo Scraper")
apollo_label.pack()

apollo_user_label = tk.Label(apollo_frame, text="User:")
apollo_user_label.pack()

# Use a Combobox or other suitable widget for user selection
user_options = ["user1", "user2", "user3"]  # Replace with your user data
apollo_user_combo = ttk.Combobox(apollo_frame, values=['avora', 'tools', 'achugh'], state="readonly")
apollo_user_combo.current(0)  # Pre-select the first user (optional)
apollo_user_combo.pack()

apollo_login_button = tk.Button(apollo_frame, text="Login", command=lambda: login_apollo_(apollo_user_combo.get().strip()))
apollo_login_button.pack(pady=5)

apollo_url_label = tk.Label(apollo_frame, text="URL:")
apollo_url_label.pack()

apollo_url_entry = tk.Entry(apollo_frame)
apollo_url_entry.pack()

apollo_list_name_label = tk.Label(apollo_frame, text="List Name:")
apollo_list_name_label.pack()

apollo_list_name_entry = tk.Entry(apollo_frame)
apollo_list_name_entry.pack()

apollo_num_pages_label = tk.Label(apollo_frame, text="Number of Pages:")
apollo_num_pages_label.pack()

apollo_num_pages_entry = tk.Entry(apollo_frame)
apollo_num_pages_entry.pack()

apollo_scrape_button = tk.Button(apollo_frame, text="Prospect", command=lambda: scrape_apollo(apollo_url_entry.get().strip(), apollo_list_name_entry.get().strip(), int(apollo_num_pages_entry.get())))
apollo_scrape_button.pack(pady=5)

# Sales Navigator section

sales_navigator_label = tk.Label(sales_navigator_frame, text="Sales Navigator Scraper")
sales_navigator_label.pack()

sales_navigator_user_label = tk.Label(sales_navigator_frame, text="User:")
sales_navigator_user_label.pack()

# Use a Combobox or other suitable widget for user selection
sales_navigator_user_combo = ttk.Combobox(sales_navigator_frame, values=['gouravrathore6161'], state="readonly")
sales_navigator_user_combo.current(0)  # Pre-select the first user (optional)
sales_navigator_user_combo.pack()

sales_navigator_login_button = tk.Button(sales_navigator_frame, text="Login", command=lambda: login_sales_navigator(sales_navigator_user_combo.get().strip()))
sales_navigator_login_button.pack(pady=5)

sales_navigator_url_label = tk.Label(sales_navigator_frame, text="URL:")
sales_navigator_url_label.pack()

sales_navigator_url_entry = tk.Entry(sales_navigator_frame)
sales_navigator_url_entry.pack()

sales_navigator_list_name_label = tk.Label(sales_navigator_frame, text="List Name:")
sales_navigator_list_name_label.pack()

sales_navigator_list_name_entry = tk.Entry(sales_navigator_frame)
sales_navigator_list_name_entry.pack()

sales_navigator_num_pages_label = tk.Label(sales_navigator_frame, text="Number of Pages:")
sales_navigator_num_pages_label.pack()

sales_navigator_num_pages_entry = tk.Entry(sales_navigator_frame)
sales_navigator_num_pages_entry.pack()

sales_navigator_scrape_button = tk.Button(sales_navigator_frame, text="Prospect", command=lambda: scrape_sales_navigator(sales_navigator_url_entry.get().strip(), sales_navigator_list_name_entry.get().strip(), int(sales_navigator_num_pages_entry.get())))
sales_navigator_scrape_button.pack(pady=5)

# Data Extraction section
data_extraction_label = tk.Label(root, text="Data Extraction")
data_extraction_label.pack()
# platform  dropdown
platform_label = tk.Label(root, text="Platform:")
platform_label.pack()

# Use a Combobox or other suitable widget for country selection
platform_options = ["apollo", "sales_navigator"]  # Replace with your country data
platform_combo = ttk.Combobox(root, values=platform_options, state="readonly")
platform_combo.current(0)  # Pre-select the first country (optional)
platform_combo.pack()

campaign_name_label = tk.Label(root, text="Campaign Name:")
campaign_name_label.pack()

campaign_name_entry = tk.Entry(root)
campaign_name_entry.pack()

# campaign country dropdown
campaign_country_label = tk.Label(root, text="Country:")
campaign_country_label.pack()

# Use a Combobox or other suitable widget for country selection
country_options = ["US", "Canada", "UK", "Australia"]  # Replace with your country data
campaign_country_combo = ttk.Combobox(root, values=country_options, state="readonly")
campaign_country_combo.current(0)  # Pre-select the first country (optional)
campaign_country_combo.pack()

num_pages_label = tk.Label(root, text="Number of Pages:")
num_pages_label.pack()

num_pages_entry = tk.Entry(root)
num_pages_entry.pack()

date_picker_label = tk.Label(root, text="Select Date:")
date_picker_label.pack()

date_picker_value = tk.StringVar()
today = datetime.datetime.now()
date_options = [today.strftime("%d-%m-%Y")]  # Initialize with today's date
for i in range(1, 28):
    date_options.append((today + datetime.timedelta(days=i)).strftime("%d-%m-%Y"))  # Add next 28 days

date_picker = ttk.Combobox(root, values=date_options, textvariable=date_picker_value, state="readonly")
date_picker.current(0)  # Pre-select today's date
date_picker.pack()

extract_data_button = tk.Button(root, text="Extract Data", command=lambda: extract_data_gui(campaign_name_entry.get().strip(), int(num_pages_entry.get()), date_picker.get().strip(), platform_combo.get().strip(), campaign_country_combo.get().strip()))
extract_data_button.pack(pady=5)

# read only text box for csv url
csv_url_label = tk.Label(root, text="CSV URL:")
csv_url_label.pack()

csv_url_text = tk.Text(root, height=1, width=50)
csv_url_text.pack()
csv_url_text.config(state=tk.DISABLED)  # Disable editing

# copy button to copy csv url
copy_button = tk.Button(root, text="Copy", command=copy_to_clipboard)
copy_button.pack(pady=5)


root.mainloop()  # Start the GUI