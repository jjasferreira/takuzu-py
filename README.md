# takuzu-py

IST Artificial Intelligence course's project (LEIC-A 2021/2022)

A program that solves the Takuzu problem using A.I. search techniques in Python 3.8

Made by [João Cardoso](https://github.com/joaoncardoso) and [José João Ferreira](https://github.com/jjasferreira)

---

## How to run tests with the `test.sh` script

```
./test.sh [flags] <path_to_takuzu.py> <path_to_tests>
```

- `-d` flag shows in the terminal the "diff" of expect output with actual output
- `-c` flag removes generated `.result` files (instead of testing)
- `-h` flag (as usual) shows this information

### Example

```bash
./test.sh -d takuzu.py tests
```

In addition to the tests in this _repo_, you can find more and their respective results [_here_](https://github.com/diogotcorreia/proj-ist-unit-tests/tree/master/ia/2021-2022/custom-tests)

---

## Formatting

In order to keep consistency in this project, we use [`black`](https://github.com/psf/black) as a code formatter for Python files.

Alternatively, for the Markdown ones, we use [`prettier`](https://github.com/prettier/prettier).
