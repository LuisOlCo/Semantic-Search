from collections import Counter
import numpy as np
import matplotlib.pyplot as plt

class Vocabulary():

    def __init__(self):
        self.counter_global = {}
        self.token_to_idx = {}
        self.idx_to_token = {}
        self.length = 0
        self.chapter_counter = {}
        self.most_common_words_dict = {}

    def update_vocabulary(self,token,chapter):
        '''
        Updates the vocabulary and the counters given one token
        '''
        self._add_token(token)
        self._update_counter(token,self.counter_global)
        self._update_chapter_counter(token,chapter)

    def _add_token(self,token):
        '''
        Builds a dictionary with all the words in the dataset
        '''
        if token not in self.token_to_idx:
            self.token_to_idx.update({token:self.length})
            self.idx_to_token.update({self.length:token})
            self.length += 1

    def _update_counter(self,token,counter):
        '''
        Tracks the frequency of each word in the dataset
        '''
        if token in counter:
            counter[token] += 1
        else:
            counter.update({token:1})

    def _update_chapter_counter(self,token,chapter):
        '''
        Builds a dictionary tracking the frequency of words in each chapter
        '''
        if chapter in self.chapter_counter:
            self._update_counter(token,self.chapter_counter[chapter])
        else:
            self.chapter_counter.update({chapter:{}})

    def most_common_words_per_cluster(self,chapters,n):
        '''
        Returns a pie chart for every chapter with the top n most common words
        '''
        # list of tuples with the most common word and their frequencies
        for chapter in chapters:
            words = Counter(self.chapter_counter[chapter]).most_common(n)
            words_dict = {}
            for word in words:
                words_dict[word[0]] = word[1]

            # from the tuple to a dictionary
            top_words = []
            freqs = []
            for x, y in words_dict.items():
                top_words.append(x)
                freqs.append(y)

            # plot
            plt.figure(figsize=(30,10))
            plt.title('Chapter: %d' %chapter, fontsize=30)
            plt.pie(freqs, labels=top_words,wedgeprops=dict(width=.7), autopct='%1.0f%%', startangle= -20, textprops={'fontsize': 30})
            plt.axis('equal')
            plt.show()

    def more_frequent_words(self,chapters,n):
        '''
        Returns the n more frequent words in each chapter with their corresponding frq in each chapter
        '''
        # First get a dictionary with the most common words in each chapter, the value
        # of every key would be a list, that we fill with the freq of the word in each chapter
        most_common_words = []
        for chapter in chapters:
            words = Counter(self.chapter_counter[chapter]).most_common(n)
            for word in words:
                if word[0] in self.most_common_words_dict:
                    pass
                else:
                    self.most_common_words_dict.update({word[0]:[]})
                    most_common_words.append(word[0])

        # Secondly we add to the list for each word their freq in each chapter, so we can
        # keep track of the freq over the book
        for chapter in chapters:
            for word in most_common_words:
                if word in self.chapter_counter[chapter]:
                    self.most_common_words_dict[word].append(self.chapter_counter[chapter][word])
                else:
                    self.most_common_words_dict[word].append(0)

        return self.most_common_words_dict

    def more_frequent_words_cluster_series_graph(self):
        '''
        Plots the freq of the most frequent words along the chapters in the document
        '''
        for k,v in self.most_common_words_dict.items():
            x = np.array(v)
            t = np.array(range(1,len(x)+1))
            plt.plot(t,x)
            plt.title(k)
            plt.ylabel ('Frequency')
            plt.xlabel ('Chapters')
            plt.show()

    def most_used_word(self):
        '''
        Returns the most used word in the corpus
        '''
        global_freq = {}
        max_frq = 0
        for key,val in self.most_common_words_dict.items():
            if sum(val) > max_frq:
                max_frq = sum(val)
                most_used_word = key
        return most_used_word
