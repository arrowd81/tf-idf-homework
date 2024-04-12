import os

from calculations import calculate_term_frequency, calculate_inverse_document_frequency, cosine_similarity
from download_and_save import download


def load_documents(documents_directory):
    documents = {}
    for document_name in os.listdir(documents_directory):
        if document_name.endswith('.txt'):
            with open(documents_directory + document_name, 'r', encoding='utf-8') as file:
                documents[document_name.encode().decode()] = file.read()
    return documents


def main(download_docks=False):
    zip()
    if download_docks:
        download()
    documents = load_documents('./wikipedia_pages/')
    term_frequency = {}

    for document_name, document_data in documents.items():
        term_frequency[document_name] = calculate_term_frequency(document_data)
    idf, words_in_documents = calculate_inverse_document_frequency(documents)

    first_doc_name = list(documents.keys())[0]
    last_doc_name = list(documents.keys())[-1]

    tf_cosine_sim_to_first = {}
    for document_name, tf_dict in term_frequency.items():
        if document_name == first_doc_name:
            continue
        tf_cosine_sim_to_first[document_name] = cosine_similarity(term_frequency[first_doc_name], tf_dict)

    tf_cosine_sim_to_last = {}
    for document_name, tf_dict in term_frequency.items():
        if document_name == last_doc_name:
            continue
        tf_cosine_sim_to_last[document_name] = cosine_similarity(term_frequency[last_doc_name], tf_dict)

    idf_cosine_sim_to_first = {}
    for document_name in documents.keys():
        if document_name == first_doc_name:
            continue
        idf_cosine_sim_to_first[document_name] = cosine_similarity(
            {word: idf[word] for word in words_in_documents[first_doc_name]},
            {word: idf[word] for word in words_in_documents[document_name]})

    idf_cosine_sim_to_last = {}
    for document_name in documents.keys():
        if document_name == last_doc_name:
            continue
        idf_cosine_sim_to_last[document_name] = cosine_similarity(
            {word: idf[word] for word in words_in_documents[last_doc_name]},
            {word: idf[word] for word in words_in_documents[document_name]})

    sorted_idf = sorted(idf.items(), key=lambda x: x[1], reverse=True)
    sorted_tf = {name: sorted(tf.items(), key=lambda x: x[1], reverse=True) for name, tf in term_frequency.items()}
    most_similar_to_first_tf = max(tf_cosine_sim_to_first, key=tf_cosine_sim_to_first.get)
    most_similar_to_last_tf = max(tf_cosine_sim_to_last, key=tf_cosine_sim_to_last.get)
    most_similar_to_first_idf = max(idf_cosine_sim_to_first, key=idf_cosine_sim_to_first.get)
    most_similar_to_last_idf = max(idf_cosine_sim_to_last, key=idf_cosine_sim_to_last.get)
    print('done!')


if __name__ == '__main__':
    main()
