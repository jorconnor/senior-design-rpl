'''
Created on Feb 8, 2017

@author: Jordan
'''

import copy
from jsondiff import diff
from os import walk
from os.path import exists,splitext
from subprocess import Popen, PIPE
from string import digits

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
        "chsarp" : "cs",
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
        "functions"
        ]

def resolve_input(lang_dir, test,test_dir):
    return test_input.replace("$", lang_dir).replace("&", test_dir) + test

def resolve_base_input(lang_dir,test_dir):
    return test_input.replace("$", lang_dir).replace("&", test_dir)

def resolve_output(lang_dir,test,test_dir):
    test_base = splitext(test)[0]
    return test_output.replace("$", lang_dir).replace("&", test_dir).replace("?",test_base)

def run_tests():
    failures = 0
    testCount = 0
    for dir in tests:
        for lang,alias in langs.items():
            base_path = resolve_base_input(lang,dir)
            for (dirpath, dirnames, test_files) in walk(base_path):
                for test_file in test_files: 
                    resolved_input = resolve_input(lang,test_file,dir)
                    resolved_output = resolve_output(lang,test_file,dir)
                    if not exists(resolved_input): continue
                    if not exists(resolved_output): continue
                    with open(resolved_output, 'r') as vOut:
                        test = splitext(test_file)[0]
                        pattern = copy.copy(test)
                        pattern = pattern.translate(None,digits)
                        proc = Popen('rosie -manifest ' + manifest_file + ' -wholefile -encode json ' + alias + "." + pattern + " " + resolved_input, stdout=PIPE, stderr=PIPE,shell=True)
                        stdout,stderr = proc.communicate()
                        if(stderr != ''): print(stderr)
                        try:
                            diffs = diff(vOut,stdout.replace("\\r",""))
                            if len(diffs) > 0: 
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
    if(failures > 0): exit(1)
            
if __name__ == '__main__':
    run_tests()
