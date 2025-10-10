# import os
# import csv
# from dev_fetcher import *

# def test_load_devs_correct():
#     #Setup
#     devs = set()
#     devs.add(("name1", "email1"))
#     devs.add(("name2", "email2"))
#     devs.add(("name3", "email3"))
#     with open("test.csv", 'w', newline='') as csvfile:
#         writer = csv.writer(csvfile, delimiter=',', quotechar='"')
#         writer.writerow(["name", "email"])
#         writer.writerows(devs)

#     #Test
#     loaded_devs = dev_fetcher.load_devs("test.csv")
#     assert len(loaded_devs) == 3
#     assert ["name1", "email1"] in loaded_devs
#     assert ["name2", "email2"] in loaded_devs
#     assert ["name3", "email3"] in loaded_devs

#     #Cleanup
#     os.remove("test.csv")

# def test_load_devs_empty_file():
#     #Setup
#     with open("test.csv", 'w', newline='') as csvfile:
#         ...

#     #Test
#     loaded_devs = dev_fetcher.load_devs("test.csv")
#     assert len(loaded_devs) == 0

#     #Cleanup
#     os.remove("test.csv")

# def test_load_devs_no_file():
#     try:
#         dev_fetcher.load_devs("non_existent_file.csv")
#         assert False, "Expected an exception for non-existent file"
#     except FileNotFoundError:
#         assert True