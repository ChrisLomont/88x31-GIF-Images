import os
from os import walk

# same byte values and size
def sameBytes(b1,b2):
    if len(b1) != len(b2):
        return False
    for i in range(len(b1)):
        if b1[i] != b2[i]:
            return False
    return True


# given a list, return list of those without text and those with text
def removeList(items,txt):
    good = []
    bad = []
    for n in items:
        if txt in n.lower():
            bad.append(n)
        else:
            good.append(n)
    return good,bad

# given a list, return list of shortest one and rest
def takeShortest(items):
    lo = items.copy()
    hi = []

    while len(lo)>1:
        if len(lo[0])<=len(lo[1]):
            hi.append(lo[1])
            lo.remove(lo[1])
        elif len(lo[0])>len(lo[1]):
            hi.append(lo[0])
            lo.remove(lo[0])

    return lo,hi


# preferred name from list of same names, and list of bad names
def splitNames(names):
    # those with and without prefix
    good1,bad1 = removeList(names,'PREFIX_')

    good2,bad2 = removeList(good1,'button')

    good3, bad3 = takeShortest(good2)

    good = good3
    bad = bad1 + bad2 + bad3

    # if all were bad, pull shortest back out to good
    if len(good) == 0:
        good,bad = takeShortest(bad)
    
    # sanity checks
    if len(bad) == len(names):
        #print('good',good)
        #print('bad',bad)
        raise Exception('too many bad names')

    if len(bad) +1 != len(names):
        #print('good',good)
        #print('bad',bad)
        raise Exception('too many good names')
    
    return good[0],bad

# remove identical files, recurses on list of same size files
# return number removed
def remove_dups(files):
    if len(files)<2:
        return 0
    
    # find matches to first file
    m = [files[0]]
    with open(files[0], mode='rb') as file: # b is important -> binary
        fileContent1 = file.read()
        for i in range(1,len(files)):
            with open(files[i], mode='rb') as file: # b is important -> binary
                fileContent2 = file.read()
                if sameBytes(fileContent1,fileContent2):
                    m.append(files[i])


    nextFiles = files.copy()
    if len(m)>1:
        goodName,badNames = splitNames(m)
        #print('good name',goodName,'from',m)
        nextFiles.remove(goodName)
        for bad in badNames:
            nextFiles.remove(bad)
        # actually remove files
        for bad in badNames:
            os.remove(bad)
    else:
        nextFiles.remove(m[0])

    # recurse on remaining, track count removed
    return (len(m)-1) + remove_dups(nextFiles)

    # recurse
    # remove_dups()
    




# remove identical files
def process_dups(path):
    remove_count = 0
    filesBySize = dict()
    for (dirpath, dirnames, filenames) in walk(path):
        for file in filenames:
            fn = f'{dirpath}\{file}'
            size = os.path.getsize(fn)
            filesBySize.setdefault(size,[]).append(fn)
    # now for each size, compare all to all
    for key,values in filesBySize.items():
        count = len(values)
        if count > 1:
            size = os.path.getsize(values[0])
            #print(f'len {size} has {count} items')
            remove_count = remove_count + remove_dups(values)
    print(f'{remove_count} files removed')
