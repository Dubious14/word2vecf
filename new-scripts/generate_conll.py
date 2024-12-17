import spacy

# Load SpaCy's small English language model
nlp = spacy.load("en_core_web_sm")

def convert_to_conll(sentences, output_file):
    """
    Convert a list of sentences to CoNLL format using SpaCy.
    Ensures the root token has head=0.
    """
    with open(output_file, "w") as f:
        for sentence in sentences:
            doc = nlp(sentence)
            for token in doc:
                head = 0 if token.head == token else token.head.i + 1  # ROOT has head=0
                f.write(f"{token.i + 1}\t{token.text}\t_\t{token.pos_}\t_\t_\t{head}\t{token.dep_}\n")
            f.write("\n")  # Separate sentences

# Example sentences
if __name__ == "__main__":
    sentences = [
        "Australian scientist discovers star with telescope."
    ]
    convert_to_conll(sentences, "parsed.conll")
