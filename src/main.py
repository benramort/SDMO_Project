import csv
import pandas as pd
import unicodedata
import string

from Levenshtein import ratio as sim
from pydriller import Repository
from git import Repo
import os
import dev_fetcher
import bird_heuristic
# This block of code take the repository, fetches all the commits,
# retrieves name and email of both the author and commiter and saves the unique
# pairs to csv
# If you provide a URL, it clones the repo, fetches the commits and then deletes it,
# so for a big project better clone the repo locally and provide filesystem path

DEVS = dev_fetcher.fetch_devs(os.environ["REPOSITORY_URL"])
# DEVS = dev_fetcher.fetch_devs("/home/benat/Dokumentuak/Oulu/Software Development, Maintenance and Operations/SDMO_Project/.git")
# Compute similarity between all possible pairs

SIMILARITY = bird_heuristic.similarity_list(DEVS)

# Save data on all pairs (might be too big -> comment out to avoid)
cols = ["name_1", "email_1", "name_2", "email_2", "c1", "c2",
        "c3.1", "c3.2", "c4", "c5", "c6", "c7"]
df = pd.DataFrame(SIMILARITY, columns=cols)
df.to_csv(os.path.join("results", "devs_similarity.csv"), index=False, header=True)

# Set similarity threshold, check c1-c3 against the threshold
t=float(os.environ["THRESHOLD"])
print("Threshold:", t)
df["c1_check"] = df["c1"] >= t
df["c2_check"] = df["c2"] >= t
df["c3_check"] = (df["c3.1"] >= t) & (df["c3.2"] >= t)
# Keep only rows where at least one condition is True
df = df[df[["c1_check", "c2_check", "c3_check", "c4", "c5", "c6", "c7"]].any(axis=1)]

# Omit "check" columns, save to csv
df = df[["name_1", "email_1", "name_2", "email_2", "c1", "c2",
        "c3.1", "c3.2", "c4", "c5", "c6", "c7"]]
df.to_csv(os.path.join("results", f"devs_similarity_t={t}.csv"), index=False, header=True)