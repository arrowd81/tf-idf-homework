import math
import re


def calculate_term_frequency(document: str):
    words = re.split(r'[^a-zA-Z0-9\u0600-\u06FF]', document)
    word_count = {}
    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    total_words = len(words)
    return {word: count / total_words for word, count in word_count.items()}


def calculate_inverse_document_frequency(documents: dict):
    words = {}
    words_in_documents = {}
    total_documents = len(documents)
    for document_name, data in documents.items():
        document_words = set(re.split(r'[^a-zA-Z0-9\u0600-\u06FF]', data))  # to remove duplicates
        words_in_documents[document_name] = document_words
        for word in document_words:
            if word in words:
                words[word] += 1
            else:
                words[word] = 1
    return {word: math.log(total_documents / count) for word, count in words.items()}, words_in_documents


def cosine_similarity(dict1, dict2):
    all_keys = set(dict1.keys()).union(dict2.keys())

    vector1 = [dict1.get(key, 0) for key in all_keys]
    vector2 = [dict2.get(key, 0) for key in all_keys]

    dot_product = sum(x * y for x, y in zip(vector1, vector2))

    magnitude1 = math.sqrt(sum(x ** 2 for x in vector1))
    magnitude2 = math.sqrt(sum(x ** 2 for x in vector2))

    if magnitude1 == 0 or magnitude2 == 0:
        return 0  # Handle division by zero
    else:
        return dot_product / (magnitude1 * magnitude2)
