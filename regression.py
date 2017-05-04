'''
Created on Feb 8, 2017

@author: Jordan
'''

import copy,json
from os import walk
from os.path import exists,splitext
from subprocess import Popen, PIPE
from string import digits
import difflib
import sys

testfiles = "./testfiles/"
basic_path = testfiles + "$"
test_input = testfiles + "$" + "/input/&/"
test_output = testfiles + "$" + "/output/&/?.json"
manifest_file = "./MANIFEST"
out = "./test.json"

langs = { 
        "java" : "java",
        "c" : "c",
        "cpp" : "cpp",
        "csharp" : "cs",
        "go" : "go",
        "javascript" : "js",
        "ruby" : "rb",
        "r" : "r",
        "bash" : "b",
        "vb" : "vb"
        }

tests = [ 
        "comments",
        "dependencies",
        "functions",
        "classes",
        "structs",
        ]

def resolve_input(lang_dir, test,test_dir):
    return test_input.replace("$", lang_dir).replace("&", test_dir) + test

def resolve_base_input(lang_dir,test_dir):
    return test_input.replace("$", lang_dir).replace("&", test_dir)

def resolve_output(lang_dir,test,test_dir):
    test_base = splitext(test)[0]
    return test_output.replace("$", lang_dir).replace("&", test_dir).replace("?",test_base)

class HtmlPrinter:
    
    def __init__(self,id):
        self.ts = id
        self.file=open("./result" + str(self.ts) + ".html", 'w')
        
    def add_table(self,test,html):
        self.file.write("<h1>" + test + "</h1>")
        self.file.write(html)
        
    def close(self):
        self.file.close()

def run_tests():
    failures = 0
    testCount = 0
    printer = HtmlPrinter(sys.argv[1])
    for dir in tests:
        for lang,alias in langs.items():
            base_path = resolve_base_input(lang,dir)
            for (dirpath, dirnames, test_files) in walk(base_path):
                for test_file in test_files: 
                    resolved_input = resolve_input(lang,test_file,dir)
                    resolved_output = resolve_output(lang,test_file,dir)
                    if not exists(resolved_input): continue
                    if not exists(resolved_output): continue
                    with open(resolved_output, 'rU') as vOut:
                        test = splitext(test_file)[0]
                        pattern = copy.copy(test)
                        pattern = pattern.translate(None,digits)
                        proc = Popen('rosie -manifest ' + manifest_file + ' -wholefile -encode json ' + alias + "." + pattern + " " + resolved_input, stdout=PIPE, stderr=PIPE,shell=True)
                        stdout = ''
                        stderr = ''
                        for line in proc.stdout: stdout += line
                        for line in proc.stderr: stderr += line
                        if(stderr != ''): print(stderr)
                        try:
                            json1 = json.loads(vOut.read())
                            json2 = json.loads(stdout)
                            jsonOut1 = json.dumps(json1,indent=2, sort_keys=True)
                            jsonOut2 = json.dumps(json2,indent=2, sort_keys=True)
                            if jsonOut1 != jsonOut2:
                                differ = difflib.HtmlDiff()
                                printer.add_table(lang + " : " + test, ''.join(differ.make_file(jsonOut1.splitlines(True),jsonOut2.splitlines(True))))
                                failures += 1
                                print("-------------------------------------------------")
                                print (test + " test failed for " + lang)
                        except ValueError:
                            failures += 1
                            print("-------------------------------------------------")
                            print (test + " test failed for " + lang)
                    testCount += 1
    print("-------------------------------------------------")
    if(testCount == 1):
        print(str(testCount) + " test ran")
    else:
        print(str(testCount) + " tests ran")
    if(failures == 1):
        print(str(failures) + " test failed")
    else:
        print(str(failures) + " tests failed")
    print("-------------------------------------------------")
    printer.close()
    if(failures > 0): exit(1)
    
            
if __name__ == '__main__':
    run_tests()
