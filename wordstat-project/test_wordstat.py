import pytest
from collections import Counter
from wordstat import countNword, main

def test_unicode_words():
    result = countNword("café naÏve")
    assert result == Counter({"café": 1, "naïve": 1})

def test_very_long_line():
	text = "word " * 100_000
	result = countNword(text)
	assert result == Counter({"word": 100_000})

def test_top_n_output(tmp_path, monkeypatch, capsys):
    file = tmp_path / "sample.txt"
    file.write_text("bus bus bus truck truck car car car", encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["wordstat.py", str(file), "-n", "2"])
    assert main() == 0
    output = capsys.readouterr().out.splitlines()
    assert len(output) == 2
    assert output[0] == "bus:\t3"
    assert output[1] == "car:\t3"
	
def handle_empty_file(tmp_path, monkeypatch):
	file = tmp_path / "empty.txt"
	file.write_text("", encoding = "utf-8")
	monkeypatch.setattr("sys.argv", ["wordstat.py", str(file)])
	assert main() == 0

def test_word_count():
	result = countNword("book pen pen book tea")
	assert result == Counter({"book": 2, "pen": 2, "tea": 1})

def test_case_insensitive():
	result = countNword("Python python PYTHON pyTHon")
	assert result == Counter({"python": 4})

def test_missing_file(tmp_path, monkeypatch, capsys):
	file = tmp_path / "missing.txt"
	monkeypatch.setattr("sys.argv", ["wordstat.py", str(file)])
	assert main() == 1
	error = capsys.readouterr().err
	assert "was not found!" in error

def test_invalid_top_n(monkeypatch):
	monkeypatch.setattr("sys.argv", ["wordstat.py", "sample.txt", "-n", "abc"])
	with pytest.raises(SystemExit) as error:
		main()
	assert error.value.code == 2
