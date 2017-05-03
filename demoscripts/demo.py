from pygit2 import clone_repository
from sys import argv,exit
from shutil import rmtree
from os.path import isdir,splitext
from os import walk,getenv
import pylab
from tabulate import tabulate
from time import time
from multiprocessing import Process, Queue
import rosie
from json import dumps


def init_engine(expression):
    ROSIE_HOME = getenv("ROSIE_HOME")
    if not ROSIE_HOME:
    #    print "Environment variable ROSIE_HOME not set.  (Must be set to the root of the rosie directory.)"
        exit(-1)
        
    Rosie = rosie.initialize(ROSIE_HOME, ROSIE_HOME + "/ffi/librosie/librosie.so")
    #print "Rosie library successfully loaded"

    engine = Rosie.engine()
    #print "Obtained a rosie matching engine:", engine, "with id", engine.id

    engine.load_manifest("../MANIFEST")

    config = dumps( {'expression': expression,
                      'encode': 'json'} )
    engine.configure(config)

    engine.inspect()
    return engine

langs = {
        ".java" : "java",
        ".c" : "c",
        ".cpp" : "cpp",
        ".cs" : "cs",
        ".go" : "go",
        ".rb" : "rb",
        ".r" : "r",
        ".b" : "b",
        ".sh" : "b",
        ".vb" : "vb",
        ".h" : "c",
        ".js" : "js",
        ".py" : "py",
        }

features = [ 
        "block_comment",
        "line_comment",
        "dependency",
        "function",
        "class",
        "struct",
        "package",
        ]

rows = ["b", "c", "cpp", "cs", "go", "java", "js", "py", "r", "rb", "vb"]
cols = ["block_comment", "line_comment", "dependency", "function", "class", "struct", "package"]
vals = pylab.zeros((11,8), dtype=object)
for i in range(11):
    vals[i][0] = rows[i]

#url = 'https://github.com/jamiejennings/rosie-pattern-language'

if(len(argv) < 2):
    print "Usage: demo.py <url>"
    exit(2)
url = argv[1]

repo_path = "./repo/"
output =  repo_path + "/output"
if(isdir(repo_path)):
    rmtree(repo_path)
clone_repository(url,repo_path)

def run_thread(file_list,q):
    for f in file_list:
        run_rosie(f,q)
    return 
        
def run_rosie(path,q):
    filename, file_extension = splitext(path)
    print(path)
    engine = init_engine(langs[file_extension] + ".file")
    r = ''
    with open(path, 'r') as f:
        r = dumps(engine.match(f.read(),1))
    for feature in features:
        curCount = r.count("\\\"" + langs[file_extension] + "." + feature + "\\\"")
        row = rows.index(langs[file_extension])
        col = cols.index(feature)
        q.put([row,col,curCount])
    return 

def iterate_over_path(path):
    q = Queue()
    ps = []
    split_files = [[],[],[],[]]
    for path,subdirs,files in walk(path):    
        for i in range(len(files)):
            filename, file_extension = splitext(path+"/"+ files[i])
            if file_extension in langs:
                if(len(split_files[i % 4]) < 50):
                    split_files[i % 4].append(path+"/"+files[i])

    for file_list in split_files:
        ps.append(Process(target=run_thread,args=(file_list,q)))
    for p in ps: p.start()
    for p in ps: p.join()

    while not q.empty():
        tmp = q.get()
        vals[tmp[0]][tmp[1]+1] += tmp[2]
            
bef = time()
iterate_over_path(repo_path)
print(time() - bef)
print tabulate(vals, headers=cols, tablefmt='orgtbl')

    