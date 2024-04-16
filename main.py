from lib2to3.pgen2 import driver
from tkinter import *
from tkinter import ttk  # for dropdown menu
from methods import *
driver=init_driver()

# Main GUI window
window = Tk()
window.title("Scraper Tool")

# Quit button
quit_button = Button(window, text="Quit", command=driver.quit)
quit_button.pack(pady=10)

# Tools dropdown menu
tool_label = Label(window, text="Select Tool:")
tool_label.pack(pady=5)
tool_options = ["-- Select User --","tools", "achugh", "avora"]  # Replace with actual tools
tool_variable = StringVar(window)
tool_variable.set(tool_options[0])  # Set default option
tool_dropdown = ttk.Combobox(window, values=tool_options, textvariable=tool_variable)
tool_dropdown.pack(pady=5)

# add login and logout button side by side
login_button = Button(window, text="Login", command=lambda: login_apollo(driver, tool_variable.get()))
login_button.pack(pady=10)

# URL input field
url_label = Label(window, text="Enter URL:")
url_label.pack(pady=5)
url_entry = Entry(window)
url_entry.pack(pady=5)

# List Name input field
list_name_label = Label(window, text="List Name:")
list_name_label.pack(pady=5)
list_name_entry = Entry(window)
list_name_entry.pack(pady=5)


# Number of pages input field
num_pages_label = Label(window, text="Number of Pages:")
num_pages_label.pack(pady=5)
num_pages_entry = Entry(window)
num_pages_entry.pack(pady=5)

# Scrape button
scrape_button = Button(window, text="Scrape", command=lambda: automate_prospecting(driver, url_entry.get(),list_name_entry.get() ,num_pages_entry.get()))
scrape_button.pack(pady=10)

# Separator line
separator = ttk.Separator(window, orient=HORIZONTAL)
separator.pack(fill=X, padx=20, pady=10)

# Data extraction labels and entries
campaign_name_label = Label(window, text="Campaign Name:")
campaign_name_label.pack(pady=5)
campaign_name_entry = Entry(window, state='disabled')
campaign_name_entry.pack(pady=5)

# country_label = Label(window, text="Country:")
# country_label.pack(pady=5)
# country_entry = Entry(window, state='disabled')
# country_entry.pack(pady=5)

# country dropdown menu
country_options = ["-- Select Country --","us", "uk"]  # Replace with actual countries
country_variable = StringVar(window)
country_variable.set(country_options[0])  # Set default option
country_dropdown = ttk.Combobox(window, values=country_options, textvariable=country_variable, state='disabled')
country_dropdown.pack(pady=5)


date_label = Label(window, text="Date:")
date_label.pack(pady=5)
date_entry = Entry(window, state='disabled')
date_entry.pack(pady=5)

# Extract button (disabled for now)
extract_button = Button(window, text="Extract Data", state='disabled', command=lambda: extract_data(scrape_apollo(tool_variable.get(), url_entry.get(), num_pages_entry.get())))
extract_button.pack(pady=10)

window.mainloop()
