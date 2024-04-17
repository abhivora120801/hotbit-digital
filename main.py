from tkinter import *
from tkinter import ttk  # for separator and dropdown

# Placeholder functions for now, replace with your actual scraping logic
def login_apollo(user_account, url, listname, num_pages):
    print(f"Logging in to Apollo with {user_account}, Scraping: {url}, List: {listname}, Pages: {num_pages}")

def login_linkedin(user_account, url, listname, num_pages):
    print(f"Logging in to LinkedIn Sales Navigator with {user_account}, Scraping: {url}, List: {listname}, Pages: {num_pages}")

def scrape_apollo(user_account, url, listname, num_pages):
    print(f"Scraping with Apollo using account: {user_account}, URL: {url}, List: {listname}, Pages: {num_pages}")
    # Replace with your actual scraping logic

def scrape_linkedin(user_account, url, listname, num_pages):
    print(f"Scraping with LinkedIn Sales Navigator using account: {user_account}, URL: {url}, List: {listname}, Pages: {num_pages}")
    # Replace with your actual scraping logic

# Main GUI window
window = Tk()
window.title("Scraper Tool")

# Apollo and LinkedIn frames
apollo_frame = Frame(window)
apollo_frame.pack(side=LEFT, padx=10, pady=10)

linkedin_frame = Frame(window)
linkedin_frame.pack(side=RIGHT, padx=10, pady=10)

def create_tool_section(frame, tool_name, login_function, scrape_function):
    # User Account Dropdown
    user_account_label = Label(frame, text=f"{tool_name} User Account:")
    user_account_label.pack(pady=5)
    user_account_options = ["-- Select Account --", "Account 1", "Account 2"]  # Replace with actual accounts
    user_account_variable = StringVar(frame)
    user_account_variable.set(user_account_options[0])
    user_account_dropdown = ttk.Combobox(frame, values=user_account_options, textvariable=user_account_variable)
    user_account_dropdown.pack(pady=5)

    # Login Button
    login_button = Button(frame, text="Login", command=lambda: login_function(user_account_variable.get(), url_entry.get(), listname_entry.get(), num_pages_entry.get()))
    login_button.pack(pady=5)

    # URL, List Name, and Pages Input Fields (placed outside the function for shared access)
    global url_entry, listname_entry, num_pages_entry

    url_label = Label(window, text="URL:")
    url_label.pack(pady=5)
    url_entry = Entry(window)
    url_entry.pack(pady=5)

    listname_label = Label(window, text="List Name:")
    listname_label.pack(pady=5)
    listname_entry = Entry(window)
    listname_entry.pack(pady=5)

    num_pages_label = Label(window, text="Number of Pages:")
    num_pages_label.pack(pady=5)
    num_pages_entry = Entry(window)
    num_pages_entry.pack(pady=5)

    # Scrape Button
    scrape_button = Button(frame, text="Scrape", command=lambda: scrape_function(user_account_variable.get(), url_entry.get(), listname_entry.get(), num_pages_entry.get()))
    scrape_button.pack(pady=5)

# Create sections for each tool
create_tool_section(apollo_frame, "Apollo", login_apollo, scrape_apollo)
create_tool_section(linkedin_frame, "LinkedIn Sales Navigator", login_linkedin, scrape_linkedin)

# Separator line
separator = ttk.Separator(window, orient=HORIZONTAL)
separator.pack(fill=X, padx=20, pady=10)

window.mainloop()

