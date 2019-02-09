#!/usr/python3
import os,sys

def getDirSize(path):

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
    return sz

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
                dirs[fl]=getDirSize(fl)
            else:
                files[fl]=os.stat(fl).st_size

    print(dirs)

            


def main():

    if len(sys.argv) !=2:
        print("pass dir cmdline")
        sys.exit(1)


    os.chdir(sys.argv[1])

    scanFiles(input("Enter option baseScan or recursive Scan(r/*):"))





if __name__ == "__main__":
    main()