
def processImage(infile):

    try :
        img = Image.open(infile)
        img = img.convert('RGBA')
        return img.tobytes()
    except:
        print("exception for",infile)
        return bytes(0)


    """
    print('process',infile)
    try:
        im = Image.open(infile)
    except IOError:
        print("Cant load", infile)
        raise Exception('cannot read....')

    i = 0
    mypalette = im.getpalette()

    try:
        while 1: # gif frames?
            im.putpalette(mypalette)
            new_im = Image.new("RGBA", im.size)
            new_im.paste(im)
            # new_im.save('foo'+str(i)+'.png')

            i += 1
            im.seek(im.tell() + 1)

    except EOFError:
        pass # end of sequence
    """
# FNV1 hash
FNV_32_PRIME = 0x01000193
FNV_64_PRIME = 0x100000001b3

FNV0_32_INIT = 0
FNV0_64_INIT = 0
FNV1_32_INIT = 0x811c9dc5
FNV1_32A_INIT = FNV1_32_INIT
FNV1_64_INIT = 0xcbf29ce484222325
FNV1_64A_INIT = FNV1_64_INIT
import sys
if sys.version_info[0] == 3:
    _get_byte = lambda c: c
else:
    _get_byte = ord
def fnv(data, hval_init, fnv_prime, fnv_size):
    """
    Core FNV hash algorithm used in FNV0 and FNV1.
    """
    assert isinstance(data, bytes)

    hval = hval_init
    for byte in data:
        hval = (hval * fnv_prime) % fnv_size
        hval = hval ^ _get_byte(byte)
    return hval

def fnv1_32(data, hval_init=FNV1_32_INIT):
    """
    Returns the 32 bit FNV-1 hash value for the given data.
    """
    return fnv(data, hval_init, FNV_32_PRIME, 2**32)


def dumbHash(data):
    return fnv1_32(data)

def image_compare(images):
    print(images)
    for fn in images:
        imageObject = Image.open(fn)
        print('anim',imageObject.is_animated)
        print('frames',imageObject.n_frames)
       

        # Display individual frames from the loaded animated GIF file
        #for frame in range(0,imageObject.n_frames):
        #    imageObject.seek(frame)
        #    imageObject.show()        

def remove_dup_imagery(path):
    """
    # hash first RGBA image frame, find possible same
    fhash = dict()
    for (dirpath, dirnames, filenames) in walk(path):
        for file in filenames:
            fn = f'{dirpath}\{file}'
            #if fn.lower().endswith('.gif'):
            imgBytes = processImage(fn)
            hash = dumbHash(imgBytes)
            fhash.setdefault(hash,[]).append(fn)
    for key,values in fhash.items():
        if len(values)>1:
            image_compare(values)
    todo - needs more work!
    """