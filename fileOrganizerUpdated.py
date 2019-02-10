#!/usr/python3
import os,sys,string,random,time,signal,re,shutil
import magic
from PIL import Image
from moviepy.editor import VideoFileClip
mode=''
names=[]
prename=''

def scanFiles(keyword):

    imgFiles = []
    vidFiles = []
    gifFiles = []
    othFiles = []
    unrecFiles = []

    global includeopt


    os.system("echo "+'"'+"find . -type f -name "+"*'*"+" | rename 's/ /_/g'"+'"')

    ofiles={}
    for root, directories, filenames in os.walk('.'):
        #print(root,end='\r')
        for filename in filenames:
            if "9351" in filename and includeopt == '0':
                continue
            if not "9351" in filename and includeopt == '1':
                continue
            try:
                if keyword == "":
                    f=os.path.abspath(os.path.join(root,filename))
                    fsz=os.stat(f).st_size
                    if fsz < 10240:
                        continue
                    ofiles[f]=fsz
                elif keyword in filename:
                    f=os.path.abspath(os.path.join(root,filename))
                    fsz=os.stat(f).st_size
                    if fsz < 10240:
                        continue
                    ofiles[f]=fsz
            except Exception as e:
                print(e)

    files = sorted(ofiles.items(),key=lambda x:x[1],reverse=True)

    for fl,sz in files:
        flnm_lower=os.path.basename(fl.lower())

        if ".jpg" in flnm_lower or ".png" in flnm_lower or ".jpeg" in flnm_lower:
            imgFiles.append(fl)
        elif ".mp4" in flnm_lower or ".avi" in flnm_lower or ".mkv" in flnm_lower or ".mov" in flnm_lower or ".flv" in flnm_lower or ".m4v" in flnm_lower or ".ts" in flnm_lower or ".m2ts" in flnm_lower:
            vidFiles.append(fl)
        elif ".gif" in flnm_lower:
            gifFiles.append(fl)
        elif  ".txt" in flnm_lower or  ".py" in flnm_lower or ".pdf" in flnm_lower or ".ppt" in flnm_lower or ".doc" in flnm_lower :
            othFiles.append(fl)
        else:
            unrecFiles.append(fl)


    files = []


    files.append(imgFiles)
    files.append(gifFiles)
    files.append(vidFiles)
    files.append(othFiles)
    files.append(unrecFiles)



    return files

def choiceFilter(files,ch):

    if ch == 3:
        vidFilter(files)
    elif ch == 4 or ch == 5:
        unFilter(files)
    else:
        imgFilter(files)


def delay(img):

	sz=os.stat(img).st_size/1000
	sl=0
	if sz <= 2000:
		sl=2.35
	elif sz > 2000 and sz <= 5000:
		sl=2.99
	elif sz > 5000 and sz <= 10000:
		sl=5.4
	elif sz> 10000 and sz<=15000:
		sl=6.73
	elif sz > 15000 and sz<30000:
		sl=9.4
	else:
		sl=11.9
	if "gif" in img[0].lower():
		time.sleep(sl+1.5)
	else:
		time.sleep(sl)
	os.system("killall pqiv")



def imgFilterHelper(files):
    
    fls = {}
    for fl in files:
        try:
            tmp = Image.open(fl).size
            sz = tmp[0]
            fls[fl]=sz
        except Exception as e:
            fls[fl]=0

    tmps = sorted(fls.items(),key=lambda x:x[1],reverse=True)

    files=[]
    for fl,_ in tmps:
        print(_)
        files.append(fl)

    return files



