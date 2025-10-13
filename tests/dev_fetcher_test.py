import os
import csv
import dev_fetcher
import git


def test_fetch_devs_correct(tmp_path):
    #Setup
    repo_path = tmp_path / "test_repo"
    os.mkdir(repo_path)
    repository = git.Repo.init(repo_path)
    #Commiter 1
    file1 = repo_path / "file1.txt"
    file1.write_text("change1")
    repository.index.add([str(file1)])
    repository.index.commit("Commit1", author=git.Actor("name1", "email1"), committer=git.Actor("name1", "email1"))
    #Commiter 2
    file2 = repo_path / "file2.txt"
    file2.write_text("change2")
    repository.index.add([str(file2)])
    repository.index.commit("Commit2", author=git.Actor("name2", "email2"), committer=git.Actor("name2", "email2"))
    #Commiter 3
    file1 = repo_path / "file3.txt"
    file1.write_text("change3")
    repository.index.add([str(file1)])
    repository.index.commit("Commit3", author=git.Actor("name3", "email3"), committer=git.Actor("name3", "email3"))
    #Test
    devs = dev_fetcher.fetch_devs(str(repo_path), store = False)
    assert len(devs) == 3
    assert ("name1", "email1") in devs
    assert ("name2", "email2") in devs
    assert ("name3", "email3") in devs

    # devs = dev_fetcher.load_devs("results/devs.csv") TODO Make something with load devs
    # assert len(devs) == 3
    # assert ("name1", "email1") in devs
    # assert ("name2", "email2") in devs
    # assert ("name3", "email3") in devs
    #Cleanup
    repository.close()


def test_load_devs_correct(tmp_path):
    #Setup
    devs = set()
    devs.add(("name1", "email1"))
    devs.add(("name2", "email2"))
    devs.add(("name3", "email3"))
    csv_path = tmp_path / "test.csv"
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"')
        writer.writerow(["name", "email"])
        writer.writerows(devs)

    #Test
    loaded_devs = dev_fetcher.load_devs(csv_path)
    assert len(loaded_devs) == 3
    assert ("name1", "email1") in loaded_devs
    assert ("name2", "email2") in loaded_devs
    assert ("name3", "email3") in loaded_devs

    #Cleanup
    os.remove(csv_path)

def test_load_devs_empty_file(tmp_path):
    #Setup
    csv_path = tmp_path / "test.csv"
    with open(csv_path, 'w', newline='') as csvfile:
        ...

    #Test
    loaded_devs = dev_fetcher.load_devs(csv_path)
    assert len(loaded_devs) == 0

    #Cleanup
    os.remove(csv_path)

def test_load_devs_no_file():
    try:
        dev_fetcher.load_devs("non_existent_file.csv")
        assert False, "Expected an exception for non-existent file"
    except FileNotFoundError:
        assert True