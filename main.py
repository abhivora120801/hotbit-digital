from tkinter import *
from tkinter import ttk  # for dropdown menu


# Main GUI window
window = Tk()
window.title("Apollo Scraper Tool")

# Tools dropdown menu
tool_label = Label(window, text="Select Tool:")
tool_label.pack(pady=5)
tool_options = ["-- Select Tool --","tools", "achugh", "avora"]  # Replace with actual tools
tool_variable = StringVar(window)
tool_variable.set(tool_options[0])  # Set default option
tool_dropdown = ttk.Combobox(window, values=tool_options, textvariable=tool_variable)
tool_dropdown.pack(pady=5)

# URL input field
url_label = Label(window, text="Enter URL:")
url_label.pack(pady=5)
url_entry = Entry(window)
url_entry.pack(pady=5)

# Number of pages input field
num_pages_label = Label(window, text="Number of Pages:")
num_pages_label.pack(pady=5)
num_pages_entry = Entry(window)
num_pages_entry.pack(pady=5)

# Scrape button
scrape_button = Button(window, text="Scrape", command=lambda: scrape_apollo(tool_variable.get(), url_entry.get(), num_pages_entry.get()))
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
