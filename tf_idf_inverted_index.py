import json
import math
from collections import defaultdict, Counter

from documents import TransformedDocument
from index import BaseIndex


def count_terms(terms: list[str]) -> Counter:
    return Counter(terms)


class TfIdfInvertedIndex(BaseIndex):
    def __init__(self):
        # Mapping of terms to the number of documents they occur in.
        self.doc_counts = Counter()
        # Mapping doc_id to term counts in the corresponding document.
        self.term_to_doc_id_tf_scores = defaultdict(dict)
        self.total_documents_count = 0

    def write(self, path: str):
        with open(path, 'w') as fp:
            fp.write(json.dumps({
                '__metadata__': {
                    'doc_counts': [
                        {
                            'term': term,
                            'count': count
                        }
                        for term, count in self.doc_counts.items()
                    ]
                }
            }) + '\n')
            for doc_id, counts in self.term_to_doc_id_tf_scores.items():
                fp.write(json.dumps({
                    'doc_id': doc_id,
                    'counts': [
                        {
                            'term': term,
                            'count': count
                        }
                        for term, count in counts.items()
                    ]
                }) + '\n')

    def add_document(self, doc: TransformedDocument):
        term_counts = count_terms(doc.terms)
        self.doc_counts.update(term_counts.keys())
        doc_length = len(doc.terms)
        self.total_documents_count += 1

        # Mapping from doc_ids to term counts in the corresponding document.
        for term, count in term_counts.items():
            self.term_to_doc_id_tf_scores[term][doc.doc_id] = count / doc_length

    def term_frequency(self, term, doc_id):
        return self.term_to_doc_id_tf_scores[term].get(doc_id, 0.0)

    def inverse_document_frequency(self, term):
        return math.log(len(self.term_to_doc_id_tf_scores) / self.doc_counts[term])

    def tf_idf(self, term, doc_id):
        return self.term_frequency(term, doc_id) * self.inverse_document_frequency(term)

    def combine_term_scores(self, terms: list[str], doc_id) -> float:
        return sum([self.tf_idf(term, doc_id) for term in terms])

    def search(self, processed_query: list[str], number_of_results: int) -> list[str]:
        matching_doc_ids = None

        for term in processed_query:
            term_doc_ids = set(self.term_to_doc_id_tf_scores.get(term, {}).keys())

            if matching_doc_ids is None:
                matching_doc_ids = term_doc_ids
            else:
                matching_doc_ids = matching_doc_ids.intersection(term_doc_ids)

        if matching_doc_ids is None:
            return []
        #these if blocks make it so if not ever query term in doc, then it just returns the whole thing

        scores = dict()
        for doc_id in matching_doc_ids:
            score = self.combine_term_scores(processed_query, doc_id)
            scores[doc_id] = score
        sorted_docs = sorted(matching_doc_ids, key=scores.get, reverse=True)
        return sorted_docs[:number_of_results]
