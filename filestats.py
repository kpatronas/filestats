#!/usr/bin/env python
import os,sys, argparse, hashlib, time

pathList = ['/dev','/proc']

def parseArguments():
	parser = argparse.ArgumentParser(description = 'filestats.py: file statistics.')
	# Install packages option
	parser.add_argument('-r', '--recursive',
						help = '-r/--recursive: recursive search',
						action='store_true',
						default = False,
						required = False)
	
	parser.add_argument('-m', '--md5',
						help = '-m/--md5: get md5 hash',
						action='store_true',
						default = False,
						required = False)
						
	parser.add_argument('-b', '--bigger',
						help = '-b/--bigger: add only files bigger than <bigger> bytes',
						type  = int,
						default = 0,
						required = False)
						
	parser.add_argument('-d', '--desc',
						help = '-d/--desc: descending order',
						action='store_true',
						default = False,
						required = False)
	
	parser.add_argument('-p', '--path',
						help = '-p/--path: path to search',
						type  = str,
						default = '/',
						required = False)
	
	parser.add_argument('-n', '--number',
						help = '-n/--number: show top <number> files, "0" to print all',
						type  = int,
						default = 1,
						required = False)
						
	return vars(parser.parse_args())

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def walker(startPath = "/"):
	fslist = []
	fstat  = {}
	args = parseArguments()
	
	recursive 	= args['recursive']
	md5hash 	= args['md5']
	startPath 	= args['path']
	num 		= args['number']
	desc 		= args['desc']
	bigger 		= args['bigger']
	
	for dirpath, dirs, files in os.walk(startPath):
		for f in files:
			try:
				if dirpath not in pathList:
					fileName = '%s/%s'%(dirpath,f)
					if not os.path.islink(fileName):
						
						if md5hash == False:
							fstat = {'name':fileName,
									 'size':os.path.getsize(fileName),
									 'modified':time.ctime(os.path.getmtime(fileName)),
									 'created':time.ctime(os.path.getctime(fileName))}
						else:
							sizeFile = sizeof_fmt(os.path.getsize(fileName))
							fstat = {'name':fileName,
									 'size':os.path.getsize(fileName),
									 'md5':md5(fileName),
									 'modified':time.ctime(os.path.getmtime(fileName)),
									 'created':time.ctime(os.path.getctime(fileName))}
									 
						if bigger > 0 and os.path.getsize(fileName)<bigger:
							pass
						else:
							fslist.append(fstat)
			except:
				pass
		if recursive == False:
			break
	return md5hash,desc, num, sorted(fslist, key=lambda k: k['size'])

if __name__ == '__main__':
	md5hash, desc, num, fileList = walker(startPath = "/")
	llist = []
	try:
		if desc == True:
			if len(fileList) >= num and num!=0:
				llist =  fileList[0:num]
			else:
				llist =  fileList
		else:
			if len(fileList) >= num and num !=0:
				llist = fileList[-num:]
			else:
				llist = fileList
				
		if not md5hash:	
			for i in llist:
				print "F:%s,S:%s,M:%s,C:%s"%(i['name'],sizeof_fmt(i['size']),i['modified'],i['created'])
		else:
			for i in llist:
				print "F:%s,S:%s,M:%s,C:%s,MD5:%s"%(i['name'],sizeof_fmt(i['size']),i['modified'],i['created'],i['md5'])
	except:
		print "No files found in directory"
