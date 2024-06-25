import requests
from bs4 import BeautifulSoup
import hashlib
import base64

#list of URLs to process
urls = ["https://cash.app/", "https://att.com", "https://www.cyberghostvpn.com/", "https://yahoo.com", "https://www.weebly.com/", "https://www.caffeine.tv/", "https://www.humblebundle.com/"]

def get_html(url):
    #get HTML content from URL
    response = requests.get(url)
    if response.status_code == requests.codes.ok:
        return response.text
    else:
        print(f"Error fetching {url}: {response.status_code}")
        return None
    

def extract_sri_tags(html):
    #parse HTML and get elements with integrity attribute
    soup = BeautifulSoup(html, 'html.parser')
    sri_tags = []
    for element in soup.find_all(['script', 'link']):
        if 'integrity' in element.attrs:
            sri_tags.append(element)
    return sri_tags


def get_src_integrity(sri_tags):
    #get src or href with hash
    integrity_info = []
    for element in sri_tags:
        resource_attribute = 'src' if element.name == 'script' else 'href'
        resource_url = element.get(resource_attribute, '')
        if resource_url:
            integrity_info.append({'url': resource_url, 'integrity': element['integrity'], 'type': resource_attribute})
    return integrity_info


def validate_hash(security_info):
    #get hash algo, compute hash and compare
    for info in security_info:
        resource_url = info['url']
        integrity_attr = info['integrity']
        try:
            #extract hash algo
            hash_type, provided_hash = integrity_attr.split('-', 1)
            hash_func = getattr(hashlib, hash_type.lower())

            #get src or href
            response = requests.get(resource_url)
            if response.status_code != requests.codes.ok:
                print(f"Error fetching {resource_url}: {response.status_code}")
                continue

            #compute hash
            content_hash = hash_func(response.content).digest()
            computed_hash = base64.b64encode(content_hash).decode()

            #compare hashes
            if computed_hash == provided_hash:
                print(f"Hash matches for {resource_url}")
            else:
                print(f"Hash mismatch for {resource_url}")
                print(f"Provided hash: {provided_hash}")
                print(f"Computed hash: {computed_hash}")


        except AttributeError:
            #handle unsupported hash algos
            print(f"Unsupported hash type '{hash_type}' for {resource_url}")
        except Exception as error:
            #exception handling
            print(f"Error processing {resource_url}: {str(error)}")


#process urls
for url in urls:
    print(f"Processing {url}")
    html = get_html(url)
    if html:
        sri_tags = extract_sri_tags(html)
        if sri_tags:
            integrity_info = get_src_integrity(sri_tags)
            validate_hash(integrity_info)
        else:
            print(f"No SRI tags found for {url}, check manually")
