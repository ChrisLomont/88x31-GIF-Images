# scrape all GIFs from web page with size 88x31, old school animated logos/ads
# Chris Lomont 2022

import re
import requests
#from bs4 import BeautifulSoup
from bs4 import *
import os
from urllib.parse import urlparse
import imagesize

# given an image link (to local or global image), get an actual url and a filename
def get_items(url,image_link):
    #print(url, image_link)
    # cases: image_link 
    # - ends in file only - then relative to ulr
    # - starts with \ - then on same domain, then path
    # - starts with http:// or https:// is absolute
    # 
    # filename always at end

    # start here, assumes absolute
    image_url = image_link

    has_http = image_link.startswith('https://') or image_link.startswith('http://')
    if not has_http:

        # urlparse (http://bob.org/funk/fred/index.html)
        #  scheme = 'http'
        #  netloc = 'bob.org'
        #  path = funk/fred/index.html
        # use os.path.basename() to get filename from end
        m = urlparse(url)
        #print(m)

        if image_link.startswith('/'):
            # global on site
            image_url = f'{m.scheme}://{m.netloc}{image_link}'
        else:
            # local on site
            head,tail = os.path.split(m.path)
            if not '.' in tail:
                head = head + tail 
            image_url = f'{m.scheme}://{m.netloc}{head}/{image_link}'
    
    # get filename from proper URL        
    a = urlparse(image_url)
    # print(a)
    ap = a.path.replace('//','/') # was getting errors here
    filename = os.path.basename(ap)
    if len(filename)<1:
        print(a)
        raise Exception("bababa")
    #print(image_url, filename)
    #print()
    return image_url, filename

if False:
    get_items("http://bob.com/monkey/index.html","/tom.gif")
    get_items("http://bob.com/monkey/index.html","/images/tom.gif")
    get_items("http://bob.com/monkey/index.html","tom.gif")
    get_items("http://bob.com/monkey/index.html","images/tom.gif")

    get_items("http://bob.com/monkey/index.html","http://funk.org/images/tom.gif")
    get_items("http://bob.com/monkey/index.html","httptom.gif")
    get_items("http://bob.com/monkey/index.html","httpstom.gif")

if False:
    get_items("http://bob.com/monkey/","/tom.gif")
    get_items("http://bob.com/monkey/","/images/tom.gif")
    get_items("http://bob.com/monkey/","tom.gif")
    get_items("http://bob.com/monkey/","images/tom.gif")

if False:
    get_items("http://bob.com/monkey","/tom.gif")
    get_items("http://bob.com/monkey","/images/tom.gif")
    get_items("http://bob.com/monkey","tom.gif")
    get_items("http://bob.com/monkey","images/tom.gif")


# exit()

# same byte values and size
def sameBytes(b1,b2):
    if len(b1) != len(b2):
        return False
    for i in range(len(b1)):
        if b1[i] != b2[i]:
            return False
    return True

def isvalid(url):
	return requests.head(url).status_code < 400

def download_images(url,images, folder_name):
    count = 0
    notgif = 0
    badsize = 0
    print(f"Found {len(images)} images for url {url}")
    #print(images)
    if len(images) != 0:
        for i, image in enumerate(images):
            image_link1 = image["src"]

            try:
                image_url, filename  = get_items(url,image_link1)
            except Exception:
                print(f"get error on {url} {image_link1}")
                continue

            #if not filename.endswith('.gif'):
            #    print(filename,'not a gif')
            #    notgif = notgif + 1
            #    continue

            #valid = isvalid(image_url)
            #print(image_link1, filename, image_url, valid)

            #continue
            print(f'{i+1}/{len(images)} {image_url}')

            r = requests.get(image_url).content

            filename2 = f"{folder_name}/{filename}"

            if os.path.exists(filename2):
                # skip if identical, else rename
                with open(filename2, mode='rb') as file: # b is important -> binary
                    fileContent2 = file.read()
                    if sameBytes(r,fileContent2):
                        print(f'Files identical {filename2}, 2nd ignored')
                        continue
                
                pc = 0
                while os.path.exists(filename2):
                    print("ERROR: file exists!",filename2)
                    filename2 = f"{folder_name}/PREFIX_{pc}_{filename}"
                    pc = pc + 1

            try :
                with open(filename2, "wb+") as f:
                    f.write(r)
                    count += 1

                w,h = imagesize.get(filename2)
                if w != 88 or h != 31:
                    print(f'{filename2} has size not 88x31: {w}x{h}')
                # other common sizes: 85x31, 59x31, 88x28, 88x30, 76x31, 100x40, etc...
                if w < 44 or 110 < w or h < 20 or 60 < h:
                    print('file deleted')
                    badsize = badsize+1
                    os.remove(filename2)

            except Exception:
                print(f'Exception writing file {filename2}')
            

        print(f" {count} images have been downloaded out of {len(images)}, {notgif} were not gifs, {badsize} wrong size")

