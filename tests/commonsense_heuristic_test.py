import commonsense_heuristic
import os

def test_process_correct():
    dev = ("John Doe", "john.doe@example.com")
    expected = ("john doe", ["john", "doe"], ["j", "d"], "john.doe@example.com", "john.doe")
    print(commonsense_heuristic.process(dev))
    assert commonsense_heuristic.process(dev) == expected

def test_process_at_email():
    dev = ("John Doe", "john.doe at example.com")
    expected = ("john doe", ["john", "doe"], ["j", "d"], "john.doe@example.com", "john.doe")
    assert commonsense_heuristic.process(dev) == expected

def test_similarity_check():
    THRESHOLD = float(os.environ["THRESHOLD"])
    dev_a = ("john doe", ["john", "doe"], ["j", "d"], "john.doe@example.com", "john.doe")
    dev_b = ("john doe", ["john", "doe"], ["j", "d"], "john.doe@example.com", "john.doe")
    expected = ("john doe", "john.doe@example.com", "john doe", "john.doe@example.com", 1, True, True, True)
    assert commonsense_heuristic.similarity_check(dev_a, dev_b) == expected

    dev_c = ("jane smith", ["jane", "smith"], ["j", "s"], "jane.smith@example.com", "jane.smith")
    print(commonsense_heuristic.similarity_check(dev_a, dev_c))
    result = commonsense_heuristic.similarity_check(dev_a, dev_c)
    assert result[4] < THRESHOLD
    assert result[5] is False
    assert result[6] is False
    assert result[7] is False

def test_similarity_list():
    devs = [("John Doe", "john.doe@example.com"), ("Jane Austen", "jane.austen@example.com")]
    similarity_list = commonsense_heuristic.similarity_list(devs)
    assert len(similarity_list) == 1
    # print(similarity_list)
    # print(commonsense_heuristic.similarity_check(devs[0], devs[1]))
    assert similarity_list[0] == commonsense_heuristic.similarity_check(commonsense_heuristic.process(devs[0]), commonsense_heuristic.process(devs[1]))

