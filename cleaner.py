# clean images in dirs
# 1. png, etc. to gif
# - merge various image dirs into one
# 2. dups removed, merged, naming?
#    similar ones?
#    size changes same/similar?
# - trim some?
# - dups with PREFIX coding - clean, rename?
# - sort on size, move non-standard ones out. or fix them?

# numbers: # files, sizes, before after cleaning
# make massive webpage with all?
# make webpage with errors/ merges/ etc?

import os
import shutil
from os import walk
import imagesize # quick image sizer
from PIL import Image


# our code
import copyimgs
import convertimg
import removedups



# write html page with all images in given directory
def to_html(htmlname, path):
    with open(f'{htmlname}.html', 'w') as f:
        for (dirpath, dirnames, filenames) in walk(path):
            f.write('<!DOCTYPE html><html><body style="background-color:black;>"\n')
            for file in filenames:
                f2 = f'{path}\{file}'
                #w,h = imagesize.get(f2)
                #if w==88 and h==31:
                f.write(f'<img src="{f2}" title="{f2}"  />\n')
            f.write('</body></html>\n')

# check for files. Directories ok to have
def isEmpty(path):
    for (dirpath, dirnames, filenames) in walk(path):
        if len(filenames)>0:
            return False
    return True

# where files go, subdirs are errors and workspaces
dest = "cleaned"

def copy():
    # ensure empty
    if not isEmpty(dest):
        print(f'ERROR: ensure directory "{dest}" is empty')
        exit()

    # 1. copy all to one place
    # only run this once, else delete directories dest and 'bad'
    copyimgs.copy(dest,["88x31","88x31s","images"])


def convert():
    # 2. convert remaining PNG, jpg, to gif
    convertimg.convert_to_gif(dest+'/notgif',dest)
    convertimg.convert_to_gif(dest+'/offsize/notgif',dest+'/offsize')


# 3. remove bitwise identical files
def remove():
    removedups.process_dups(dest)
    removedups.process_dups(dest+'/offsize')

copy()
convert()    
remove()    

# todo 
# 4. look for same image: 
#  - png and 1 frame gif
#  - what if images similar? how to output?

#remove_dup_imagery(dest)
# readImages('bad')


# make html
to_html('images',dest)
to_html('offsize',dest+'/offsize')

