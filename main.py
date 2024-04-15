import os

from calculations import calculate_term_frequency, calculate_inverse_document_frequency, tf_idf_cosine_similarity
from download_and_save import download


def load_documents(documents_directory):
    documents = {}
    for document_name in os.listdir(documents_directory):
        if document_name.endswith('.txt'):
            with open(documents_directory + document_name, 'r', encoding='utf-8') as file:
                documents[document_name] = file.read()
    return documents


def main(download_docks=False):
    if download_docks:
        download()
    documents = load_documents('./wikipedia_pages/')
    term_frequency = {}

    for document_name, document_data in documents.items():
        term_frequency[document_name] = calculate_term_frequency(document_data)
    idf = calculate_inverse_document_frequency(documents)

    first_doc_name = list(documents.keys())[0]
    last_doc_name = list(documents.keys())[-1]

    tf_idf_cosine_sim_to_first = {}
    for document_name, tf_dict in term_frequency.items():
        if document_name == first_doc_name:
            continue
        tf_idf_cosine_sim_to_first[document_name] = tf_idf_cosine_similarity(term_frequency[first_doc_name], tf_dict,
                                                                             idf)

    tf_idf_cosine_sim_to_last = {}
    for document_name, tf_dict in term_frequency.items():
        if document_name == last_doc_name:
            continue
        tf_idf_cosine_sim_to_last[document_name] = tf_idf_cosine_similarity(term_frequency[last_doc_name], tf_dict, idf)

    sorted_idf = sorted(idf.items(), key=lambda x: x[1], reverse=True)
    sorted_tf = {name: sorted(tf.items(), key=lambda x: x[1], reverse=True) for name, tf in term_frequency.items()}
    most_similar_to_first = max(tf_idf_cosine_sim_to_first, key=tf_idf_cosine_sim_to_first.get)
    most_similar_to_last = max(tf_idf_cosine_sim_to_last, key=tf_idf_cosine_sim_to_last.get)
    print('done!')


if __name__ == '__main__':
    main()