def random_generator(size=4, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def imgFilter(files):
    global names
    global prename
    global mode


    files = imgFilterHelper(files)



    ctr=0
    tfls=len(files)
    for img in files:
        os.system("pqiv -c -f '"+img+"' &")
        delay(img)

        if mode == 'r':
            input("press any")
            continue

        ext = "."+magic.from_file(img,mime=True).split('/')[-1]

        exPath=os.path.dirname(img)
        fileName=os.path.basename(img)

        fname=''
        ch='un'
        ctr+=1
        print("\n"+str(ctr)+"/"+str(tfls)+".file:"+fileName)
        print(os.stat(img).st_size/1000)

        if prename == '':
            for actnm in names:
                if actnm[:4] in fileName.lower():
                    print("Found:"+actnm)
                    ch = input("enter to confirm:")
                    if ch == "":
                        fname = actnm
                    if "]]" in ch:
                        print(img+" deleted")
                        os.remove(img)
                    break

            if "]]" in ch:
                continue

            if ch != "" and ch != 'un' :
                for act in names:
                    if ch in act:
                        fname = act

            if fname == "":
                print("fileName not Found")
                fname = input("Enter completeName:")
                if "]]" in fname:
                    print(img+" deleted")
                    os.remove(img)
                    continue
                
                if fname == "":
                    fname = input("Enter to confirm:")
                    if fname == "":
                        print(img+" deleted")
                        os.remove(img)
                        continue
        else:
            fname=prename


        sname = input("Enter partName:")

        if "skip" in sname:
            print("skipping")
            continue

        if "]]" in sname:
            print(img+" deleted")
            os.remove(img)
            continue

        finalName = fname+random_generator()+sname+"_9351_"+ext
        print(finalName)
        shutil.move(img,exPath+"/"+finalName)


def vidFilterHelper(files):
    fls = {}


    for fl in files:
        try:
            clip = VideoFileClip(fl)
            fls[fl]=round(os.stat(fl).st_size/clip.duration,3)
            #fls[fl]=os.stat(fl).st_size
        except Exception as e:
            k=0

    tmps = sorted(fls.items(),key=lambda x:x[1],reverse=True)

    files=[]
    for fl,_ in tmps:
        print(_)
        files.append(fl)

    return files


def vidFilter(files):
    global names
    global prenam
    global mode

    files=vidFilterHelper(files)

    ctr=0
    tfls=len(files)
    for img in files:
        ctr+=1
        os.system("vlc '"+img+"' ")

        if mode == 'r':
            input("press any")
            continue

        ext = "."+magic.from_file(img,mime=True).split('/')[-1]

        exPath=os.path.dirname(img)
        fileName=os.path.basename(img)

        fname=''
        ch = 'un'

        print("\n"+str(ctr)+"/"+str(tfls)+".file:"+fileName)

        if prename == "":
            for actnm in names:
                if actnm[:4] in fileName.lower():
                    print("Found:"+actnm)
                    ch = input("enter to confirm:")
                    if ch == "":
                        fname = actnm
                    if "]]" in ch:
                        print(img+" deleted")
                        os.remove(img)
                    break

            if "]]" in ch:
                continue
            if ch != "" and ch != 'un':
                for act in names:
                    if ch in act:
                        fname = act

            if fname == "":
                print("fileName not Found")
                fname = input("Enter completeName:")

        else:
            fname=prename


        sname = input("Enter partName:")

        if "skip" in sname:
            print("skipping")
            continue


        if "]]" in sname:
            print(img+" deleted")
            os.remove(img)
            continue


        finalName = fname+random_generator()+sname+"_9351_"+ext
        print(finalName)
        shutil.move(img,exPath+"/"+finalName)




def unFilter(files):
    print("you are in:"+os.getcwd())

    dir = input("Enter dirname to create:")

    if not os.path.isdir(os.getcwd()+"/"+dir):
        os.mkdir(dir)
    os.chdir(dir)

    for fl in files:
        try:
            if not os.path.isfile("./"+os.path.basename(fl)):
                shutil.move(fl,"./"+os.path.basename(fl))
            else:
                shutil.move(fl,"./"+random_generator()+os.path.basename(fl))
        except Exception as e:
            print(e)


def filter(files):
    imgs,gifs,vids,oth,unrec = files

    print("\n1.Images\t"+str(len(imgs)))
    print("2.Gifs\t\t"+str(len(gifs)))
    print("3.Vids\t\t"+str(len(vids)))
    print("4.rec_Oth\t"+str(len(oth)))
    print("5.unrec\t\t"+str(len(unrec)))
    print("6.Move Above:")

    ch = int(input("\nEnter choice:"))

    if ch == 6:
        choitem=int(input("\nEnter item:"))
        unFilter(files[choitem-1])
    else:
        choiceFilter(files[ch-1],ch)


def main():

    global names
    global prename
    global includeopt
    global mode

    mode = input("Read-only or modified:")


    with open("/home/vamshi/.actnames.txt",'r') as fl:
        for ln in fl:
            names.append(ln[:-1])

    if len(sys.argv)!= 2:
        dir = input("Enter Full dirname:")
    else:
        dir = os.path.abspath(sys.argv[1])


    if dir == None or dir == "/home/vamshi" or dir == "~/" or dir == "/home/vamshi/" or not os.path.isdir(dir):
        print("passed "+dir+" exiting....")
        sys.exit()

    os.chdir(dir)

    includeopt = input("9351 include(1/0):")
    keyword = input("Enter search term:")

    print("Scanning "+os.getcwd()+"...........\n")

    if "/home/vamshi" == os.getcwd():
        print("passed "+dir+" exiting....")
        sys.exit()

    prename = input("Enter prename:")

    files = scanFiles(keyword)

    filter(files)




if __name__ == '__main__':
    main()
