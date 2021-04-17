import os
import sys

from flask import Flask, request, jsonify, render_template, redirect

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import tensorflow as tf
import logging
import pandas as pd
from simpletransformers.ner import NERModel

app = Flask(__name__)

global graph
graph = tf.get_default_graph()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        test_sents = pd.read_csv(request.files.get('file'))
    aspect_model = NERModel("bert", "/Users/mutaz/Desktop/Mutaz Thesis bert/hotel_reviews", use_cuda=False,
                            labels=["B-A", "I-A", "O"],
                            args={"use_cuda": False,
                                  "save_eval_checkpoints": False,
                                  "save_steps": -1,
                                  "output_dir": "MODEL",
                                  'overwrite_output_dir': True,
                                  "save_model_every_epoch": False,
                                  })

    predictions, raw_outputs = aspect_model.predict(test_sents["sentence"])
    pred = [[tag__ for word_ in s for word__, tag__ in word_.items()] for s in [sentence_ for sentence_ in predictions]]
    print(pred)
    # connect(test_sents, aspects_prds)
    return redirect('https://dub01.online.tableau.com/#/site/absa/views/absa_project/MAIN?:iid=20&:original_view=y')
    # return render_template('index2.html', data_dict=d, data_=len(all_aspects), sentences = test_sents["sentence"].values, df=final_df)


@app.route('/results', methods=['POST'])
def results():
    data = request.get_json(force=True)
    return jsonify(data)


if __name__ == '__main__':
    # graph = tf.get_default_graph()
    app.run(debug=True, threaded=False)
