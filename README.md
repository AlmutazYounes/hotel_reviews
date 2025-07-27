# 🏨 Hotel Reviews Aspect-Based Sentiment Analysis (ABSA)

A sophisticated system for analyzing Arabic hotel reviews using Aspect-Based Sentiment Analysis (ABSA) with BERT-based Named Entity Recognition (NER). This project provides both a web interface and API for extracting aspects from hotel reviews.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)
![BERT](https://img.shields.io/badge/BERT-Multilingual-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)

## 🌟 Features

- **🎯 High Accuracy**: Achieves 84% F1 score on Arabic hotel reviews
- **🌍 Arabic Language Support**: Optimized for Arabic text processing
- **🤖 BERT-based Model**: Uses `bert-base-multilingual-cased` for robust aspect extraction
- **💻 Web Interface**: Beautiful, responsive web application
- **📱 Mobile Friendly**: Works seamlessly on all devices
- **🔌 API Support**: RESTful API for integration
- **📊 Real-time Analysis**: Instant results with loading animations
- **🎨 Modern UI**: Clean design with Arabic RTL support
- **✅ Production Ready**: Fully tested and deployed

## 🏗️ Architecture

The system consists of three main components:

1. **🧠 Model Training**: BERT-based NER model for aspect extraction
2. **🌐 Web Application**: Flask-based interface for user interaction
3. **📈 Data Processing**: Efficient handling of Arabic text data

## 📁 Project Structure

```
hotel_reviews/
├── 📂 Data/
│   ├── 📂 raw/                    # Training and test data
│   ├── 📂 XML/                    # XML format data
│   └── 📂 manually cleaned XML/   # Manually cleaned data
├── 📂 flask_app/
│   ├── 📂 templates/              # HTML templates
│   │   ├── index.html            # Main interface
│   │   └── results.html          # Results display
│   ├── 📂 static/                 # Static files (CSS, JS)
│   ├── app.py                    # Flask application
│   └── main.py                   # Original Flask app
├── 📂 hotel_reviews_model/        # Trained model files
├── train_model.py                # Model training script
├── demo.py                       # Demo script
├── test_app.py                   # Test script
├── main.py                       # Original training script
├── xml_to_txt.py                # Data conversion utility
├── sample_data.csv              # Sample data for testing
├── requirements.txt             # Python dependencies
├── setup.py                     # Package setup
├── install.sh                   # Installation script
├── DEPLOYMENT.md                # Deployment guide
├── LICENSE                      # MIT License
└── README.md                    # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git

### Installation

#### Option 1: Automated Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/AlmutazYounes/hotel_reviews.git
cd hotel_reviews

# Run the installation script
chmod +x install.sh
./install.sh
```

#### Option 2: Manual Installation

```bash
# Clone the repository
git clone https://github.com/AlmutazYounes/hotel_reviews.git
cd hotel_reviews

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Train the model
python train_model.py

# Start the web application
cd flask_app
python app.py
```

### Usage

1. **Access the Web Interface**
   - Open your browser and go to `http://localhost:5003`
   - You'll see a beautiful interface with two options

2. **Single Sentence Analysis**
   - Click on "جملة واحدة" (Single Sentence) tab
   - Enter an Arabic hotel review
   - Click "تحليل الجملة" (Analyze Sentence)
   - View the extracted aspects directly under the input field

3. **Bulk File Analysis**
   - Click on "ملف CSV" (CSV File) tab
   - Upload a CSV file with a "sentence" column
   - Click "تحليل الملف" (Analyze File)
   - View results for all reviews

## 📊 Model Performance

| Metric | Value |
|--------|-------|
| **F1 Score** | 84% |
| **Model** | BERT-base-multilingual-cased |
| **Labels** | B-A (Beginning), I-A (Inside), O (Outside) |
| **Training Data** | 100,552 samples |
| **Test Data** | 24,848 samples |
| **Language** | Arabic |
| **Response Time** | ~4-7 seconds per sentence |

## 🎯 Usage Examples

### Single Sentence Analysis

```python
from simpletransformers.ner import NERModel

# Load the trained model
model = NERModel("bert", "hotel_reviews_model", use_cuda=False)

# Analyze a sentence
sentence = "الفندق رائع والخدمة ممتازة والغرف نظيفة"
predictions, _ = model.predict([sentence])

# Extract aspects
aspects = extract_aspects(predictions[0])
print(aspects)  # ['الفندق', 'الخدمة', 'الغرف']
```

### Web API Usage

```bash
# Single sentence analysis
curl -X POST http://localhost:5003/analyze_sentence \
  -H "Content-Type: application/json" \
  -d '{"sentence": "الفندق رائع والخدمة ممتازة والغرف نظيفة"}'

# File upload analysis
curl -X POST http://localhost:5003/predict \
  -F "file=@reviews.csv"
```

## 🔧 Configuration

### Model Parameters

The model can be configured in `train_model.py`:

```python
aspect_model = NERModel("bert", "bert-base-multilingual-cased",
                        labels=["B-A", "I-A", "O"],
                        args={
                            "train_batch_size": 5,
                            "num_train_epochs": 2,
                            "learning_rate": 0.0001,
                            "gradient_accumulation_steps": 5
                        })
```

### Flask Configuration

The web application can be configured in `flask_app/app.py`:

```python
app.run(debug=True, threaded=False, host='0.0.0.0', port=5003)
```

## 📈 Training Data

The model is trained on Arabic hotel reviews with the following characteristics:

- **Language**: Arabic
- **Domain**: Hotel reviews and feedback
- **Aspect Types**: Hotel features, services, amenities, location, staff
- **Annotation Scheme**: IOB2 (Inside-Outside-Beginning)
- **Data Source**: Curated hotel review dataset

## 🎨 Interface Features

### Modern Design
- **Clean Interface**: No distracting hover effects
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Arabic RTL Support**: Proper right-to-left text direction
- **Loading Indicators**: Clear feedback during processing

### User Experience
- **Tabbed Interface**: Easy switching between single sentence and file upload
- **Real-time Feedback**: Loading spinners and progress indicators
- **Error Handling**: Clear error messages and validation
- **Results Display**: Results appear directly under input fields

### Results Display
- **Aspect Tags**: Colorful tags for identified aspects
- **Statistics**: Summary of analysis results
- **Clean Layout**: Easy to read and understand

## 🛠️ Development

### Running Tests

```bash
# Test the model and web interface
python test_app.py

# Run the demo script
python demo.py

# Test the web interface
cd flask_app
python app.py
```

### Adding New Features

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 API Documentation

### Endpoints

#### POST `/analyze_sentence`
Analyze a single sentence for aspects.

**Request:**
```json
{
  "sentence": "الفندق رائع والخدمة ممتازة"
}
```

**Response:**
```json
{
  "sentence": "الفندق رائع والخدمة ممتازة",
  "aspects": ["الفندق", "الخدمة"],
  "num_aspects": 2
}
```

#### POST `/predict`
Upload a CSV file for bulk analysis.

**Request:** Multipart form data with CSV file

**Response:**
```json
{
  "results": [...],
  "summary": {
    "total_reviews": 10,
    "total_aspects": 25,
    "avg_aspects": 2.5
  }
}
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation as needed
- Ensure Arabic text support

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Almutaz Younes**
- GitHub: [@AlmutazYounes](https://github.com/AlmutazYounes)
- Email: almutaz.younes@example.com

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Almutaz Younes**
- GitHub: [@AlmutazYounes](https://github.com/AlmutazYounes)

---

**⭐ Star this repository if you find it useful!** 