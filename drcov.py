"""
Auto cov collect
@author: Xu Hanyu

use drrun to collect cov file at current path
edit the command in the source code before using
"""

import sys
import os

if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], "\corpus_path")
else:
    testcases = []
    folder = str(sys.argv[1])
    sum = 0
    for root, dirs, files in os.walk(folder, topdown=False):
        for name in files:
            if True:
                # if name.endswith(".xml"):
                testcase = os.path.abspath(os.path.join(root, name))
                testcases.append(testcase)
                sum += 1

    i = 1
    for testcase in testcases:
        print("\n[", i, "of", sum, "] Running DynamoRIO for testcase: ",
              testcase)
        os.system(
            "DynamoRIO\\bin32\\drrun.exe -t drcov -- msxml.exe %s"
            % testcase) # Remember to change this command to adapt
        i += 1
