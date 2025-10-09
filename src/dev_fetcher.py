import csv 
import os
from pydriller import Repository

class dev_fetcher():
    
    def fetch_devs():
        DEVS = set()
        for commit in Repository("https://github.com/benramort/Spootify").traverse_commits():
            DEVS.add((commit.author.name, commit.author.email))
            DEVS.add((commit.committer.name, commit.committer.email))

        DEVS = sorted(DEVS)

        with open(os.path.join("results", "devs.csv"), 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"')
            writer.writerow(["name", "email"])
            writer.writerows(DEVS)
        
        print(DEVS)
        return DEVS
    
    def load_devs(file : str):
        DEVS = []
        with open(file, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                DEVS.append(row)
        DEVS = DEVS[1:]
        return DEVS
