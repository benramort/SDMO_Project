from itertools import combinations
import dev_fetcher
import string
import unicodedata
from Levenshtein import ratio as sim
# Function for pre-processing each name,email
def process(dev):
    name: str = dev[0]

    # Remove punctuation
    trans = name.maketrans("", "", string.punctuation)
    name = name.translate(trans)
    # Remove accents, diacritics
    name = unicodedata.normalize('NFKD', name)
    name = ''.join([c for c in name if not unicodedata.combining(c)])
    # Lowercase
    name = name.casefold()
    # Strip whitespace
    name = " ".join(name.split())


    # Attempt to split name into firstname, lastname by space
    parts = name.split(" ")
    # Expected case
    if len(parts) == 2:
        first, last = parts
    # If there is no space, firstname is full name, lastname empty
    elif len(parts) == 1:
        first, last = name, ""
    # If there is more than 1 space, firstname is until first space, rest is lastname
    else:
        first, last = parts[0], " ".join(parts[1:])

    # Take initials of firstname and lastname if they are long enough
    i_first = first[0] if len(first) > 1 else ""
    i_last = last[0] if len(last) > 1 else ""

    # Determine email prefix
    email: str = dev[1]
    prefix = email.split("@")[0]

    return name, first, last, i_first, i_last, email, prefix

# def similarity_check(DEVS):
#     SIMILARITY = []
    
#     for dev_a, dev_b in combinations(DEVS, 2):
#     # Pre-process both developers
#         name_a, first_a, last_a, i_first_a, i_last_a, email_a, prefix_a = process(dev_a)
#         name_b, first_b, last_b, i_first_b, i_last_b, email_b, prefix_b = process(dev_b)

#     # Conditions of Bird heuristic
#         c1 = sim(name_a, name_b)
#         c2 = sim(prefix_b, prefix_a)
#         c31 = sim(first_a, first_b)
#         c32 = sim(last_a, last_b)
#         c4 = c5 = c6 = c7 = False
#     # Since lastname and initials can be empty, perform appropriate checks
#         if i_first_a != "" and last_a != "":
#             c4 = i_first_a in prefix_b and last_a in prefix_b
#         if i_last_a != "":
#             c5 = i_last_a in prefix_b and first_a in prefix_b
#         if i_first_b != "" and last_b != "":
#             c6 = i_first_b in prefix_a and last_b in prefix_a
#         if i_last_b != "":
#             c7 = i_last_b in prefix_a and first_b in prefix_a

#     # Save similarity data for each conditions. Original names are saved
#         SIMILARITY.append([dev_a[0], email_a, dev_b[0], email_b, c1, c2, c31, c32, c4, c5, c6, c7])
#     return SIMILARITY

def similarity_check(dev_a, dev_b):
    # Pre-process both developers
        name_a, first_a, last_a, i_first_a, i_last_a, email_a, prefix_a = dev_a
        name_b, first_b, last_b, i_first_b, i_last_b, email_b, prefix_b = dev_b

    # Conditions of Bird heuristic
        c1 = sim(name_a, name_b)
        c2 = sim(prefix_b, prefix_a)
        c31 = sim(first_a, first_b)
        c32 = sim(last_a, last_b)
        c4 = c5 = c6 = c7 = False
    # Since lastname and initials can be empty, perform appropriate checks
        if i_first_a != "" and last_a != "":
            c4 = i_first_a in prefix_b and last_a in prefix_b
        if i_last_a != "":
            c5 = i_last_a in prefix_b and first_a in prefix_b
        if i_first_b != "" and last_b != "":
            c6 = i_first_b in prefix_a and last_b in prefix_a
        if i_last_b != "":
            c7 = i_last_b in prefix_a and first_b in prefix_a

        return dev_a[0], email_a, dev_b[0], email_b, c1, c2, c31, c32, c4, c5, c6, c7


def similarity_list(DEVS):
    processed_devs = [process(dev) for dev in DEVS]
    SIMILARITY = [similarity_check(dev_a, dev_b) for dev_a, dev_b in combinations(processed_devs, 2)]
    return SIMILARITY