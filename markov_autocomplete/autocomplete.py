import re
import os
import pickle
import numpy as np
from nltk import ngrams
from collections import Counter

class Autocomplete():
    """
To train the autocomplete with your own data you need to have a list of sentences
and pass it as an argument of the class.

For example we can use the first two paragraphs from Robinson Crusoe

from markov_autocomplete.autocomplete import Autocomplete

sentences = ['''I WAS born in the year 1632, in the city of York, of a good family,\
though not of that country, my father being a foreigner of Bremen,\
who settled first at Hull. He got a good estate by merchandise,\
and leaving off his trade, lived afterwards at York,\
from whence he had married my mother, whose relations were named Robinson,\
a very good family in that country, and from whom I was called Robinson Kreutznaer;\
but, by the usual corruption of words in England, we are now called - nay we call\
ourselves and write our name - Crusoe; and so my companions always called me.",\
"I had two elder brothers, one of whom was lieutenant-colonel to an English\
regiment of foot in Flanders, formerly commanded by the famous Colonel Lockhart,\
and was killed at the battle near Dunkirk against the Spaniards. What became of my\
second brother I never knew, any more than my father or mother knew what became of me.''']

ac = Autocomplete(model_path="ngram",
                  sentences=sentences,
                  n_model=3,
                  n_candidates=10,
                  match_model="middle",
                  min_freq=0,
                  punctuations="",
                  lowercase=True)

ac.predictions("country")
    """

    def __init__(self, model_path="./", sentences=None, n_model=3, n_candidates=10, match_model="middle",
                 min_freq=5, punctuations="""!"#$%&\'()*+,./:;<=>?@[\\]^_{|}~""", lowercase=True):
        # Model parameters
        # order of the n-gram to use for the autocomplete
        self.n_model = n_model
        # number of candidates suggested sentences to show
        self.n_candidates = n_candidates
        # path to the folder that stores the language model
        self.model_path = model_path
        # type of autocomplete model
        # `start`, `end` of `middle`
        self.match_model = match_model
        # do not consider ngrams that appear less than this value when generating the language model
        self.min_freq = min_freq
        # punctuations to remove
        self.punctuations = punctuations
        # lowercase the sentences?
        self.lowercase = lowercase
        # list of sentences to use to train the model
        if sentences is None:
            sentences = []
        self.sentences = sentences

        if not os.path.isdir(self.model_path):
            os.makedirs(self.model_path)

        # loading the language model
        for N in range(1, self.n_model + 1):
            filename = self.model_path + "/" + str(N) + "-grams.pickle"
            if not os.path.exists(filename):
                # if no language model is found, then it is computed
                # remove the dashes and the bendy apostrophe
                if not self.sentences:
                    raise Exception("You need to give a sample sentences to train the model!")
                self.compute_language_model()

        # ngrams_freqs is a dictionary whose keys are the ngrams labels and the values their counts
        self.ngrams_freqs = dict()
        for N in range(1, self.n_model + 1):
            filename = self.model_path + "/" + str(N) + "-grams.pickle"
            with open(filename, "rb") as f:
                self.ngrams_freqs[N] = pickle.load(f)

        # saving the ngrams_freqs keys in a separate dictionary
        self.ngrams_keys = dict()
        for N in range(1, self.n_model + 1):
            self.ngrams_keys[N] = list(self.ngrams_freqs[N].keys())

        # saving the total counts
        self.total_counts = [sum(self.ngrams_freqs[N].values()) for N in range(1, self.n_model + 1)]


    def get_ngrams(self, sentence, n=1):
        """
        Given a sentence returns a list of its n-grams
        """
        # remove punctuation
        if self.punctuations != "":
            sentence = re.sub('[' + self.punctuations + ']', ' ', sentence).strip()
        if self.lowercase:
            sentence = sentence.lower()
        # generate tokens
        if n > 1:
            sentence = [" ".join(n) for n in ngrams(sentence.split(), n, pad_right=True, right_pad_symbol='</END>')]
        else:
            sentence = sentence.split()
        # return the token
        # filter for empty string
        return list(filter(None, sentence))


    def compute_language_model(self):
        """
        Given a list of sentences compute the n-grams
        """
        if len(self.sentences) < 1e4:
            for N in range(1, self.n_model + 1):
                ngrams_list = []
                for sentence in self.sentences:
                    ngrams_sentence = self.get_ngrams(sentence, n=N)
                    ngrams_list.extend(ngrams_sentence)
                ngrams_freqs = Counter(ngrams_list)
                filename = self.model_path + "/" + str(N) + "-grams.pickle"
                with open(filename, "wb") as f:
                    pickle.dump(ngrams_freqs, f)
                print("Saving the %s-grams in %s" % (N, filename))
        else:
            try:
                from pyspark import SparkContext, SparkConf
            except:
                raise ImportError("pySpark not found! Please go to http://spark.apache.org/downloads.html")
            else:
                # If there are more than 100,000 sentences use Spark to compute the n-grams
                conf = SparkConf().setMaster("local").setAppName("ComputeLanguageModel")
                sc = SparkContext(conf=conf)
                sentences = sc.parallelize(self.sentences)

                for N in range(1, self.n_model + 1):
                    ngrams_freqs = sentences.flatMap(lambda x: self.get_ngrams(x, n=N))
                    ngrams_freqs = ngrams_freqs.map(lambda word: (word, 1)).reduceByKey(lambda x, y: x + y).collect()
                    ngrams_freqs.sort(key=lambda x: -x[1])
                    ngrams_freqs = list(filter(lambda x: x[1] > self.min_freq, ngrams_freqs))
                    ngrams_freqs = dict(ngrams_freqs)
                    filename = self.model_path + "/" + str(N) + "-grams.pickle"
                    with open(filename, "wb") as f:
                        pickle.dump(ngrams_freqs, f)
                        print("Saving the %s-grams in %s" % (N, filename))

                sc.stop()


    def compute_prob_sentence(self, sentence):
        """
        Given a sentence, return the log probability of that sentence using the n-gram approximation
        :return:
        """
        if sentence != "":
            total_prob = 0
            pieces = sentence.split()
            for i in range(1, len(pieces) + 1):
                if i <= self.n_model:
                    piece = pieces[:i]
                else:
                    piece = pieces[i - self.n_model:i]
                #
                ngram_model_to_use = len(piece)
                piece_lbl = " ".join(piece)
                if ngram_model_to_use in self.ngrams_freqs:
                    den = float(self.total_counts[ngram_model_to_use - 1])
                    num = float(self.ngrams_freqs[ngram_model_to_use].get(piece_lbl.lower(), 0))
                    piece_prob = np.log10(num/den)
                else:
                    return -np.inf
                total_prob += piece_prob
            return total_prob
        else:
            return -100


    def predictions(self, word):
        """
        Autocomplete a word or a sentence using a HMM (Hidden Markov Model)
        The HMM approximates the probability of a sentence with the n-gram model.
        For instance for a 4-word sentence and a 3-gram model we have

        P(w1 w2 w3 w4) = P(w1) * P(w2| w1) * P(w3| w1 w2) * P(w4| w1 w2 w3)

        :param word: the input word(s)
        """
        word = word.lower()
        parts = word.split()
        beginning = ""
        if len(parts) >= self.n_model:
            beginning = " ".join(parts[:-self.n_model + 1])
            word = " ".join(parts[-self.n_model + 1:])
        #
        if self.match_model == "start":
            candidates = np.array(list(filter(lambda x: x.startswith(word), self.ngrams_keys.get(self.n_model, ''))))
        elif self.match_model == "end":
            candidates = np.array(list(filter(lambda x: x.endswith(word), self.ngrams_keys.get(self.n_model, ''))))
        elif self.match_model == "middle":
            candidates = np.array(list(filter(None, [key if word in key else None for key in self.ngrams_keys.get(self.n_model, '')])))[::-1]
        else:
            raise Exception("match_model can only be `start`, `end` or `middle`")
        #
        if len(candidates) == 0:
            return [], []
        #
        predictions = []
        if len(candidates) >= 1:
            for i in range(len(candidates)):
                if beginning == "":
                    predictions.append(" ".join([beginning, candidates[i].replace("</END>", "").capitalize()]).strip())
                else:
                    predictions.append(" ".join([beginning.capitalize(), candidates[i].replace("</END>", "")]).strip())
        #
        predictions = np.array(predictions)
        probabilities = np.array(
            [self.compute_prob_sentence(sentence) for sentence in predictions])
        order = np.argsort(probabilities)[::-1]
        predictions = list(predictions[order][:self.n_candidates])
        probabilities = list(probabilities[order][:self.n_candidates])
        #
        return predictions, probabilities



