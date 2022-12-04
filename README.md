# 88x31 sized GIFs

Chris Lomont

Dec 2022

Here is a collection of 7304  88x31 gifs that used to be common sized for banner ads and links on the early web. There are also 656 gif that a around this size.

Example:

![Images](art/Images.png)



I removed all that were binary exact files. I have not (yet?) removed ones that are actually the same image frames.

I have not hand checked to remove any NSFW images, even in the example screen shot.

## Notes

I scraped several websites and obtained some github images. These are listed in `scraper.py`, a Python tool that scrapes websites and saves all images (renaming as needed).

Then `cleaner.py` cleans the files through a few steps. Read the code if you're interested.

Excellent gif explorer site http://www.matthewflickinger.com/lab/whatsinagif/gif_explorer.asp

### Steps for code

1. Make venv: `python -m venv venv`
2. Activate venv (on windows, `venv\Scripts\activate`)
3. Install requirements: `pip install -r requrements.txt`
4. get images 
   1. Scraping: `python scraper.py`
   2. git checkout the git repos listed in `scraper.py`
5. clean images: `python cleaner.py` PNG, JPG, and other files converted to gifs, sizes checked, basic checking done
6. Result images in `cleaned` and some subdirectories. `images.html` and `offsize.html` are all the images (too many to view in Chrome)



