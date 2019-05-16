# ir-project-14

# To run with example data:

Firstly, make sure to have a running instance of elasticsearch. make_index.py and elasticSearchUI assumes a running instance on
the default port, port 9200. Now:

1. cd crawler
2. sh run.sh

Alternatively, instead of running run.sh, you can create an empty folder `sources/` and remove `path_index.txt` if it already exits. Then pass a list of repositories of your own choosing into stdin of `crawler.py`, in the format suggested by `example_input.txt`. Next, create your index: 

3. cd ..
4. python3 make_index.py

Finally, start the UI server (launches an instance on port 3001):

5. node elasticSearchUI/index.js
