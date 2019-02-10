import magic,os,sys,shutil,time
from threading import Thread,active_count
allfiles=[]
def modify(fl):
	ext = "."+magic.from_file(fl,mime=True).split('/')[-1]
	try:
		dst=fl.replace(".","")+ext
		if len(dst) > 50:
			dst=dst[:40]+ext
		shutil.move(fl,dst)
	except Exception as e:
		print(e)
def scan(forcemode):
	global allfiles
	allfiles=[]
	for root,drs,files in os.walk('.'):
		for fl in files:
			lfl = fl.lower()
			if ".zip" in lfl or ".txt" in lfl or ".mp4" in lfl or ".mkv" in lfl or ".ts" in lfl :
				continue
			if forcemode != "":
				allfiles.append(os.path.abspath(os.path.join(root,fl)))
				continue
			if len(lfl) > 5 and lfl[-5] == '.' and len(lfl) <50:
				continue
			if len(lfl.split('.')[-1]) > 5 or len(lfl.split('.')) == 1  or len(lfl) > 50: 
				allfiles.append(os.path.abspath(os.path.join(root,fl)))

def main():
	global allfiles
	if len(sys.argv) < 2 :
		print("pass dir")
		return 
	os.chdir(sys.argv[1])
	forcemode = input("force rename all(y/n):")
	scan(forcemode)

	for fl in allfiles:
		Thread(target=modify,args=(fl,)).start()
		while active_count() > 10:
			time.sleep(1)

if __name__ == "__main__" :main()
