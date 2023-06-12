To use the image display, you need to have parameters.json file present in the folder and it's structure needs to be

- json["image_urls"][<specify url with list index>]["url"] -> String

(Optional specify the amount of images you want to loop through with json["display_amount"] -> Int

Example: 
{
  "image_urls": [
    {
      "url": <address here as string>
    }
  ],
  "display_amount": 12
}

