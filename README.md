# Hyena protocol tests

Here's where unit tests for Hyena protocol are. There is a single Python file that processes 
tests scripts. This repository depends on `hyena-engine`, `hyena-cpp` and `hyena-app` for binaries 
for generating tests output (serialized messages) and verifying the messages.

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


## Hyena verifier

Hyena verifier `parse_msg` parses a serialized Hyena request and outputs the result. It takes a single parameter, the 
file with serialized request.

For example, when using output from the example of C++ generator (see above), `parse_msg lala.bin` would output the folowing:
`Insert {source: 321, timestamps: #10, columns: [3: I8Dense #10 ]}`. It should be read as: the file contains an Insert request
for source 321, containing 10 timestamps and a single column with id 3, type I8Dense and 10 data items.
