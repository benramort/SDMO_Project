import bird_heuristic
import os

def test_process_correct():
    dev = ("John Doe", "john.doe@example.com")
    expected = ("john doe", "john", "doe", "j", "d", "john.doe@example.com", "john.doe")
    assert bird_heuristic.process(dev) == expected

def test_process_single_name():
    dev = ("John", "john.doe@example.com")
    expected = ("john", "john", "", "j", "", "john.doe@example.com", "john.doe")
    assert bird_heuristic.process(dev) == expected

def test_process_multiple_spaces():
    dev = ("John De La Sierra", "john.doe@example.com")
    expected = ("john de la sierra", "john", "de la sierra", "j", "d", "john.doe@example.com", "john.doe")
    assert bird_heuristic.process(dev) == expected

def test_similarity_check():
    THRESHOLD = float(os.environ["THRESHOLD"])
    dev_a = ("john doe", "john", "doe", "j", "d", "john.doe@example.com", "john.doe")
    dev_b = ("john doe", "john", "doe", "j", "d", "john.doe@example.com", "john.doe")
    expected = ("john doe", "john.doe@example.com", "john doe", "john.doe@example.com", 1, 1, 1, 1, True, True, True, True)
    assert bird_heuristic.similarity_check(dev_a, dev_b) == expected

    dev_c = ("jane smith", "jane", "smith", "j", "s", "jane.smith@example.com", "jane.smith")
    result = bird_heuristic.similarity_check(dev_a, dev_c)
    assert result[4] < THRESHOLD
    assert result[5] < THRESHOLD
    assert result[6] < THRESHOLD
    assert result[7] < THRESHOLD
    assert result[8] is False
    assert result[9] is False
    assert result[10] is False
    assert result[11] is False

def test_similarity_list():
    devs = [("John Doe", "john.doe@example.com"), ("Jane Austen", "jane.austen@example.com")]
    similarity_list = bird_heuristic.similarity_list(devs)
    assert len(similarity_list) == 1
    # print(similarity_list)
    # print(bird_heuristic.similarity_check(devs[0], devs[1]))
    assert similarity_list[0] == bird_heuristic.similarity_check(bird_heuristic.process(devs[0]), bird_heuristic.process(devs[1]))

