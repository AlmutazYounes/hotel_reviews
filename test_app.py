#!/usr/bin/env python3
"""
Test script for Hotel Reviews ABSA Application
This script tests both the model and the web interface.
"""

import requests
import json
import time
import sys
import os

def test_model():
    """Test the trained model directly."""
    print("🧠 Testing Model...")
    
    try:
        from simpletransformers.ner import NERModel
        
        # Get model path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(current_dir, "hotel_reviews_model")
        
        if not os.path.exists(model_path):
            print("❌ Model not found. Please train the model first.")
            return False
        
        # Load model
        model = NERModel("bert", model_path, use_cuda=False,
                         labels=["B-A", "I-A", "O"],
                         args={"use_cuda": False})
        
        # Test sentence
        test_sentence = "الفندق رائع والخدمة ممتازة والغرف نظيفة"
        predictions, _ = model.predict([test_sentence])
        
        # Extract aspects
        aspects = []
        current_aspect = []
        
        prediction = predictions[0]
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
        
        print(f"✅ Model test successful!")
        print(f"   Sentence: {test_sentence}")
        print(f"   Aspects found: {aspects}")
        print(f"   Number of aspects: {len(aspects)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Model test failed: {str(e)}")
        return False

def test_web_api():
    """Test the web API endpoints."""
    print("\n🌐 Testing Web API...")
    
    base_url = "http://localhost:5002"
    
    # Test if server is running
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("✅ Web server is running")
        else:
            print(f"❌ Web server returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException:
        print("❌ Web server is not running. Please start it with: cd flask_app && python app.py")
        return False
    
    # Test single sentence analysis
    try:
        test_sentence = "الموقع جيد والطعام لذيذ"
        response = requests.post(
            f"{base_url}/analyze_sentence",
            json={"sentence": test_sentence},
            headers={"Content-Type": "application/json", "X-Requested-With": "XMLHttpRequest"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Single sentence analysis successful!")
            print(f"   Sentence: {data['sentence']}")
            print(f"   Aspects: {data['aspects']}")
            print(f"   Count: {data['num_aspects']}")
        else:
            print(f"❌ Single sentence analysis failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Single sentence analysis failed: {str(e)}")
        return False
    
    # Test file upload (using sample data)
    try:
        sample_file = "sample_data.csv"
        if os.path.exists(sample_file):
            with open(sample_file, 'rb') as f:
                files = {'file': f}
                response = requests.post(
                    f"{base_url}/predict",
                    files=files,
                    headers={"X-Requested-With": "XMLHttpRequest"},
                    timeout=60
                )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ File upload analysis successful!")
                print(f"   Total reviews: {data['summary']['total_reviews']}")
                print(f"   Total aspects: {data['summary']['total_aspects']}")
                print(f"   Average aspects: {data['summary']['avg_aspects']}")
            else:
                print(f"❌ File upload analysis failed: {response.status_code}")
                return False
        else:
            print("⚠️  Sample data file not found, skipping file upload test")
            
    except Exception as e:
        print(f"❌ File upload analysis failed: {str(e)}")
        return False
    
    return True

def main():
    """Main test function."""
    print("=" * 60)
    print("🏨 Hotel Reviews ABSA - Application Test")
    print("=" * 60)
    
    # Test model
    model_success = test_model()
    
    # Test web API
    api_success = test_web_api()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    if model_success:
        print("✅ Model: Working correctly")
    else:
        print("❌ Model: Failed")
    
    if api_success:
        print("✅ Web API: Working correctly")
    else:
        print("❌ Web API: Failed")
    
    if model_success and api_success:
        print("\n🎉 All tests passed! Your application is ready to use.")
        print("🌐 Open http://localhost:5002 in your browser to access the web interface.")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 