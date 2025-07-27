import os
import sys

from flask import Flask, request, jsonify, render_template, redirect

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import logging
import pandas as pd
from simpletransformers.ner import NERModel

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            test_sents = pd.read_csv(request.files.get('file'))
            
            # Get the model path
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            model_path = os.path.join(current_dir, "hotel_reviews_model")
            
            if not os.path.exists(model_path):
                return "Error: Model not found. Please train the model first using train_model.py", 500
            
            aspect_model = NERModel("bert", model_path, use_cuda=False,
                                    labels=["B-A", "I-A", "O"],
                                    args={"use_cuda": False,
                                          "save_eval_checkpoints": False,
                                          "save_steps": -1,
                                          "output_dir": "MODEL",
                                          'overwrite_output_dir': True,
                                          "save_model_every_epoch": False,
                                          })

            predictions, raw_outputs = aspect_model.predict(test_sents["sentence"])
            
            # Process predictions to extract aspects
            results = []
            for i, (sentence, prediction) in enumerate(zip(test_sents["sentence"], predictions)):
                aspects = []
                current_aspect = []
                
                # Handle the prediction format correctly
                if isinstance(prediction, list):
                    for word_dict in prediction:
                        for word, tag in word_dict.items():
                            if tag == "B-A":
                                if current_aspect:
                                    aspects.append(" ".join(current_aspect))
                                current_aspect = [word]
                            elif tag == "I-A":
                                current_aspect.append(word)
                            else:  # O
                                if current_aspect:
                                    aspects.append(" ".join(current_aspect))
                                    current_aspect = []
                else:
                    for word, tag in prediction.items():
                        if tag == "B-A":
                            if current_aspect:
                                aspects.append(" ".join(current_aspect))
                            current_aspect = [word]
                        elif tag == "I-A":
                            current_aspect.append(word)
                        else:  # O
                            if current_aspect:
                                aspects.append(" ".join(current_aspect))
                                current_aspect = []
                
                if current_aspect:
                    aspects.append(" ".join(current_aspect))
                
                results.append({
                    "sentence": sentence,
                    "aspects": aspects,
                    "num_aspects": len(aspects)
                })
            
            # Calculate summary statistics
            total_aspects = sum(result["num_aspects"] for result in results)
            avg_aspects = round(total_aspects / len(results), 1) if results else 0
            
            # Check if it's an AJAX request (for the new interface)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    "predictions": predictions,
                    "sentences": test_sents["sentence"].tolist(),
                    "results": results,
                    "summary": {
                        "total_reviews": len(results),
                        "total_aspects": total_aspects,
                        "avg_aspects": avg_aspects
                    }
                })
            else:
                # For traditional form submission, render results page
                return render_template('results.html', 
                                     data_=results, 
                                     total_aspects=total_aspects, 
                                     avg_aspects=avg_aspects)
            
        except Exception as e:
            return f"Error processing file: {str(e)}", 500


@app.route('/analyze_sentence', methods=['POST'])
def analyze_sentence():
    """Analyze a single sentence for aspects."""
    try:
        data = request.get_json()
        sentence = data.get('sentence', '').strip()
        
        if not sentence:
            return jsonify({"error": "No sentence provided"}), 400
        
        # Get the model path
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(current_dir, "hotel_reviews_model")
        
        if not os.path.exists(model_path):
            return jsonify({"error": "Model not found. Please train the model first using train_model.py"}), 500
        
        aspect_model = NERModel("bert", model_path, use_cuda=False,
                                labels=["B-A", "I-A", "O"],
                                args={"use_cuda": False,
                                      "save_eval_checkpoints": False,
                                      "save_steps": -1,
                                      "output_dir": "MODEL",
                                      'overwrite_output_dir': True,
                                      "save_model_every_epoch": False,
                                      })

        predictions, raw_outputs = aspect_model.predict([sentence])
        prediction = predictions[0]
        
        # Extract aspects from prediction
        aspects = []
        current_aspect = []
        
        # Handle the prediction format correctly
        if isinstance(prediction, list):
            for word_dict in prediction:
                for word, tag in word_dict.items():
                    if tag == "B-A":
                        if current_aspect:
                            aspects.append(" ".join(current_aspect))
                        current_aspect = [word]
                    elif tag == "I-A":
                        current_aspect.append(word)
                    else:  # O
                        if current_aspect:
                            aspects.append(" ".join(current_aspect))
                            current_aspect = []
        else:
            for word, tag in prediction.items():
                if tag == "B-A":
                    if current_aspect:
                        aspects.append(" ".join(current_aspect))
                    current_aspect = [word]
                elif tag == "I-A":
                    current_aspect.append(word)
                else:  # O
                    if current_aspect:
                        aspects.append(" ".join(current_aspect))
                        current_aspect = []
        
        if current_aspect:
            aspects.append(" ".join(current_aspect))
        
        return jsonify({
            "sentence": sentence,
            "aspects": aspects,
            "num_aspects": len(aspects)
        })
        
    except Exception as e:
        return jsonify({"error": f"Error analyzing sentence: {str(e)}"}), 500


@app.route('/results', methods=['POST'])
def results():
    data = request.get_json(force=True)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True, threaded=False, host='0.0.0.0', port=5003) 