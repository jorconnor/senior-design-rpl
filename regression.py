'''
Created on Feb 8, 2017

@author: Jordan
'''

import json
import tempfile
from jsondiff import diff
import os
from subprocess import call

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
          "dependencies" : "dependencies"
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
            #matcher = diff_match_patch()
            resolved_input = resolve_input(lang,alias,test,dir)
            resolved_output = resolve_output(lang,test,dir)
            if not os.path.exists(resolved_input): continue
            if not os.path.exists(resolved_output): continue
            try:
                os.remove(out)
            except OSError:
                pass
            with open(resolved_output, 'r') as vOut:
                with open(out, 'w') as tempOut:
                    call(["rosie", "-manifest", manifest_file, "-wholefile", "-encode", "json", alias + "." + test, resolved_input], stdout=tempOut)
                with open(out, "r+") as tempOut:
                    #verified_out = json.dumps(json.loads(vOut.read()).sort())
                    #new_out = json.dumps(json.loads(tempOut.read()).sort())
                    verified_out = json.loads(vOut.read())
                    new_out = json.loads(tempOut.read())
                    #verified_out = sorted(json.loads(vOut.read()))
                    #new_out = sorted(json.loads(tempOut.read()))
                    #print (json.dumps(verified_out))
                    #@print (json.dumps(new_out))
                    # diffs = matcher.diff_main(verified_out,new_out)
                    #if(len(diffs) != 0):
                    diffs = diff(verified_out,new_out)
                    if(len(diffs) > 0): 
                        failures += 1
                        print (test + " test failed for " + lang)
            testCount += 1
            try:
                os.remove(out)
            except OSError:
                pass
    print("-------------------------------------------------")
    print(str(testCount) + " tests ran")
    print(str(failures) + " tests failed")
    print("-------------------------------------------------")
    
            
if __name__ == '__main__':
    run_tests()