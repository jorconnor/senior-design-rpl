'''
Created on Feb 8, 2017

@author: Jordan
'''

import json
import tempfile
from jsondiff import diff
import os
from subprocess import Popen, PIPE

testfiles = "./testfiles/"
test_input = testfiles + "$" + "/input/&/?.@"
test_output = testfiles + "$" + "/output/&/?.json"
manifest_file = "./MANIFEST"
out = "./test.json"

langs = { "java" : "java",
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

tests = { 
          "line_comments" : "comments",
          "block_comments" : "comments",
          "dependencies" : "dependencies",
          "functions" : "functions"
        }

def resolve_input(lang_dir, lang_alias, test,test_dir):
    return test_input.replace("$", lang_dir).replace("&", test_dir) .replace("?",test).replace("@", lang_alias)

def resolve_output(lang_dir,test,test_dir):
    return test_output.replace("$", lang_dir).replace("&", test_dir) .replace("?",test)

def run_tests():
    failures = 0
    testCount = 0
    for test,dir in tests.items():
        for lang,alias in langs.items():
            resolved_input = resolve_input(lang,alias,test,dir)
            resolved_output = resolve_output(lang,test,dir)
            if not os.path.exists(resolved_input): continue
            if not os.path.exists(resolved_output): continue
            with open(resolved_output, 'r') as vOut:
                proc = Popen('rosie -manifest ' + manifest_file + ' -wholefile -encode json ' + alias + "." + test + " " + resolved_input, stdout=PIPE, stderr=PIPE, shell=True)
                return_code = proc.wait()
                stdout,sterr = proc.communicate()
                if(sterr != ''): print(sterr)
                try:
                    verified_out = json.loads(vOut.read())
                    new_out = json.loads(stdout)
                    diffs = diff(verified_out,new_out)
                    if(len(diffs) > 0 or return_code != 0): 
                        failures += 1
                        print("-------------------------------------------------")
                        print (test + " test failed for " + lang)
                except ValueError:
                    failures += 1
                    print("-------------------------------------------------")
                    print (test + " test failed for " + lang)
            testCount += 1
    print("-------------------------------------------------")
    print(str(testCount) + " tests ran")
    print(str(failures) + " tests failed")
    print("-------------------------------------------------")
    if(failures > 0): exit(1)
            
if __name__ == '__main__':
    run_tests()