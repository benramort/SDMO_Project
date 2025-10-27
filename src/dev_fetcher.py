import csv 
import os
from pydriller import Repository

def fetch_devs(repository : str, store : bool = True):
    DEVS = set()
    for commit in Repository(repository).traverse_commits():
        #if not "@users.noreply.github.com" in commit.author.email:
        DEVS.add((commit.author.name, commit.author.email))
        DEVS.add((commit.committer.name, commit.committer.email))
    DEVS = sorted(DEVS)
    
    if (store):
        with open(os.path.join("results", "devs.csv"), 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"')
            writer.writerow(["name", "email"])
            writer.writerows(DEVS)
    
    print(DEVS)
    return DEVS

def load_devs(file : str):
    DEVS = set()
    with open(file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader, None)
        for row in reader:
            DEVS.add((row[0], row[1]))
    return DEVS

#I used this to include an id to load in a csv with the matches already determined to use as a control dataset.
def load_devs_with_id(file : str):
    DEVS = set()
    with open(file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader, None)
        for row in reader:
            DEVS.add((row[0], row[1], row[2]))
    return DEVS