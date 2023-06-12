To use the image display, you need to have Parameters.json file present in the folder and it's structure needs to be

- json["image_urls"][<specify url with list index>]["url"] -> String

(Optional specify the headers and amount of images you want to loop through)

Example: 
{
  "image_urls": [
    {
      "url": <address here as string>
    }
  ],
  "display_amount": 12,
  "headers": <headers here as string>
}

