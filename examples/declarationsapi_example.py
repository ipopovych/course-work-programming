import requests
import json
from time import sleep


def get_dec(id, save=True):
    """
    :param id: declartion number id
    :return: json declaration
    """
    print("Looking for declaration {}".format(id))
    URL = 'http://declarations.com.ua/declaration/' + str(id) + '?format=opendata'
    dec = requests.get(URL).json()
    print("Declaration found") if dec else "Error"
    if save:
        with open("dec" + str(id) + ".json", "w") as fp:
            json.dump(dec, fp)
    return dec


def find_dec(keyword, page, save=True):
    """
    :param keyword: keyword request for search
    :param page: page to search for
    :return: json declaration
    """
    print("Looking for declaration with '{}' keyword at page {}".format(keyword, page))
    URL = 'http://declarations.com.ua/search?q=' + keyword + '&format=opendata&page=' + str(page)
    dec = requests.get(URL).json()
    print("Declaration found") if dec else "Error"
    if save:
        with open("dec" + keyword + ".json", "w") as fp:
            json.dump(dec, fp)
    return dec


def find_all(save=True):
    """
    :return: list of json declarations
    """
    data = []
    print("Fetching page #1")

    r = requests.get("http://declarations.com.ua/search?format=opendata").json()
    data += r["results"]["object_list"]

    for page in range(2, r["results"]["paginator"]["num_pages"] + 1):
        sleep(0.5)
        print("Fetching page #{}".format(page))

        subr = requests.get(
            "http://declarations.com.ua/search?format=opendata&page=%s" % page).json()
        data += subr["results"]["object_list"]

    print("Declarations exported {}".format(len(data)))
    if save:
        with open("alldecs.json", "w") as fp:
            json.dump(data, fp)
    return data


dec1 = get_dec(5210)
# Now dec1 is a dictionary with declaration 5210, it is saved as json file
print(type(dec1))
print(dec1)

dec2 = find_dec("Президент", 1, save=False)
# Now dec2 contains results of thw 1st page for "Президент" search
# It is not saved
print(dec2)

# it will take time....
declarations = find_all(save=True)
# Now all declarations are saved as json file
