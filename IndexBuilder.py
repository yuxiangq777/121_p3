from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
#from nltk.corpus import stopwords
import math
import os
import json

class InvertedIndex:
    
    def __init__(self):
        #self.db = pymongo.MongoClient("mongodb+srv://yuxiangq:<password>@121p3-uczxe.mongodb.net/test?retryWrites=true").get_default_database()
        #self.InvertedIndex_collection = self.db["InvertedIndex"]
        self.InvertedIndex_collection = dict()
        self.file_url_map = json.load(open(os.path.join(".","WEBPAGES_RAW", "bookkeeping.json")), encoding="utf-8")
        self.number_of_file= 37497
        #self.stop_words = set(stopwords.words('english')) 
    def tokenize_file(self, file_id):
        tokenizer = RegexpTokenizer(r'([0-9a-zA-Z]+)')
        #stemmer = PorterStemmer()
        wnl = WordNetLemmatizer()
        word_index= 0
        file_id_list = file_id.split("/")
        file = open(os.path.join(".","WEBPAGES_RAW", file_id_list[0],file_id_list[1]),encoding="utf-8")
        content= file.read()
        parsed_content = BeautifulSoup(content,"html.parser")
        for s in parsed_content(["script","style"]):
            s.decompose()
        for word in tokenizer.tokenize(parsed_content.get_text().strip().lower()):
            #if not word in self.stop_words: 
            word = wnl.lemmatize(word)
            if word not in self.InvertedIndex_collection:
                self.InvertedIndex_collection[word]= dict()
                self.InvertedIndex_collection[word][file_id]=[1,[word_index],0]
            else:
                if file_id in self.InvertedIndex_collection[word]:
                    self.InvertedIndex_collection[word][file_id][0] +=1
                    self.InvertedIndex_collection[word][file_id][1].append(word_index)
                        
                else:
                    self.InvertedIndex_collection[word][file_id]=[1,[word_index],0]
            word_index+= 1
        for sentence in parsed_content.find_all("h1"):
            for word in tokenizer.tokenize(sentence.text.strip().lower()):
                word = wnl.lemmatize(word)
                if word in self.InvertedIndex_collection and file_id in self.InvertedIndex_collection[word]:
                    self.InvertedIndex_collection[word][file_id][0] += 3
        for sentence in parsed_content.find_all("h2"):
            for word in tokenizer.tokenize(sentence.text.strip().lower()):
                word = wnl.lemmatize(word)
                if word in self.InvertedIndex_collection and file_id in self.InvertedIndex_collection[word]:
                    self.InvertedIndex_collection[word][file_id][0] += 3
        for sentence in parsed_content.find_all("h3"):
            for word in tokenizer.tokenize(sentence.text.strip().lower()):
                word = wnl.lemmatize(word)
                if word in self.InvertedIndex_collection and file_id in self.InvertedIndex_collection[word]:
                    self.InvertedIndex_collection[word][file_id][0] += 3
        for sentence in parsed_content.find_all("b"):
            for word in tokenizer.tokenize(sentence.text.strip().lower()):
                word = wnl.lemmatize(word)
                if word in self.InvertedIndex_collection and file_id in self.InvertedIndex_collection[word]:
                    self.InvertedIndex_collection[word][file_id][0] += 1
        for sentence in parsed_content.find_all("strong"):
            for word in tokenizer.tokenize(sentence.text.strip().lower()):
                word = wnl.lemmatize(word)
                if word in self.InvertedIndex_collection and file_id in self.InvertedIndex_collection[word]:
                    self.InvertedIndex_collection[word][file_id][0] += 1
        del content
        del parsed_content
        file.close()
    def test(self):
        count =0 
        for file_id in self.file_url_map.keys():
            self.tokenize_file(file_id)
            count +=1
            if count == 100:
                break
        for word, posting_list in self.InvertedIndex_collection.items():
            for file_id, info in posting_list.items():
                info[2] = (1+math.log10(info[0]))*math.log10(self.number_of_file/len(posting_list))
    def process_all_file(self):
        for file_id in self.file_url_map.keys():
            self.tokenize_file(file_id)
        for word, posting_list in self.InvertedIndex_collection.items():
            for file_id, info in posting_list.items():
                info[2] = (1+math.log10(info[0]))*math.log10(self.number_of_file/len(posting_list))
    def write_to_file(self):
        with open("InvertedIndex.json","w") as file:
            json.dump(self.InvertedIndex_collection,file)

if __name__ == "__main__":
    build_index = InvertedIndex()
    build_index.process_all_file()
    build_index.write_to_file()
    print("finished with ", len(build_index.InvertedIndex_collection))