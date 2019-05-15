import urllib.request
import json
import sys
import re
import uuid

query_prefix = "https://api.github.com/repos/"
query_suffix = "/git/trees/master?recursive=1"
githubusercontent_prefix = "https://raw.githubusercontent.com/"

"""
Returns paths to files within the specified repository ending with specified 
file extension.

repository must include owner and repository name. E.g. "henrikglass/erodr"
"""
def get_filepaths(repository :str, extension :str) -> str:
    query = query_prefix + repository + query_suffix;
    res = urllib.request.urlopen(query)
    res = json.loads(res.read().decode('utf-8'))
    paths = ""
    for entry in res['tree']:
        path = entry['path']
        if path.endswith(extension):
            paths += repository + "/blob/master/" + path + "\n"
            sys.stdout.write('.')
            sys.stdout.flush()
    return paths

"""
downloads files from github given a path (<owner>/<repo>/<branch/filepath>) and
stores them in specified directory, prepended with a unique id. A mapping of
the unique filename to its filepath are added to path_index
"""
def download_files(path_index :str, filepath :str, directory :str) -> str:
    file_url = githubusercontent_prefix + filepath;
    id = uuid.uuid1().__str__()
    filename = id + "-" + filepath.split("/")[-1]
    res = urllib.request.urlretrieve(file_url.replace('blob/',''), directory + filename)    # Temporarily replace blob before download
    path_index += filename + " " + filepath + "\n"
    
    return path_index

def main(argv):
    sys.stdout.write("Getting filepaths")
    paths = ""
    for line in sys.stdin:
        if line[0] == '#':
            continue
        paths += get_filepaths(line.rstrip(), ".java")
 
    sys.stdout.write('\n')
    sys.stdout.write("Downloading files.")
    path_index = ""
    for path in paths.splitlines():
        sys.stdout.write('.')
        sys.stdout.flush()
        path_index = download_files(path_index, path, "sources/")
    sys.stdout.write('\n')

    f = open("path_index.txt", "w+")
    f.write(path_index)
    f.close()
    
    
if __name__ == "__main__":
    main(sys.argv[1:])
