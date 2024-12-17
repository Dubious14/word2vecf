from collections import defaultdict


def extract_dependencies(conll_input, output_file, min_word_freq=0):
    """
    Extract word-context pairs from a CoNLL-formatted dependency parse file.

    Parameters:
    - conll_input: Path to the input parsed CoNLL file.
    - output_file: Path to save the extracted word-context pairs.
    - min_word_freq: Minimum word frequency threshold (optional).
    """
    # Store word frequencies
    word_freq = defaultdict(int)

    # First pass: Count word frequencies
    print("Counting word frequencies...")
    with open(conll_input, "r") as f:
        for line in f:
            if line.strip():  # Skip blank lines
                parts = line.split("\t")
                word = parts[1].lower()
                word_freq[word] += 1

    # Second pass: Extract dependencies
    print("Extracting dependencies...")
    with open(conll_input, "r") as f, open(output_file, "w") as out:
        sentence = []
        for line in f:
            if line.strip():
                parts = line.split("\t")
                word_id = int(parts[0])
                word = parts[1].lower()
                head = int(parts[6])  # Head word ID
                relation = parts[7]  # Dependency relation
                sentence.append((word_id, word, head, relation))
            else:
                # Process the sentence
                for word_id, word, head, relation in sentence:
                    if relation.strip().lower() != "punct" and head > 0:
                        head_word = sentence[head - 1][1]
                        context = f"{head_word}-{relation}"
                        if word_freq[word] >= min_word_freq:
                            out.write(f"{word}\t{context}\n")
                sentence = []  # Reset sentence

    print(f"Dependencies extracted and saved to '{output_file}'")


if __name__ == "__main__":
    # Input file: Parsed CoNLL file
    conll_input = input("Enter the parsed CoNLL file name (e.g., parsed.conll): ").strip()
    if not conll_input:
        conll_input = "parsed.conll"

    # Output file: Word-context pairs
    output_file = input("Enter the output file name (e.g., dep.contexts): ").strip()
    if not output_file:
        output_file = "dep.contexts"

    # Optional: Minimum word frequency
    min_word_freq = input("Enter minimum word frequency (default=0): ").strip()
    min_word_freq = int(min_word_freq) if min_word_freq.isdigit() else 0

    # Run the extraction
    extract_dependencies(conll_input, output_file, min_word_freq)
