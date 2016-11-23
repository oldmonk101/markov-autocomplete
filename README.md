# Markov Autocomplete

Hidden Markov Model to generate autocomplete suggestion.

# Installation

Download and install the last spark distribution
Export variables, e.g.:

```bash
export SPARK_HOME=/opt/spark
export PYTHONPATH=$SPARK_HOME/python/lib/py4j-0.8.2.1-src.zip:$PYTHONPATH
```

Install requirements:
```bash
pip install -r requirements.txt
```

Install the package:
```bash
python setup.py install
```

# How To Use

The model can be trained with your own list of sentences.

For instance, if we want to train using the first two paragraphs of Robinson Crusoe 

```
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

ac = Autocomplete(model_path = "ngram",
                  sentences = sentences,
                  n_model=3,
                  n_candidates=10,
                  match_model="middle",
                  min_freq=0,
                  punctuations="",
                  lowercase=True)

ac.predictions("country")
```


## How it works
Given an input string that consists of `N` words `w_1, ..., w_N`, the model predicts the following word, `w_{N+1}`, from the language model.

The most probable candidate for `w_{N+1}` is computed by maximazing

```
P (w_{N+1} | w_N, ..., w_{N - O + 2})
```

where `O` is the order of the model.

Once the best candidate is computed the probability of the whole sentence is approximated with an n-gram model

```
P (w_1, ..., w_N, w_{N+1}) = PROD_i P (w_i | w_{i-N-1}, ..., w_{i-1})
```

For instance, for a 2-gram model we have

```
P( w1, w2, w3, w4) = P(w1) P(w2|w1) P(w3|w2) P(w4|w3)
```

On the other hand, for a 3-gram model we have

```
P( w1, w2, w3, w4) = P(w1) P(w2|w1) P(w3|w1, w2) P(w4|w2, w3)
```

Higher-order model will be more precise, but at the expense of generating a large list of n-grams, which may negatively impact on storage space and computational time.

If the input string contains less words than the order of the model, the autocomplete will compute the most probably n-gram of the same order of the model.

## References

* [1] https://en.wikipedia.org/wiki/N-gram
* [2] https://en.wikipedia.org/wiki/Hidden_Markov_model
* [3] https://en.wikipedia.org/wiki/Language_model