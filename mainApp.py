#!/usr/python3
import os,sys
import magic

filesType=''

def checkFile(fl):
    fl=fl.lower()
    if filesType == "img":
        if ".jpg" in fl or ".jpeg" in fl or ".png" in fl:
            return True
    elif filesType == "gif":
        if ".gif" in fl:
            return True
    elif filesType == "vid":
        if ".mkv" in fl or ".mp4" in fl or ".avi" in fl or ".flv" in fl or ".mov" in fl or ".m4v" in fl or ".ts" in fl or ".m2ts" in fl: 
            return True
    return False
def getDirSizeAndFiles(path):

    sz = 0
    files={}
    for root,drs,fls in os.walk(path):
            for fl in fls:
                if checkFile(fl) or filesType == "":
                    try:
                        fullfl=os.path.abspath(os.path.join(root,fl))
                        tmpsz=round(os.stat(fullfl).st_size/(1024),4)
                        files[fullfl]=tmpsz
                        sz+=tmpsz
                    except Exception as e:
                        print(e)
    files = sorted(files.items(),key=lambda x:x[1],reverse=True)
    return [sz,files]


def scanFiles(path):


    files={}
    dirs={}
    outfiles={}
    print("in dir:"+path)
    os.chdir(path)
  
    for fl in os.listdir("."):
        if os.path.isdir(fl):
            dirs[fl]=getDirSizeAndFiles(fl)
        else:
            if checkFile(fl) or filesType=="":
                outfiles[fl]=os.stat(fl).st_size



    sortedDirs = sorted(dirs.items(),key=lambda x:x[1][0],reverse=True)
    sortedOutFiles = sorted(outfiles.items(),key=lambda x:x[1],reverse=True)

    outerctr=0

    

    printDirs={}

    index=1
    for dr,sz in sortedDirs:
        outerctr+=1
        if outerctr == 10:
            break
        print(str(index)+" "+dr+" "+str(sz[0]))
        printDirs[index]=dr
        index+=1
        ctr=0
        for fl,flsz in sz[1]:
            print("\t"+str(index)+" "+fl+" "+str(flsz))
            printDirs[index]=fl
            index+=1
            ctr+=1
            if ctr == 10:
                break
    ctr=0
    for otfl,otsz in sortedOutFiles:
        print(str(index)+" "+otfl+" "+str(otsz))
        printDirs[index]=otfl
        index+=1
        ctr+=1
        if ctr == 10:
            break

    option = int(input("Enter option:"))

    if option == 0:
        return ".."



    selectedOption=printDirs[option]

    if os.path.isdir(selectedOption):
        print("returning "+selectedOption)
        return selectedOption
    else:
        playMedia(selectedOption)
    
    return ""

def playMedia(fl):
    ext = magic.from_file(fl,mime=True).split('/')[-1]

    if "jpeg" == ext or "png" ==ext or "gif" == ext or "jpg" == ext:
        os.system("pqiv -c -f '"+fl+"' ")
    else:
        os.system("vlc '"+fl+"' ")
    return




def main():

    global filesType

    if len(sys.argv) !=2:
        print("pass dir cmdline")
        sys.exit(1)


    os.chdir(sys.argv[1])


    filesType = input("Enter fileType(img/gif/vid/*):")

    path="."
    while True:
        drfl=scanFiles(path)
        if drfl == "":
            path="."
        else:
            path=os.path.abspath(os.path.join(os.getcwd(),drfl))





if __name__ == "__main__":
    main()