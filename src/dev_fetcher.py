import csv 
import os
from pydriller import Repository

class dev_fetcher():
    def fetch_devs():
        DEVS = set()
        for commit in Repository("https://github.com/dotnet-architecture/eShopOnContainers").traverse_commits():
            DEVS.add((commit.author.name, commit.author.email))
            DEVS.add((commit.committer.name, commit.committer.email))

        DEVS = sorted(DEVS)

        with open(os.path.join("results", "devs.csv"), 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"')
            writer.writerow(["name", "email"])
            writer.writerows(DEVS)
#

# This block of code reads an existing csv of developers

        DEVS = []
# Read csv file with name,dev columns
        with open(os.path.join("results", "devs.csv"), 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                DEVS.append(row)
# First element is header, skip
        DEVS = DEVS[1:]
        return DEVS