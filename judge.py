import os
import re
import shutil
import subprocess
from zipfile import ZipFile

CURRENT_PATH = os.getcwd()
XV6_PATH = os.path.join(".", "xv6")
SUBMISSIONS_PATH = os.path.join(".", "submissions")
RESULT_DIR = os.path.join(".", "results")
RESULTS_BUF = ""
ERR_BUF = ""

NTU_STUDENT_ID_REGEX = r"^[brdt][a-zA-Z0-9]{8}$"
NTNU_STUDENT_ID_REGEX = r"^[4689][a-zA-Z0-9]{8}$"


def grade_individual(zip_file):
    structure_err = True
    student_id = os.path.splitext(zip_file)[0]

    # create result directory for each individual
    result_path = os.path.join(RESULT_DIR, student_id)
    os.mkdir(result_path)
    open(os.path.join(result_path, "result.txt"), "w").close()  # touch equivalent
    open(os.path.join(result_path, "err.txt"), "w").close()  # touch equivalent

    try:
        # extract all files to the result directory
        with ZipFile(os.path.join(SUBMISSIONS_PATH, zip_file), "r") as z:
            z.extractall(path=result_path)
        
        # find the directory name inside the extracted contents
        extracted_contents = os.listdir(result_path)
        dir_name = ""
        guess_dir_name = ""
        for item in extracted_contents:
            if os.path.isdir(os.path.join(result_path, item)):
                if re.match(NTU_STUDENT_ID_REGEX, item) or re.match(NTNU_STUDENT_ID_REGEX, item):
                    dir_name = item
                    structure_err = False
                    break
                elif os.path.isfile(os.path.join(result_path, item, "mp0.c")):
                    guess_dir_name = item
                    break

        if dir_name == "" and guess_dir_name != "":
            dir_name = guess_dir_name

        # overwrite mp0.c and Makefile in xv6
        shutil.copy(os.path.join(result_path, dir_name, "mp0.c"), os.path.join(XV6_PATH, "user"))
        shutil.copy(os.path.join(result_path, dir_name, "Makefile"), XV6_PATH)

        # run grading
        os.chdir(XV6_PATH)
        process = subprocess.Popen("make grade", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, _ = process.communicate()
        subprocess.Popen("make clean > /dev/null", shell=True).wait()  # wait to ensure it finishes
        os.chdir(CURRENT_PATH)

        # store results
        with open(os.path.join(result_path, "result.txt"), "w") as f:
            f.write(stdout)

        global RESULTS_BUF
        score_pattern = r"Score: (\d{1,3})/100"
        match = re.search(score_pattern, stdout)
        if match:
            score = match.group(0)  # Full match, e.g., "Score: 90/100"
            RESULTS_BUF += student_id + ", " + score + "\n"
            print "Score for " + student_id + ": " + score
        else:
            print "No score found in output for " + student_id

        # dir name does not comform with the specification
        if structure_err:
            with open(os.path.join(result_path, "result.txt"), "a") as f:
                f.write("Malformed directory structure. Should -10 points.\n")

    except Exception as e:
        global ERR_BUF
        ERR_BUF += student_id + ", " + str(e) + "\n\n"
        print "Grading error: " + str(e)
        with open(os.path.join(result_path, "err.txt"), "w") as f:
            f.write(str(e))

    return


def grade():
    assert os.path.exists(XV6_PATH)
    assert os.path.exists(SUBMISSIONS_PATH)
    os.mkdir(RESULT_DIR)

    for submission in os.listdir(SUBMISSIONS_PATH):
        if submission.endswith(".zip"):
            print "Grading " + submission
            grade_individual(submission)
            print ""

    summary_path = os.path.join(RESULT_DIR, "summary.csv")
    err_path = os.path.join(RESULT_DIR, "error.csv")
    with open(summary_path, "w") as f:
        f.write(RESULTS_BUF)
    with open(err_path, "w") as f:
        f.write(ERR_BUF)
    return


if __name__ == "__main__":
    grade()
