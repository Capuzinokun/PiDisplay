import requests
import json
import random
from PIL import Image
from io import BytesIO
import re

class DataHandler:

    def __init__(self):
        self.images_file_path = 'Images.json'
        self.parameter_file_path = 'Parameters.json'
        self.image_urls = []
        self.loaded_images = []
        self.display_amount = 5

    def load_images(self):
        self.loaded_images = []
        for url in self.image_urls:
            response = requests.get(url)
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            self.loaded_images.append(img)
        return

    def get_images(self, data):
        self.image_urls = []
        body = data["posts"]
        random.shuffle(body)
        for child in body[:self.display_amount]:
            if child["file"]["url"] is not None:
                self.image_urls.append(child["file"]["url"])

    def write_data(self, data, file_path):
        with open(file_path, 'w', encoding="utf-8") as file:
            # Write the JSON data to the file
            json.dump(data, file, ensure_ascii=False)

        print('JSON data written to', file_path)
        
    def fetch_images(self):
        with open(self.parameter_file_path, 'r', encoding="utf-8") as file:
            data = json.load(file)
            images_url = data["image_urls"][0]["url"]
            self.display_amount = data["display_amount"]
            
        print(images_url)
        
        headers = None
        if "headers" in data:
            headers = json.loads(data["headers"].replace("'", '"'))
        
        response = requests.get(images_url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            
            clean_data = {}
            for key, value in data.items():
                if isinstance(value, str):
                    # Remove emojis
                    value = value.encode('ascii', 'ignore').decode('ascii')
                    # Remove non-ASCII characters
                    value = re.sub(r'[^\x00-\x7F]+', '', value)
                clean_data[key] = value
            
            # Process and use the data as needed
            self.write_data(data, self.images_file_path)
        else:
            print('Error occurred:', response.status_code)
            with open(self.images_file_path, 'r', encoding="utf-8") as file:
                data = json.load(file)
                
        self.get_images(data)