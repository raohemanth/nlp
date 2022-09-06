import re

def read_bert_file_and_return_content():
    complete_word_content = ""
    with open('BERT-vocab.txt') as bert_file:
        complete_word_content = bert_file.read()
    bert_file.close()

    with open('BERT-vocab.txt') as bert_file:
        lines = bert_file.readlines()
        complete_word_list = [line.strip() for line in lines]
    return {"complete_word_content": complete_word_content,"complete_word_list": complete_word_list}

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

def non_stem_word_elimination(word_content, word_list):
    nouns_to_eliminates = ["age","al","ance","ence","dom","ee","er","or","hood","ism","ist","ity","ty","ment","ness","ry","ship","sion","tion","xion"]
    adverbs_to_eliminate = ["ly", "ward","wards", "wise"]
    adjectives_to_eliminate = ["able","ible","al","en","ese","ful","i","ic","ish","ive","ian","less","ly","ous","y"]
    verbs_to_elimate = ["ate","en","ify","ise","ize","ing"]

    list_of_suffixes_to_eliminate= nouns_to_eliminates + adverbs_to_eliminate + adjectives_to_eliminate + verbs_to_elimate
    list_of_words_matched = []
    words_to_consider = []
    for indv_adverb in list_of_suffixes_to_eliminate:
        list_of_words_matched = match_string_in_the_end_of_line(word_content, indv_adverb)
        list_of_words_matched=list(set(list_of_words_matched))
        for indv_match_word in list_of_words_matched:
            temp_copy_of_word_to_check_for_match = indv_match_word
            word_to_check_for_match = indv_match_word.replace(indv_adverb, "")
            while len(word_to_check_for_match) > 1:
                if word_to_check_for_match in word_list:
                    words_to_consider.append(temp_copy_of_word_to_check_for_match)
                    break
                if "{}e".format(word_to_check_for_match) in word_list:
                    words_to_consider.append(temp_copy_of_word_to_check_for_match)
                    break
                else:
                    word_to_check_for_match = word_to_check_for_match[:-1]
    return list(set(words_to_consider))

def main():
    output = read_bert_file_and_return_content()
    complete_word_content = output["complete_word_content"]
    complete_word_list = output["complete_word_list"]
    current_word_content = output["complete_word_content"]
    current_list_of_valid_words = output["complete_word_list"]
    list_of_words_to_exclude = []
    list_of_words_to_exclude += return_all_single_characters(complete_word_content)
    list_of_words_to_exclude += return_all_line_occurrence_of_substring(complete_word_content,'\[')
    list_of_words_to_exclude += return_all_line_occurrence_of_substring(complete_word_content, '#')
    list_of_words_to_exclude += return_all_line_occurrence_of_substring(complete_word_content, '[0-9]')
    current_list_of_valid_words = list(set(complete_word_list) - set(list_of_words_to_exclude))
    for indv_word_to_exclude in list_of_words_to_exclude:
        current_word_content= current_word_content.replace("\n{}\n".format(indv_word_to_exclude),"\n")
    list_of_words_to_exclude += non_stem_word_elimination(current_word_content, current_list_of_valid_words)
    final_list_of_valid_words = set(complete_word_list) - set(list_of_words_to_exclude)
    final_list_of_valid_words = [x for x in final_list_of_valid_words if x]
    print(len(final_list_of_valid_words))
    print(final_list_of_valid_words)
if __name__ == "__main__":
    main()