def scrapePage(url,folder_name):
    # os.mkdir(folder_name)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    images = soup.findAll('img')
    download_images(url,images, folder_name)

pages = [        
    'https://cyber.dabamos.de/88x31/', 
    'https://cyber.dabamos.de/88x31/index2.html',
    'https://cyber.dabamos.de/88x31/index3.html',
    'https://cyber.dabamos.de/88x31/index4.html',
    
    # done
    'https://neonaut.neocities.org/cyber/88x31.html', # done
    'https://yesterweb.org/graphics/buttons.html', # done
    'https://anlucas.neocities.org/88x31Buttons.html', # done
    'https://owlman.neocities.org/OwlMan/Banners/Neocities_Banners.html', # done
    'https://yoohoosearch.neocities.org/neocities-buttons/', # done
    'https://exo.pet/', # done

    # done
    'https://88by31.neocities.org/animals.html',
    'https://88by31.neocities.org/anime.html',
    'https://88by31.neocities.org/awareness.html',
    'https://88by31.neocities.org/drugs.html',
    'https://88by31.neocities.org/extlinks.html',
    'https://88by31.neocities.org/food.html',
    'https://88by31.neocities.org/games.html',
    'https://88by31.neocities.org/holiday.html',
    'https://88by31.neocities.org/misc.html', 
    'https://88by31.neocities.org/moviestv.html',
    'https://88by31.neocities.org/music.html',
    'https://88by31.neocities.org/now.html',
    'https://88by31.neocities.org/places.html',
    'https://88by31.neocities.org/pride.html',
    'https://88by31.neocities.org/sanrio.html',
    'https://88by31.neocities.org/web.html',

    # done    
    'https://web.archive.org/web/19991004165227/http://www.geocities.com/NapaValley/2022/iconhd-s.html',
    'https://web.archive.org/web/19991109052039/http://www.geocities.com/NapaValley/2022/iconhood.html',
    'https://web.archive.org/web/19991109025532/http://www.geocities.com/NapaValley/2022/cities.html',    
    'https://web.archive.org/web/19991004212746/http://www.geocities.com/NapaValley/2022/icons.html',
    'https://web.archive.org/web/19991004063433/http://www.geocities.com/NapaValley/2022/88sf-fan.html',
    'https://web.archive.org/web/19991004035325/http://www.geocities.com/NapaValley/2022/88food.html',
    'https://web.archive.org/web/19991108211615/http://www.geocities.com/NapaValley/2022/88fun.html',
    'https://web.archive.org/web/19991109001831/http://www.geocities.com/NapaValley/2022/88web.html',
    'https://web.archive.org/web/19991109020718/http://www.geocities.com/NapaValley/2022/88x31.html',
    'https://web.archive.org/web/19990129040545/http://www.geocities.com/NapaValley/2022/88x31.html',
]

# also github list - use git clone, get images
# https://github.com/ro1y/88x31s # done
# https://github.com/ktwrd/88x31.git # done

folder = 'images'

for page in pages:
    scrapePage(page,folder)