import eel
import csv
import threading

text_file_path = "active_domains.txt"

html_template_path = "index.html"

# Initialize Eel
eel.init("frontend", allowed_extensions=['.js', '.html'])

refreshing = False  # Flag to indicate if refresh is in progress


@eel.expose
def read_domain_data():
    domain_data = []
    with open(text_file_path, 'r') as file:
        lines = file.readlines()
        domain = None
        for line in lines:
            line = line.strip()
            if line:
                if domain is None:
                    domain = line
                else:
                    domain_data.append([domain, line])
                    domain = None

    # Clear the existing domain data
    eel.clearDomains()

    # Load the refreshed domain data
    for domain, expiry_date in domain_data:
        eel.js_addDomain(domain, expiry_date)

    return domain_data


@eel.expose
def get_domain_data():
    domain_data = read_domain_data()
    return domain_data


@eel.expose
def load_domains():
    eel.js_loadDomains(get_domain_data())


def perform_refresh_async():
    global refreshing
    refreshing = True  # Set refreshing flag to True

    # Call the refresh function from fetch_refresh.py
    from fetch_refresh import refresh
    refresh()

    refreshing = False  # Set refreshing flag to False
    load_domains()  # Update the domain data


@eel.expose
def perform_refresh():
    global refreshing
    if not refreshing:
        threading.Thread(target=perform_refresh_async).start()


# Start the Eel app
eel.start(html_template_path, size=(500, 400), suppress_error=True)



