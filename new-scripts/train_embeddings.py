import os


def file_exists(file_path):
    """
    Check if a file exists and prompt until the correct file path is entered.
    """
    while not os.path.isfile(file_path):
        print(f"Error: '{file_path}' does not exist. Please enter a valid file path.")
        file_path = input("Re-enter the file name: ").strip()
    return file_path


def train_word_embeddings():
    """
    Train dependency-based word embeddings using word2vecf with user-specified inputs.
    """
    # Prompt user for input file names and validate their existence
    train_file = input("Enter the training file name (e.g., dep1.contexts): ").strip()
    train_file = file_exists(train_file)

    word_vocab = input("Enter the word vocabulary file name (e.g., words): ").strip()
    word_vocab = file_exists(word_vocab)

    context_vocab = input("Enter the context vocabulary file name (e.g., contexts): ").strip()
    context_vocab = file_exists(context_vocab)

    output_file = input("Enter the output file name for word embeddings (e.g., word_embeddings.txt): ").strip()
    if not output_file:
        output_file = "word_embeddings.txt"

    # Optional parameters
    embedding_size = input("Enter embedding size (default=200): ").strip()
    embedding_size = int(embedding_size) if embedding_size.isdigit() else 200

    negative_samples = input("Enter number of negative samples (default=15): ").strip()
    negative_samples = int(negative_samples) if negative_samples.isdigit() else 15

    num_threads = input("Enter number of threads to use (default=4): ").strip()
    num_threads = int(num_threads) if num_threads.isdigit() else 4

    # Command to run word2vecf
    command = (
        f"./word2vecf -train {train_file} "
        f"-wvocab {word_vocab} -cvocab {context_vocab} "
        f"-output {output_file} -size {embedding_size} "
        f"-negative {negative_samples} -threads {num_threads}"
    )

    print("\nRunning command to train word embeddings...")
    print(command)  # Print command for reference
    os.system(command)  # Execute the command
    print(f"\nTraining complete. Word embeddings saved to '{output_file}'")


if __name__ == "__main__":
    train_word_embeddings()
