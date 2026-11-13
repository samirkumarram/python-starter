import argparse
import sys
import re
from collections import Counter
from pathlib import Path

def countNword(text):
	words = re.findall(r"[^\W\d_]+", text.lower(), flags = re.UNICODE)
	return Counter(words)

def main():
	parser = argparse.ArgumentParser(description = "Count words in a text file.")
	parser.add_argument("filename", help = "input text file")
	parser.add_argument("-n", "--top", type = int, default = 8, help = "number of top words to display")
	args = parser.parse_args()
	
	try:
		text = Path(args.filename).read_text(encoding="utf-8")
	except FileNotFoundError:
		print(f"Error: file '{args.filename}' was not found!", file = sys.stderr)
		return 1
	counts = countNword(text)
	for word, count in counts.most_common(args.top):
		print(f"{word}:\t{count}")
	return 0
if __name__ == "__main__":
	raise SystemExit(main())