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
import commonsense_heuristic

# This block of code take the repository, fetches all the commits,
# retrieves name and email of both the author and commiter and saves the unique
# pairs to csv
# If you provide a URL, it clones the repo, fetches the commits and then deletes it,
# so for a big project better clone the repo locally and provide filesystem path

DEVS = dev_fetcher.fetch_devs("https://github.com/benramort/Spootify")
#DEVS = dev_fetcher.load_devs_with_id("results/Audacity/devs.csv")
# DEVS = dev_fetcher.fetch_devs("/home/benat/Dokumentuak/Oulu/Software Development, Maintenance and Operations/SDMO_Project/.git")

# Compute similarity between all possible pairs

SIMILARITY = commonsense_heuristic.similarity_list(DEVS)

controlDataset : bool = False

DEVS_list = list(DEVS)
dev = DEVS_list[0]

if len(dev) > 5:
    controlDataset = True

if controlDataset:
    #Define all the columns with the IDs
    cols = ["name_1", "id_1", "email_1", "name_2", "id_2", "email_2", "c_email_same", "c_inEmailA",
        "c_inEmailB", "c_partAinB"]
        
    df = pd.DataFrame(SIMILARITY, columns=cols)
    df.to_csv(os.path.join("results", "devs_similarity.csv"), index=False, header=True)

    # Set similarity threshold, check c1-c3 against the threshold
    t=0.7
    print("Threshold:", t)

    df_remaining = df[(df["id_1"] == df["id_2"]) & (df["c_email_same"] < t)]
    df_remaining = df_remaining[~df_remaining[["c_inEmailA", "c_inEmailB", "c_partAinB"]].any(axis=1)]


    df["c_email_check"] = df["c_email_same"] >= t
    # Keep only rows where at least one condition is True
    df = df[df[["c_email_check", "c_inEmailA", "c_inEmailB", "c_partAinB"]].any(axis=1)]

    same_id_count = (df["id_1"] == df["id_2"]).sum()
    different_id_count = (df["id_1"] != df["id_2"]).sum()
    invalid_id_count = (df["id_1"] == 0).sum() + (df["id_2"] == 0).sum()
     
    print(f"Pairs with same ID: {same_id_count}")
    print(f"Pairs with different IDs: {different_id_count}")
    print(f"Pairs with invalid ID: {invalid_id_count}")

     
    # Save both to separate CSV files
    out_dir = "results"
    os.makedirs(out_dir, exist_ok=True)

    df = df[["name_1", "id_1", "email_1", "name_2", "id_2", "email_2", "c_email_same", "c_inEmailA", "c_inEmailB", "c_partAinB"]]
    df.to_csv(os.path.join("results", f"devs_similarity_t={t}.csv"), index=False, header=True)

    # Split into matching and non-matching pairs
    df_match = df[df["id_1"] == df["id_2"]]
    df_nonmatch = df[df["id_1"] != df["id_2"]]

    df_remaining.to_csv(
        os.path.join(out_dir, f"devs_similarity_t={t}_sameid_low_similarity.csv"),
        index=False,
        header=True
    )

    df_match.to_csv(os.path.join(out_dir, f"devs_similarity_t={t}_match.csv"), index=False, header=True)
    df_nonmatch.to_csv(os.path.join(out_dir, f"devs_similarity_t={t}_nonmatch.csv"), index=False, header=True)
    
else:
    #Define the columns without the IDs 
    cols = ["name_1", "emsubmittedail_1", "name_2", "email_2", "c_email_same", "c_inEmailA", "c_inEmailB", "c_partAinB"]
    
    df = pd.DataFrame(SIMILARITY, columns=cols)
    df.to_csv(os.path.join("results", "devs_similarity.csv"), index=False, header=True)
    
    # Set similarity threshold, check c1-c3 against the threshold
    t=0.7
    print("Threshold:", t)
    
    df["c_email_check"] = df["c_email_same"] >= t
    df = df[df[["c_inEmailA", "c_inEmailB", "c_partAinB"]].any(axis=1)]
    df.to_csv(os.path.join("results", f"devs_similarity_t={t}.csv"), index=False, header=True)
    
    # Save both to separate CSV files
    out_dir = "results"
    os.makedirs(out_dir, exist_ok=True)