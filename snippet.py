import json
import os
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
class snippet:
    def __init__(self):
        self.file_url_map = json.load(open(os.path.join(".","WEBPAGES_RAW", "bookkeeping.json")), encoding="utf-8")
        self.snippet_dict= {}
    def get_snippet(self):
        return self.snippet_dict
    def build_snippet(self):
        tokenizer = RegexpTokenizer(r'([0-9a-zA-Z]+)')
        for file_path in self.file_url_map.keys():
            word_count = 0
            single_snippet= ""
            file_id_list = file_path.split("/")
            file = open(os.path.join(".","WEBPAGES_RAW", file_id_list[0],file_id_list[1]),encoding="utf-8")
            content= file.read()
            parsed_content = BeautifulSoup(content,"html.parser")
            if parsed_content.find_all("p") != None:
                for each_p in parsed_content.find_all("p"):                  
                    single_snippet_list= tokenizer.tokenize(each_p.text.strip())
                    for i in single_snippet_list:
                        single_snippet = single_snippet+ " "+ i
                        word_count +=1
                        if word_count > 10:
                            break
                    if word_count> 10:
                        break
            else:
                single_snippet_list= tokenizer.tokenize(parsed_content.text.strip())
                for i in single_snippet_list:
                    single_snippet = single_snippet+ " "+ i
                    word_count +=1
                    if word_count > 10:
                        break
            if len(single_snippet) == 0:
                single_snippet_list= tokenizer.tokenize(parsed_content.text.strip())
                for i in single_snippet_list:
                    single_snippet = single_snippet+ " "+ i
                    word_count +=1
                    if word_count > 10:
                        break
            self.snippet_dict[file_path] = single_snippet
            file.close()

    def write_to_file(self):
        with open("snippet.json","w") as file:
            json.dump(self.snippet_dict,file)

if __name__ == "__main__":
    my_snippet = snippet()
    my_snippet.build_snippet()
    my_snippet.write_to_file()