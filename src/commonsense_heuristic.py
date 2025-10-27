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

    #We split the name parts
    parts = name.split(" ")

    #Get the initials for all the parts
    initials = [p[0] for p in parts if p]

    email: str = dev[1]
    if " at " in email: #In some cases it seems there is "at" instead of "@" so I put this here.
        email = email.replace(" at ", "@")
    prefix = email.split("@")[0]

    if len(dev) > 2:
        return name, parts, dev[2], initials, email, prefix
    else:
        return name, parts, initials, email, prefix


def similarity_check(dev_a, dev_b):
    # Pre-process both developers
    
    name_a = parts_a = id_a = initials_a = email_a = prefix_a = 0
    name_b = parts_b = id_b = initials_b = email_b = prefix_b = 0
    if len(dev_a) > 5:
        name_a, parts_a, id_a, initials_a, email_a, prefix_a = dev_a
        name_b, parts_b, id_b, initials_b, email_b, prefix_b = dev_b
    else: 
        name_a, parts_a, initials_a, email_a, prefix_a = dev_a = dev_a
        name_b, parts_b, initials_b, email_b, prefix_b = dev_b = dev_b

    #EMAIL CHECK
    c_email_same = sim(prefix_b, prefix_a) #Check the similarity between the two prefixes.

    #Get all combinations of the parts of the name of each developer 
    combinedAllA = [a + b for a in parts_a for b in parts_a if a != b and len(a) > 1 and len(b) > 1] 
    combinedAllB = [a + b for a in parts_b for b in parts_b if a != b and len(a) > 1 and len(b) > 1] 
   
    #leftover
    #combinedAndBaseA = combinedAllA 
    #combinedAndBaseB = combinedAllB
    
    #We keep the parts that are longer than 1 
    #longA = [p for p in combinedAndBaseA if len(p) > 1]
    #longB = [p for p in combinedAndBaseB if len(p) > 1]
    
    #NAME IN EMAIL CHECK
    c_inEmailB = any(sim(p, prefix_b) >= 0.8 for p in combinedAllA) 
    c_inEmailA = any(sim(p, prefix_a) >= 0.8 for p in combinedAllB)  
    
    #if(c_inEmailB != True): c_inEmailB = any(sim(p, prefix_b) >= 0.9 for p in parts_a if len(p) >1)
    #if(c_inEmailA != True): c_inEmailA = any(sim(p, prefix_a) >= 0.9 for p in parts_b if len(p) >1)
    
    #We remove the numbers for the following check
    remove_digits_table = str.maketrans('', '', string.digits)
    combinedAllA = [p.translate(remove_digits_table) for p in combinedAllA]
    combinedAllB = [p.translate(remove_digits_table) for p in combinedAllB]
    
    #NAME WITH NAME CHECK
    c_partAinB = False
    similarCount : int = 0
    for partA in parts_a:
        for partB in parts_b: #PART TO PART
            if sim(partA, partB) >= 0.85:
                similarCount += 1
                break
        for partB in combinedAllB: #PART TO COMBINATION
            if sim(partA, partB) >= 0.9:
                if(dev_a[2] != dev_b[2]):
                    print(partA + "---" + partB  + "///" + dev_a[0] + " " + dev_b[0])
                similarCount += 1
                break
                
    for partA in combinedAllA:
        for partB in combinedAllB: #PART TO COMBINATION
            if sim(partA, partB) > 0.9:
                if(dev_a[2] != dev_b[2]):
                    print(partA + "---" + partB  + "///" + dev_a[0] + " " + dev_b[0])
                similarCount += 1
                break
        for partB in parts_b: #PART TO COMBINATION 
            if sim(partA, partB) > 0.9:
                if(dev_a[2] != dev_b[2]):
                    print(partA + "---" + partB  + "///" + dev_a[0] + " " + dev_b[0])
                similarCount += 1
                break
               
    #Depending on the length of the name we will demand more matches 
    threshold = (len(parts_a) * len(parts_b)) / 2
    if threshold == 0:
        threshold = 1

    if similarCount > threshold:
        c_partAinB = True                                  
                    
    if len(dev_a) < 6:
        return dev_a[0], email_a, dev_b[0], email_b, c_email_same, c_inEmailA, c_inEmailB, c_partAinB
    else:
        return dev_a[0], dev_a[2], email_a, dev_b[0], dev_b[2], email_b, c_email_same, c_inEmailA, c_inEmailB, c_partAinB
        
def similarity_list(DEVS):
    processed_devs = [process(dev) for dev in DEVS]
    
    SIMILARITY = [similarity_check(dev_a, dev_b) for dev_a, dev_b in combinations(processed_devs, 2)]
    
    return SIMILARITY
    
   