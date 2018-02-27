# Hyena protocol tests

Here's where unit tests for Hyena protocol are. There is a single Python file that processes 
tests scripts. This repository depends on `hyena-engine`, `hyena-cpp` and `hyena-app` for binaries 
for generating tests output (serialized messages) and verifying the messages.

## TLDR

Type `make` to run all tests. It will compile all dependencies and than run test scripts. You'll see a line with PASS/FAIL for 
each of the tests, and then a summary not unlike the following:

```
Run 336 tests, 336 passed, 0 failed
    Hyena -> C++: PASS 100 tests, 100 passed,   0 failed
   Hyena -> Java: PASS 100 tests, 100 passed,   0 failed
    C++ -> Hyena: PASS  68 tests,  68 passed,   0 failed
   Java -> Hyena: PASS  68 tests,  68 passed,   0 failed

```

## Script format

### Test header

First non-empty line of the test script defines which binaries are used for generating and verifying tests. It has the format of:

```
[generator] -> [verifier]
```

Both `generator` and `verifier` can have following values: `C++`, `Java` and `Hyena`. The meaning of those is:

* Generator `C++`: use `gen_test_out` from `hyena-cpp` to write serialized requests to a file.
* Generator `Java`: TBD
* Generator `Hyena`: TBD (use `gen_test_out` from `hyena-engine/hyena-api` to write serialized replies to a file.
* Verifier `C++`: use `parse_msg` from `hyena-cpp` to verify Hyena's reply
* Verifier `Java`: TBD (use `TDB` from `hyena-api` to verify Hyena's reply)
* Verifier `Hyena`: use `parse_msg` from `hyena-engine/hyena-api` to verify a request (from C++ or Java).

### Test cases

Every subsequent line contains a test case. It has the following format:

```
[generator arguments] -> [output string]
```

`generator arguments` are passed as argument to the test generator (see below). `output string` is compared with 
the varifier's output.

## C++ generator

`gen_test_out` in `hyena-cpp` is used to create and serialize a valid Hyena request. It takes the following arguments:

```
> hyena-cpp/build/bin/gen_test_out -h
Usage:
 -h|--help                            print this help
 -c|--command <command>               valid command (catalog, columns, addcolumn, insert, scan)
 -o|--output <output>            *    name of a file to put output to
 -n|--column-name <column name>  A  + name of the column
 -t|--column-type <column type>  AI + type of the column
 -r|--rows <number>              I    number of rows to insert
 -s|--source-id <source id>      I    source id
 -i|--id <column id>             IS + id of the column
 -m|--min-ts <min timestamp>     S    lower bound for timestamps
 -x|--max-ts <max timestamp>     S    upper bound for timestamps
 -u|--uuid                       S  + add a random partition uuid
 -l|--filter-column <column id>  S  + column id for a filter
 -f|--filter-type <filter type>  S  + filter type, one of: I8, I16, I32, I64, U8, U16, U32, U64
 -p|--filter-operator <operator> S  + filter operator, one of: LT, LTEQ, EQ, GTEQ, GT, NOTEQ
 -v|--filter-value <value>       S  + filter value
 where:
  + can be repeated
  * applies to all commands
  C applies to catalog command
  L applies to columns command
  A applies to add column command
  I applies to insert command
  S applies to scan command
```

For example:
`-o lala.bin -c insert -s 321 -r 10 -i 3 -t i8dense` serializes an Insert command to `lala.bin` (`-o lala.bin`),
which would insert 10 random rows (`-r 10`) of  signed 8-bit integers (`-t i8dense`) into a dense column number
3 (`-i 3`) as a source id 321 (`-s 321`).

## Java generator 

`GenTest` in `hyena-api` is used to create and serialize a valid Hyena request. It takes similar arguments as C++ generator
([see above](https://github.com/FCG-LLC/hyena-proto-test#c-generator)), and can by run by:

```
java -jar hyena-api/build/libs/hyena-api-gentest-0.1-SNAPSHOT.jar <options>
```

## Hyena generator

`gen_test_out` in `hyena-engine/hyena-api` is used to create and serialize a valid Hyena reply. It takes the following arguments:

```
> target/debug/gen_test_out -h
Protocol test generator 0.1
Generates serialized messages for automated protocol tests.

USAGE:
    gen_test_out [OPTIONS] --command <command> --output <output>

FLAGS:
    -h, --help       Prints help information
    -V, --version    Prints version information

OPTIONS:
    -d, --column-data <column data>...    Number of data rows returned from scan for the column
    -i, --column-id <column id>...        Column id
    -n, --column-name <column name>...    Column name
    -t, --column-type <column type>...    Column type
    -c, --command <command>
            The command [values: columns, catalog, addcolumn, insert, scan, serializeerror]

    -w, --error-param <error param>       Error parameter
    -e, --error-type <error type>         Error type
    -o, --output <output>                 The file to put the serialized message to
    -p, --partition <partitions>          Number of partitions [default: 0]
    -r, --rows <rows>                     Number of inserted rows

```

## Verifiers

Hyena, C++, Java verifiers `parse_msg` parse a serialized Hyena request and output the result. It takes a single parameter, the 
file with serialized request.

For example, when using output from the example of C++ generator (see above), `parse_msg lala.bin` would output the folowing:
`Insert {source: 321, timestamps: #10, columns: [3: I8Dense #10 ]}`. It should be read as: the file contains an Insert request
for source 321, containing 10 timestamps and a single column with id 3, type I8Dense and 10 data items.

Java verifier is run with `java -jar hyena-api/build/libs/hyena-api-parsemsg-0.1-SNAPSHOT.jar <filename>`.
