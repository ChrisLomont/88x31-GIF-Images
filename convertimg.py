from os import walk
from PIL import Image
import copyimgs

def convertImg(srcpath,dstpath,file):
    try:
        # input file to convert
        src = f'{srcpath}\{file}'
        
        # where to put temp copy of converted file
        f2 = file.replace('.jpg','.gif').replace('.png','.gif')
        temppath = f'{srcpath}\{f2}'
        
        # convert image
        img = Image.open(src)
        # jpg has no alpha
        img = img.convert('RGB').convert('P', palette=Image.ADAPTIVE)
        img.save(temppath)


        # smart copy the file to dest
        copyimgs.smart_copy(f2,srcpath,dstpath)

    except Exception:
        print(f'Exception on file {src}')

# naive converter
def convert_to_gif(srcpath,dstpath):
    total = 0
    for (dirpath, dirnames, filenames) in walk(srcpath):
        for file in filenames:
            total = total + 1
            fn = f'{srcpath}\{file}'
            if fn.lower().endswith('.png.gif'):
                continue
            elif fn.lower().endswith('.jpg.gif'):
                continue
            elif fn.lower().endswith('.gif'):
                continue
            elif fn.lower().endswith('.png'):
                convertImg(srcpath,dstpath,file)
            elif fn.lower().endswith('.jpg'):
                convertImg(srcpath,dstpath,file)
            else:
                print(f'file {fn} unknown')
    print(f'{total} images processed')

def convert_to_gif2(path):
    pngCount = 0
    gifCount = 0
    jpgCount = 0
    total = 0
    doSave = False

    for (dirpath, dirnames, filenames) in walk(path):
        for file in filenames:
            total = total + 1
            fn = f'{path}\{file}'
            if fn.lower().endswith('.png.gif'):
                continue
            elif fn.lower().endswith('.jpg.gif'):
                continue
            elif fn.lower().endswith('.png'):
                # http://www.pythonclub.org/modules/pil/convert-png-gif
                pngCount = pngCount + 1
                img = Image.open(fn)
                # img = img.convert('RGBA') # ensure alpha band
                # alpha = img.split()[3]

                # convert image into 

                if img.mode == 'P':
                    assert(img.mode == 'P') # palette based
                    #trans = img.info['transparency']
                    if 'transparency' in img.info:
                        print(fn,"has transparency palette")
                      #  todo - read post to make it work
                    else:
                        #print(fn,"no transparency palette")
                        # png palette, no transparency has no alpha
                        img = img.convert('RGB').convert('P', palette=Image.ADAPTIVE)
                        # save
                        if doSave:
                            img.save(fn+".gif")
                else:
                    if 'transparency' in img.info:
                        # none hit here
                        print(fn,"has transparency no palette")
                    else:
                        #print(fn,"no transparency no palette")
                        # png palette, no transparency has no alpha
                        img = img.convert('RGB').convert('P', palette=Image.ADAPTIVE)
                        # save
                        if doSave:
                            img.save(fn+".gif")

                    

            elif fn.lower().endswith('.gif'):
                gifCount = gifCount + 1
            elif fn.lower().endswith('.jpg'):
                jpgCount = jpgCount + 1
                img = Image.open(fn)
                # jpg has no alpha
                img = img.convert('RGB').convert('P', palette=Image.ADAPTIVE)
                # img.save(fn+'.gif')
            else:
                print(f'file {fn} unknown')
    print(f'{pngCount} png, {gifCount} gif, ,{jpgCount} jpg, {total} total')
