from subprocess import call, check_output, CalledProcessError
import os
import shlex

gens = {
    'C++': 'hyena-cpp/build/bin/gen_test_out',
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
    counters = {'passed': 0, 'failed': 0}
    generator = get_generator(lines[0])
    verifier = get_verify(lines[0])
    for line in lines[1:]: # first line is used to get generator and verifier
        raw_input, output = line.split("->")
        input = shlex.split(raw_input)
        output = output.strip()
        try:
            call([generator, "-o", "output.bin"] + input, stdout=DEVNULL)
            ver = check_output([verifier, "output.bin"], universal_newlines=True).strip()
        except CalledProcessError as e:
            print(FAIL + ": input " + raw_input)
            print(FAIL + ": " + str(e))
            counters['failed'] += 1
            continue
        if ver == output:
            counters['passed'] += 1
            print("{2}: {0}  --->  {1}".format(raw_input, output, PASS))
        else:
            counters['failed'] += 1
            print("{2}: {0}  --->  {1}".format(raw_input, output, FAIL))
            print("\tExp '{0}'".format(output))
            print("\tGot '{0}'".format(ver))
    print("\nRun {0} tests, {1} passed, {2} failed".format(len(lines[1:]), counters['passed'], counters['failed']))

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 run_test_script.py <test_scipt>")
        sys.exit(1)
    script = sys.argv[1]
    run_script(script)
