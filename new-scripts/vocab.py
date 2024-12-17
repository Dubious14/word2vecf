from collections import defaultdict

def build_vocab(input_file, word_vocab_file, context_vocab_file, min_count=5):
    """
    Build vocabularies for words and contexts from word-context pairs.

    Parameters:
    - input_file: Path to the word-context pairs file (e.g., dep.contexts).
    - word_vocab_file: Output file for the word vocabulary.
    - context_vocab_file: Output file for the context vocabulary.
    - min_count: Minimum frequency threshold for including words/contexts.
    """
    word_counts = defaultdict(int)
    context_counts = defaultdict(int)

    # First pass: Count words and contexts
    print("Counting words and contexts...")
    with open(input_file, "r") as f:
        for line in f:
            if line.strip():  # Skip blank lines
                parts = line.strip().split("\t")
                if len(parts) == 2:  # Ensure the line has exactly two values
                    word, context = parts
                    word_counts[word] += 1
                    context_counts[context] += 1
                else:
                    print(f"Skipping malformed line: {line.strip()}")

    # Save the filtered word vocabulary
    print(f"Saving word vocabulary to '{word_vocab_file}'...")
    with open(word_vocab_file, "w") as wv:
        for word, count in word_counts.items():
            if count >= min_count:
                wv.write(f"{word}\t{count}\n")

    # Save the filtered context vocabulary
    print(f"Saving context vocabulary to '{context_vocab_file}'...")
    with open(context_vocab_file, "w") as cv:
        for context, count in context_counts.items():
            if count >= min_count:
                cv.write(f"{context}\t{count}\n")

    print("Vocabularies built and saved successfully!")


if __name__ == "__main__":
    # Input file: word-context pairs
    input_file = input("Enter the input file name (e.g., dep.contexts): ").strip()
    if not input_file:
        input_file = "dep.contexts"

    # Output files for vocabularies
    word_vocab_file = input("Enter the word vocabulary file name (e.g., wv): ").strip()
    if not word_vocab_file:
        word_vocab_file = "wv"

    context_vocab_file = input("Enter the context vocabulary file name (e.g., cv): ").strip()
    if not context_vocab_file:
        context_vocab_file = "cv"

    # Minimum frequency threshold
    min_count = input("Enter minimum frequency threshold (default=5): ").strip()
    min_count = int(min_count) if min_count.isdigit() else 5

    # Build the vocabularies
    build_vocab(input_file, word_vocab_file, context_vocab_file, min_count)
