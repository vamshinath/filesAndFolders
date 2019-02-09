#!/usr/python3
import os,sys

def getDirSizeAndFiles(path):

    sz = 0
    files={}
    for root,drs,fls in os.walk(path):
            for fl in fls:
                try:
                    fullfl=os.path.abspath(os.path.join(root,fl))
                    tmpsz=round(os.stat(fullfl).st_size/(1024),4)
                    files[fullfl]=tmpsz
                    sz+=tmpsz
                except Exception as e:
                    print(e)
    files = sorted(files.items(),key=lambda x:x[1],reverse=True)
    return [sz,files]

def scanFiles(scanOption):

    files={}
    dirs={}

    if scanOption == 'r':
        for root,drs,fls in os.walk("."):
            for fl in fls:
                try:
                    fullpathfl=os.path.abspath(os.path.join(root,fl))
                    print(fullpathfl)
                    files[fullpathfl]=os.stat(fl).st_size
                except Exception as e:
                    k=0
    else:
        for fl in os.listdir("."):
            if os.path.isdir(fl):
                dirs[fl]=getDirSizeAndFiles(fl)
            else:
                files[fl]=os.stat(fl).st_size

    sortedDirs = sorted(dirs.items(),key=lambda x:x[1][0],reverse=True)

    for dr,sz in sortedDirs:
        print(dr,sz[0])
        ctr=0
        for fl,flsz in sz[1]:
            print("\t"+fl+" "+str(flsz))
            ctr+=1
            if ctr == 10:
                break
        
            


def main():

    if len(sys.argv) !=2:
        print("pass dir cmdline")
        sys.exit(1)


    os.chdir(sys.argv[1])

    scanFiles(input("Enter option baseScan or recursive Scan(r/*):"))





if __name__ == "__main__":
    main()