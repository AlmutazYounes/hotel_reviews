#!/usr/bin/env python3
"""
Demo script for Hotel Reviews Aspect-Based Sentiment Analysis
This script demonstrates how to use the trained model for predictions.
"""

import os
import pandas as pd
from simpletransformers.ner import NERModel

def load_model():
    """Load the trained model (based on custom Ara_DialectBERT)."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, "hotel_reviews_model")
    
    if not os.path.exists(model_path):
        print("Error: Model not found. Please train the model first using train_model.py")
        return None
    
    print("Loading model (trained on MutazYoune/Ara_DialectBERT)...")
    model = NERModel("bert", model_path, use_cuda=False,
                     labels=["B-A", "I-A", "O"],
                     args={"use_cuda": False,
                           "save_eval_checkpoints": False,
                           "save_steps": -1,
                           "output_dir": "MODEL",
                           'overwrite_output_dir': True,
                           "save_model_every_epoch": False,
                           })
    print("Model loaded successfully!")
    return model

def predict_aspects(model, sentences):
    """Predict aspects in the given sentences."""
    if model is None:
        return None
    
    print("Making predictions...")
    predictions, raw_outputs = model.predict(sentences)
    
    # Process predictions
    results = []
    for i, (sentence, prediction) in enumerate(zip(sentences, predictions)):
        aspects = []
        current_aspect = []
        
        # Handle the prediction format correctly
        if isinstance(prediction, list):
            # If prediction is a list of dictionaries
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
            # If prediction is a dictionary
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
    
    return results

def main():
    """Main demo function."""
    print("=" * 60)
    print("🏨 Hotel Reviews Aspect-Based Sentiment Analysis Demo")
    print("=" * 60)
    
    # Sample Arabic hotel reviews
    sample_reviews = [
        "الفندق رائع والخدمة ممتازة والغرف نظيفة",
        "الموقع جيد لكن الطعام سيء والسعر مرتفع",
        "الموظفين ودودين والمرافق حديثة والموقع ممتاز",
        "الغرف صغيرة والإنترنت بطيء لكن النظافة جيدة",
        "مطعم الفندق ممتاز والخدمة سريعة والغرف مريحة"
    ]
    
    print(f"\n📝 Sample Reviews ({len(sample_reviews)} reviews):")
    for i, review in enumerate(sample_reviews, 1):
        print(f"{i}. {review}")
    
    # Load model
    model = load_model()
    if model is None:
        return
    
    # Make predictions
    results = predict_aspects(model, sample_reviews)
    
    if results:
        print(f"\n🎯 Analysis Results:")
        print("-" * 60)
        
        total_aspects = 0
        for i, result in enumerate(results, 1):
            print(f"\nReview {i}: {result['sentence']}")
            print(f"  📊 Number of aspects: {result['num_aspects']}")
            if result['aspects']:
                print(f"  🏷️  Identified aspects:")
                for j, aspect in enumerate(result['aspects'], 1):
                    print(f"    {j}. {aspect}")
            else:
                print(f"  ❌ No aspects identified")
            total_aspects += result['num_aspects']
        
        print(f"\n📈 Summary:")
        print(f"  • Total reviews analyzed: {len(sample_reviews)}")
        print(f"  • Total aspects identified: {total_aspects}")
        print(f"  • Average aspects per review: {total_aspects/len(sample_reviews):.1f}")
    
    print(f"\n✅ Demo completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main() 