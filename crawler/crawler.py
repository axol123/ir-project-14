import json
import uuid
import sys
import subprocess

clone_prefix = "https://github.com/"
clone_suffix = ".git"

#            continue
#        ssh_url = clone_prefix + repo.rstrip() + clone_suffix
#        subprocess.run(["git", "clone", ssh_url])
#        result = subprocess.run(["find", repo.split("/")[1], "-iname '*.java'"])
#        print(result.stdout)
    
def clone_and_copy(repo :str) -> str:
    path_index = ""

    # clone rep
    repo = repo.rstrip()
    https_url = clone_prefix + repo + clone_suffix
    subprocess.run(["git", "clone", https_url])

    # find all *.java files
    result = subprocess.check_output(["find", repo.split("/")[1], "-iname", "*.java"]).decode(sys.stdout.encoding)
    fp_list = result.split("\n")

    # move to sources/ and append to path_index
    for filepath in fp_list:
        if not filepath:
            continue
        id = uuid.uuid1().__str__()
        filename = id + "-" + filepath.split("/")[-1]
        rNameLen = len(repo.split("/")[-1])
        path_index += filename + " " + repo + "/blob/master" + filepath[rNameLen:] + "\n"
        subprocess.run(["cp", filepath, "sources/"+filename])

    # remove repo when complete
    subprocess.run(["rm", "-rf", repo.split("/")[-1]])

    return path_index

if __name__ == "__main__":
    path_index = ""
    for repo in sys.stdin:
        print("processing " + repo)
        if repo[0] == '#':
            continue
        path_index += clone_and_copy(repo)
    f = open("path_index.txt", "w+")
    f.write(path_index)
    f.close()
    #main(sys.argv[1:])
