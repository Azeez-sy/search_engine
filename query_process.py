from documents import DocumentStore
from index import BaseIndex
from tokenizer import tokenize, quotation_parser
from tf_idf_index import TfIdfIndex
from tf_idf_inverted_index import TfIdfInvertedIndex
from priority_search import PhraseSearch
import json
import sys


def not_implemented_yet():
    print("Outside of demo: this has not be implemented")
    sys.exit(0)


def case_handler(query_str, number_of_results):
    unquoted_tokens, quoted_tokens = quotation_parser(query_str)

    if len(unquoted_tokens) == 0 and len(quoted_tokens) == 0:
        not_implemented_yet()
        # handle_empty_querie()

    if len(unquoted_tokens) == 0 and len(quoted_tokens) != 0:
        not_implemented_yet()
        # return PhraseSearch.handle_quoted_query(quoted_tokens, number_of_results)

    if len(unquoted_tokens) != 0 and len(quoted_tokens) == 0:
        not_implemented_yet()
        # return PhraseSearch.handle_unquoted_query(unquoted_tokens, number_of_results)

    if len(unquoted_tokens) != 0 and len(quoted_tokens) != 0:
        return PhraseSearch.handle_mixed_query(unquoted_tokens, quoted_tokens, number_of_results)


def user_interface():
    query_str = input("Enter your query: ")
    number_of_results = input("Enter number of results desired: ")
    document_ids = case_handler(query_str, number_of_results)

    print("Document IDs returned by the search:")
    for doc_id in document_ids:
        print(doc_id)


def preprocess_query(query_str: str):
    return tokenize(query_str)


def format_out(results: list[str], document_store: DocumentStore, unused_processed_query) -> str:
    output_string = ''
    for doc_id in results:
        doc = document_store.get_by_doc_id(doc_id)
        output_string += f'({doc.doc_id}) {doc.text}\n\n'
    return output_string


def load_stopwords(stopwords_file):
    if stopwords_file:
        with open(stopwords_file, 'r') as file:
            stopwords = json.load(file)
        return list(stopwords)
    return list()


class QueryProcess:
    def __init__(self, document_store: DocumentStore, index: BaseIndex, stop_words = None):
        self.document_store = document_store
        self.index = index
        #self.stopwords = load_stopwords(stop_words) if stop_words else list()
        self.stopwords = "stop_words.json"

    def search(self, query: str, number_of_results: int) -> str:
        processed_query = preprocess_query(query)
        if self.stopwords:
            processed_query = [term for term in processed_query if term not in self.stopwords]
        results = self.index.search(processed_query, number_of_results)
        return format_out(results, self.document_store, processed_query)




# qp1 = QueryProcess(DocumentStore, TfIdfIndex(), )
# qp2 = QueryProcess(DocumentStore, TfIdfInvertedIndex())
# qp3 = QueryProcess(DocumentStore, TfIdfInvertedIndex(), "stop_words.json")
#
# result1 = timeit.timeit(lambda: qp1.search(query='credit card', number_of_results=10), number=100)
# result2 = timeit.timeit(lambda: qp2.search(query='credit card', number_of_results=10), number=100)
# result3 = timeit.timeit(lambda: qp3.search(query='credit card', number_of_results=10), number=100)
#
# print(result1)
# print(result2)
# print(result3)