import sys
import time
import os
import fnmatch
from time import strftime, localtime


# Get timestamp
timestamp = strftime('%Y%m%d%H%M%S', localtime())

# Decide which test to run; All by default
test_suites_with_path = []
for root, dirnames, filenames in os.walk('tests/'):
    for filename in fnmatch.filter(filenames, '*.py'):
        test_suites_with_path.append(os.path.join(root, filename))
if 'tests/' in str(sys.argv):
    test_suites_to_run = [test_suite for test_suite in test_suites_with_path if test_suite in sys.argv]
else:
    test_suites_to_run = 'tests/*'  # everything

# Decide run attribute; all by default
if 'smoke' in str(sys.argv):
    run_attribute = ' -a test=smoke'
if 'positive' in str(sys.argv):
    run_attribute = ' -a test=positive'
else:
    run_attribute = ' -a run=1'

# Decide environment. 'acceptance' by default
if 'prod' in sys.argv:
    env = ' -env=prod'
elif 'test' in sys.argv:
    env = ' -env=test'
else:
    env = ' -env=acceptance'

# Decide verbosity
if 'ver' in sys.argv:
    ver = ' -v'
else:
    ver = ''

# Decide whether to run tests in parallel. Parallel by default$
if any('ser' in args for args in sys.argv):
    par = ''
else:
    par = ' --process-timeout=1000 --process-restartworker --processes=24'

# Run
start = time.time()
# if there are individual suites to be run
if type(test_suites_to_run) == list:
    for test_suite in test_suites_to_run:
        # Run tests
        run_command = 'nosetests ' + run_attribute + ' --nologcapture ' + test_suite + env + ver + par
        os.system(run_command)
else:
    run_command = 'nosetests ' + run_attribute + ' --nologcapture ' + test_suites_to_run + env + ver + par
    os.system(run_command)

time_taken = int(((time.time() - start) / 60))
print ""
if time_taken == 0:
    print "Time taken: less than a minute"
else:
    print "Time taken: about " + str(time_taken) + " minutes"
print ""

# Remove images left behind by failing tests; doing it here to avoid interference during runtime
os.system('rm *.jpg > /dev/null 2>&1')
# Remove compiled files so that tests are not run twice
os.system('find . -name \*.pyc -exec rm {} \; > /dev/null 2>&1')
