# Prime numbers grammar CSG generator and checker

## This program use LBA to make prime number context-sensitive grammar and check it

### Step 1

#### To generate context-sensitive grammar use command from this holder:

```
python ./src/csg_generator.py
```

#### The following default arguments will be used here:

```
LBA_PATH = ./data/lba.txt
GRAMMAR_PATH = ./data/csg.txt
```

#### To generate context-sensitive grammar with specific arguments use:

```
usage: csg_generator.py [-h] [-lba LBA_PATH] [-g GRAMMAR_PATH]

optional arguments:
  -h, --help            show this help message and exit
  -lba LBA_PATH, --lba_path LBA_PATH
                        Path to lba file
  -g GRAMMAR_PATH, --grammar_path GRAMMAR_PATH
                        Output grammar path
```

### Step 2

#### To check if number is prime or not in prime number context-sensitive grammar use command from this holder:

```
python ./src/prime_checker.py [N]
N is a number to check
```

#### Samples

```
python ./src/prime_checker.py 31
31 is a prime number
```

OR

```
python ./src/prime_checker.py 128
128 is not a prime number
```

#### You can also specify path to prime number context-sensitive grammar:

```
python prime_generator.py [GRAMMAR_PATH] [NUMBER]
```

As shown above, the default argument is:

```
GRAMMAR_PATH = ./data/csg.txt
```

### Number deriving in context-sensitive grammar log:

```
LOG_PATH = ./data/check_log.txt
```