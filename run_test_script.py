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

def run_script(filename):
    lines = [l.strip() for l in open(filename).readlines() 
             if not l.strip().startswith("#") and not l.strip() == ""]
    from_lang, to_lang = lines[0].split("->")
    from_lang = from_lang.strip().upper()
    to_lang = to_lang.strip().upper()
    devnull = open(os.devnull, 'w')
    counters = {'passed': 0, 'failed': 0}
    for line in lines[1:]:
        raw_input, output = line.split("->")
        input = shlex.split(raw_input)
        output = output.strip()
        try:
            call([gens[from_lang], "-o", "output.bin"] + input, stdout=devnull)
            ver = check_output([vers[to_lang], "output.bin"], universal_newlines=True).strip()
        except CalledProcessError as e:
            print(FAIL + ": input " + raw_input)
            print(FAIL + ": " + str(e))
            counters['failed'] += 1
            continue
        passed = PASS if ver==output else FAIL
        print("{2}: {0}  --->  {1}".format(raw_input, output, passed))
        if not ver == output:
            counters['failed'] += 1
            print("\tGot '{0}'".format(ver))
        else:
            counters['passed'] += 1
    print("\nRun {0} tests, {1} passed, {2} failed".format(len(lines[1:]), counters['passed'], counters['failed']))

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 run_test_script.py <test_scipt>")
        sys.exit(1)
    script = sys.argv[1]
    run_script(script)
