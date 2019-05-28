from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
import math
import json
import os
class SearchEngine:
    def __init__(self,db):
        self.query = ""
        self.db= db
        self.number_of_doc = 37497
        self.return_doc = []
    
    def process_query(self):
        tokenizer = RegexpTokenizer(r'([0-9a-zA-Z]+)')
        wnl = WordNetLemmatizer()
        query_dict= dict()
        for word in tokenizer.tokenize((self.query).strip().lower()):
            word = wnl.lemmatize(word)
            if not word in query_dict:
                query_dict[word] = 1
            else:
                query_dict[word] +=1
        query_length = 0
        for word in query_dict.keys():
            if word in self.db.keys():
                idf = self.number_of_doc/len(self.db[word])
                query_dict[word]= (1+math.log10(query_dict[word]))*math.log10(idf)
            else:
                idf = 0
                query_dict[word]= 0
            query_length += query_dict[word]**2
        query_length = math.sqrt(query_length)
        for word in query_dict.keys():
            query_dict[word]= query_dict[word]/query_length
        return query_dict
    
    def calculate_cos(self):
        query_dict = self.process_query()
        cos_dict = {}
        for word in query_dict.keys():
            if word in self.db:
                doc_length = 0
                for doc_id in self.db[word].keys():
                    doc_length += self.db[word][doc_id][2]**2
                doc_length = math.sqrt(doc_length)
                for doc_id in self.db[word].keys():
                    if doc_id in cos_dict:
                        cos_dict[doc_id]+= (self.db[word][doc_id][2]/doc_length) * query_dict[word]
                    else:
                        cos_dict[doc_id] = (self.db[word][doc_id][2]/doc_length) * query_dict[word]
        return cos_dict 
    def rank_by_cos(self):
        score = self.calculate_cos()
        return sorted(score.items(), key=lambda x: (-x[1],x[0]))
    def print_results(self,query):
        sum_result = 0
        list_passed_to_tk = []
        self.query = query
        results = self.rank_by_cos()
        if len(results) == 0:
            print("No results found")
        else:
            file_url_dict = json.load(open(os.path.join(".","WEBPAGES_RAW", "bookkeeping.json")), encoding="utf-8")
            for doc in results:
                sum_result +=1
                self.return_doc.append(doc[0])
                list_passed_to_tk.append(file_url_dict[doc[0]])
                if sum_result ==20:
                    break
        return list_passed_to_tk
    
    def get_return_doc(self):
        return self.return_doc