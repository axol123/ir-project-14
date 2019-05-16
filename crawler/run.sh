rm -r path_index.txt sources
mkdir sources
# python3 toprepos.py > example_input.txt
cat example_input.txt | python3 crawler.py
