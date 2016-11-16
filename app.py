import pickle
from collections import defaultdict

from flask import Flask, jsonify, request

from settings import *

# Autocomplete
from autocomplete_model import autocomplete_query
from settings import min_prob_suggestion, model_order, numb_suggestions

# Initialize the Flask application
app = Flask(__name__)

# load the N-grams
ngrams_freqs = defaultdict(dict)
for N in [1, 2, 3]:
    filename = app_path+"/ngrams/"+str(N)+"-grams.pickle"
    with open(filename, "rb") as f:
        ngrams_freqs[N] = pickle.load(f)

# convert the N-gram dictionaries into numpy arrays
ngrams_keys = defaultdict(str)
for N in [1, 2, 3]:
    ngrams_keys[N] = list(ngrams_freqs[N].keys())

total_counts = [sum(ngrams_freqs[N].values()) for N in [1, 2, 3]]

# autocomplete endpoint that doesn't require login
# can be used for testing the speed
@app.route("/complete")
def _autocomplete_():
    search = request.args.get("text", "", type=str)
    results, probs = autocomplete_query(search, ngrams_keys, ngrams_freqs, total_counts, n_candidates=numb_suggestions, n_model=model_order, min_prob_suggestion=min_prob_suggestion)
    # print(results, probs)
    return jsonify(results=results)

if __name__ == "__main__":
    app.run(
        host=bind_ip,
        port=bind_port,
        debug=debug
    )

