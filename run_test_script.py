from subprocess import call, check_output, CalledProcessError
import os
import shlex

gens = {
    'C++': ['hyena-cpp/build/bin/gen_test_out'],
    'JAVA': ['java', '-jar', 'hyena-api/build/libs/hyena-api-gentest-0.1-SNAPSHOT.jar']
}

vers = {
    'HYENA': 'hyena-edge/target/debug/parse_msg'
}

GREEN = '\033[92m'
RED = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'

PASS = GREEN + "PASS" + ENDC
FAIL = RED + "FAIL" + ENDC

DEVNULL = open(os.devnull, 'w')

TEST_REPORT = "{2}: {0}  --->  {1}"

class TestStats(object):
    def __init__(self, name, tests, passed = 0, failed = 0):
        self.name = name
        self.tests = tests
        self.passed = passed
        self.failed = failed

    def all_passed(self):
        return self.tests == self.passed

class TestResults(object):
    def __init__(self):
        self.stats = []

    def add(self, stats):
        self.stats += [stats]

    def count(self):
        return sum([s.tests for s in self.stats])

    def failed(self):
        return sum([s.failed for s in self.stats])

    def passed(self):
        return sum([s.passed for s in self.stats])

    def all_passed(self):
        return self.count() == self.passed()

def get_generator(line):
    from_lang, _ = line.split("->")
    return gens[from_lang.strip().upper()]

def get_verify(line):
    _, to_lang = line.split("->")
    return vers[to_lang.strip().upper()]

def is_empty_or_comment(line):
    l = line.strip()
    return l.startswith("#") or l == ""


def run_script(filename):
    lines = [l.strip() for l in open(filename).readlines() if not is_empty_or_comment(l)]
    stats = TestStats(lines[0], len(lines[1:]))
    generator = get_generator(lines[0])
    verifier = get_verify(lines[0])
    for line in lines[1:]: # first line is used to get generator and verifier
        raw_input, output = line.split("->")
        input = shlex.split(raw_input)
        output = output.strip()
        try:
            call([*generator, "-o", "output.bin"] + input, stdout=DEVNULL)
            ver = check_output([verifier, "output.bin"], universal_newlines=True).strip()
        except CalledProcessError as e:
            print(FAIL + ": input " + raw_input)
            print(FAIL + ": " + str(e))
            stats.failed += 1
            continue
        if ver == output:
            stats.passed += 1
            print("{2}: {0}  --->  {1}".format(raw_input, output, PASS))
        else:
            stats.failed += 1
            print("{2}: {0}  --->  {1}".format(raw_input, output, FAIL))
            print("\tExp '{0}'".format(output))
            print("\tGot '{0}'".format(ver))

    return stats

def run_scripts_dir(dir):
    script_files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    test_results = TestResults()
    for script in script_files:
        print("Running {0}".format(script))
        stats = run_script(os.path.join(dir, script))
        test_results.add(stats)

    print("\nRun {0} tests, {1} passed, {2} failed".format(test_results.count(), test_results.passed(), test_results.failed()))
    for stat in test_results.stats:
        print("{0:>16}: {4} {1:3d} tests, {2:3d} passed, {3:3d} failed"
              .format(stat.name, stat.tests, stat.passed, stat.failed,
                      PASS if stat.all_passed() else FAIL))

def dispatch(dir_or_file):
    if not os.path.exists(dir_or_file):
        print("File or directory {0} does not exists".format(dir_or_file))
        print("Usage: python3 run_test_scipt.py <test_script_or_test_dir>")
        exit(1)
    if os.path.isdir(dir_or_file):
        run_scripts_dir(dir_or_file)
    else:
        stats = run_script(dir_or_file)
        print("\nRun {0} tests, {1} passed, {2} failed".format(stats.tests, stats.passed, stats.failed))

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 run_test_script.py <test_scipt_or_test_dir>")
        sys.exit(1)
    script = sys.argv[1]
    dispatch(script)
