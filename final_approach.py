import re
import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.corpus import words
from nltk.stem import PorterStemmer

# Takes complete word content and string to get all matches 
def return_all_line_occurrence_of_substring(complete_word_content, string_to_match=""):
    # Returns a list of all string match lines that contains "string_to_match" anywhere in a line
    return re.findall("^.*{}.*$".format(string_to_match), complete_word_content, re.MULTILINE)

# Takes complete word content and string to get all matches 
def match_string_in_the_end_of_line(complete_word_content, string_to_match=""):
    # Returns a list of all string match lines that contains "string_to_match" at the end of the line
    return re.findall("^.*{}$".format(string_to_match), complete_word_content, re.MULTILINE)

# Takes complete word content and string to get all matches 
def return_all_single_characters(complete_word_content):
    # Returns a list of all single characters in the word_content passed
    return re.findall("^.$", complete_word_content, re.MULTILINE)


def read_bert_file_and_return_words():
    complete_word_content = ""
    with open('BERT-vocab.txt') as bert_file:
        complete_word_content = bert_file.read()
    bert_file.close()
    return complete_word_content


def return_valid_words(complete_word_content):
    list_of_words_to_exclude = []
    list_of_words_to_exclude += return_all_single_characters(complete_word_content)
    list_of_words_to_exclude += return_all_line_occurrence_of_substring(complete_word_content,'\[')
    list_of_words_to_exclude += return_all_line_occurrence_of_substring(complete_word_content, '#')
    list_of_words_to_exclude += return_all_line_occurrence_of_substring(complete_word_content, '[0-9]')

    complete_word_list = []
    for indv_line in complete_word_content.splitlines():
        if indv_line != "":
            complete_word_list.append(indv_line)
    return list(set(complete_word_list) - set(list_of_words_to_exclude))


def lemmatize_and_return_valid_words(valid_word_list):
    hash_of_lemmatized_words = {}
    lemma = nltk.wordnet.WordNetLemmatizer()
    for indv_word in valid_word_list:
        lemmatized_word = lemma.lemmatize(indv_word)
        if lemmatized_word not in hash_of_lemmatized_words:
            hash_of_lemmatized_words[lemmatized_word] = 1
        else:
            hash_of_lemmatized_words[lemmatized_word] += 1
    return list(hash_of_lemmatized_words.keys())


def return_valid_list_of_stems(valid_words_after_lemmatization):
    hash_of_stems = {}
    porter_stemmer = PorterStemmer()
    for indv_word in valid_words_after_lemmatization:
        stem_word = porter_stemmer.stem(indv_word)
        if stem_word not in hash_of_stems:
            hash_of_stems[stem_word] = 1
        else:
            hash_of_stems[stem_word] += 1
    return list(hash_of_stems.keys())


def return_final_list_of_valid_words(valid_words_after_stemming):
    final_hash_of_valid_words = {}
    exhaustive_list_of_words = list(set(words.words()))
    for indv_word in valid_words_after_stemming:
        if len(indv_word)==2:
            if indv_word not in final_hash_of_valid_words and indv_word in exhaustive_list_of_words:
                final_hash_of_valid_words[indv_word] = 1
        else:
                final_hash_of_valid_words[indv_word] = 1       
    return list(final_hash_of_valid_words.keys())


def main():
    complete_word_content = read_bert_file_and_return_words()
    valid_words = return_valid_words(complete_word_content)
    print("valid_words - {}".format(len(valid_words)))
    valid_words_after_lemmatization = lemmatize_and_return_valid_words(valid_words)
    print("valid_words_after_lemmatization - {}".format(len(valid_words_after_lemmatization)))
    valid_words_after_stemming = return_valid_list_of_stems(valid_words_after_lemmatization)
    print("valid_words_after_stemming - {}".format(len(valid_words_after_stemming)))
    final_list_of_valid_words = return_final_list_of_valid_words(valid_words_after_stemming)
    print("final_list_of_valid_words - {}".format(len(final_list_of_valid_words)))

if __name__ == "__main__":
    main()