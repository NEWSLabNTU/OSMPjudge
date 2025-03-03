# OSMPjudge
A judge to grade all submission and collect results.

## Note
1. This is the judge for MP0 only. Please modify this code to create judges for other MPs and contribute.
2. The script is written in python 2 as the container only have python 2.
3. MP0 requires the submitted zip file to have the following structure:
   
    ```
    <student_id>
    |
    +-- mp0.c
    |
    +-- Makefile
    ```

   If the top directory is not named after student_id(both NTU or NTNU accepted), or file not included in a directory, a hint to deduct 10 points will appear in the student's `result.txt`.
4. If any error occurs during grading, the judge continue to the next students and warn you in the terminal. You may have to grade them manually.

## Usage
We take **MP0** as example. Please contribute and create other branches for other MPs if necessary.

### Unzip mp0
```bash
unzip mp0.zip
cd mp0
# suppose you have xv6/ here
```

### Prepare students' submission files
Download all submission from NTU COOL. Unzip it to `mp0/submissions`.
```bash
mkdir submissions
unzip [downloaded_file.zip] -d submissions 
```
The result shoud look like follows.
```bash
ls submissions
b12345678#_王小明_XXX_XXX_XXX.zip
...
```

### Clone `judge.py` under `mp0/` and prepare private testcase
Clone `judge.py` under `mp0/` and prepare private testcase.

### Enter docker
Note that we mount `mp0/` in the container here, not `xv6/`.
```bash
docker run --rm -it -v "$(pwd)":/home/os_mp0/mp0 -w /home/os_mp0/mp0 ntuos/mp0
```

### Start the judge
```bash
python judge.py  # python 2
```
`results/` will be created, with each student's grading result inside.
It starts with logging look like:
```
Grading r12345678#_王小明 (WANG, HSIAO-MING)_xxxxxx_xxxxxxx_mp0_r12345678.zip
Score for r12345678#_王小明 (WANG, HSIAO-MING)_xxxxxx_xxxxxxx_mp0_r12345678.zip: Score: 90/100
```
And you can view all results and all error in `results/summary.txt` and `results/error.txt`.
