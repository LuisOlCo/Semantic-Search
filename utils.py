import torch
import pandas as pd
import re
import string
import spacy

def max_pooling(model_output, attention_mask):
    token_embeddings = model_output[0] #First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    token_embeddings[input_mask_expanded == 0] = -1e9  # Set padding tokens to large negative value
    max_over_time = torch.max(token_embeddings, 1)[0]
    return max_over_time

def clean_selected_tweets(data):
    # Convert all text to lowercase
    data['tweet'] = data['tweet'].apply(lambda sentence: sentence.lower())
    # remove symbols, exclamation marks... --> '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    data['tweet'] = data['tweet'].apply(lambda sentence: re.sub('[%s]' % re.escape(string.punctuation), '', sentence))
    # remove numbers
    data['tweet'] = data['tweet'].apply(lambda sentence: re.sub('[0-9]', '', sentence))
    # remove line breaks special characters
    data['tweet'] = data['tweet'].apply(lambda sentence: re.sub('[\t\n\r\f\v]' , '', sentence))
    # Substitute multiple white spaces characters for one
    data['tweet'] = data['tweet'].apply(lambda sentence: re.sub(' +' , ' ', sentence))
    # From analysing the data afterwards the symbol ° has shown up several time
    data['tweet'] = data['tweet'].apply(lambda sentence: sentence.replace('°',''))

    nlp = spacy.load('en_core_web_sm')
    data['Tokenize']=data['tweet'].apply(lambda sentence: [token.lemma_ for token in list(nlp(sentence)) if not token.is_stop])
    return data

def get_bow_corpus(token_to_idx,chapter_counter):
    '''
    Transforms the chapter_counter dictionary into a list of tuple lists,
    this is the format required by Gensim to compute TD-IDF or LDA

    @Input: 1.- Dictionary tokens with their respectives index
            2.- Dictionary with the frequency of each word in each chapter
    '''
    bow_corpus = []
    for chapter in chapter_counter:
        chapter_list = []
        for word in chapter_counter[chapter]:
            chapter_list.append((token_to_idx[word],chapter_counter[chapter][word]))
        bow_corpus.append(chapter_list)
    return bow_corpus

def relevant_words_TDIDF_per_cluster(top_n_relevant_words,corpus_tfidf,idx_to_token):
    '''
    Returns back the top n most TD-IDF relevant words in a chapter
    @Input: 1.- number of most relevant words
            2.- TD-IDF values for each chapters
            3.- idx_to_token dictionary to identify the word
    '''
    top_n_relevant_words = 10
    values = []
    most_relevant_words = [None]*top_n_relevant_words

    for word in corpus_tfidf:
        values.append(word[1])

    values = sorted(values)
    top_values = values[-top_n_relevant_words:]

    for word in corpus_tfidf:
        if word[1] in top_values:
            index = top_values.index(word[1])
            most_relevant_words[index] = idx_to_token[word[0]]

    return most_relevant_words
