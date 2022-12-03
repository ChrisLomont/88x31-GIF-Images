import os
from os import walk
import imagesize # quick image sizer
from os import walk
import shutil

def isImage(filename):
    ok1 = filename.lower().endswith('.gif')
    ok2 = filename.lower().endswith('.png')
    ok3 = filename.lower().endswith('.jpg')
    ok4 = filename.lower().endswith('.jpeg')
    return ok1 or ok2 or ok3 or ok4

# ensure dir exists
def ensure_dir(path):
    if not os.path.exists(path):  
        os.makedirs(path)

# copy, rename if needed
# create dir if missing
# rename .jpeg to .jpg
def smart_copy(file,srcpath,destpath):
    # PREFIX_... stuff cleaned up better
    src = f'{srcpath}\{file}'

    # clean PREFIX repeats
    f2 = file
    pcount =0
    while f2.startswith("PREFIX_"):
        f2 = f2.replace("PREFIX_","")
        pcount = pcount + 1
    if pcount>0:
        f2 = f'PREFIX_{pcount}_'

    dst = f'{destpath}\{f2}'
    if not '.' in dst:
        dst = dst + '.gif' # assume
    # print(f"copy {src} to {dst}")

    ensure_dir(destpath)

    i = 0
    while os.path.exists(dst):
        dst = f'{destpath}\PREFIX_{i}_{file}'
        i = i + 1
        # print(f"ERROR: now copy {src} to {dst}")

    if dst.lower().endswith('.jpeg'):
        dst = dst.replace('.jpeg','.jpg')

    shutil.copyfile(src,dst)

# copy all that meet criteria to final directory
#  subdirs for offize
#  each gets notgif for not gif flavored items
def copy(dest, paths):
    sizeok = 0 # 88x31
    offsize = 0 # not 88x31
    notgif = 0 # not gif
    total = 0 # total files
    
    for path in paths:
        print("copy from path",path,"to path",dest)
        for (dirpath, dirnames, filenames) in walk(path):
            for file in filenames:
                #if not file.startswith('PREFIX_'):
                #    continue

                if  '.' in file and not isImage(file):
                    if not file.startswith('PREFIX_'):
                        print(file)
                    continue

                total  = total + 1
                
                destpath = dest # local per pass copy, adds bad and other

                # check size
                w,h = imagesize.get(f'{dirpath}\{file}') 
                #if w != 88 or h != 31:
                #    print(f'{fn} has size not 88x31: {w}x{h}')
                # other common sizes: 85x31, 59x31, 88x28, 88x30, 76x31, 100x40, etc...
                if w==88 and h==31:
                    sizeok = sizeok + 1
                elif w < 44 or 110 < w or h < 20 or 60 < h:
                    #print(f'file {file} copied to bad dir for size {w}x{h}')
                    offsize = offsize + 1
                    continue # dont copy file
                else:
                    # bad size, will go here
                    destpath = destpath + '/offsize'

                if not file.lower().endswith('.gif'):
                    destpath = destpath + '/notgif'
                    notgif = notgif + 1

                smart_copy(file,dirpath,destpath)

    print(f'{total} files, {sizeok} size ok, {offsize} bad sized, {notgif} not gifs')
