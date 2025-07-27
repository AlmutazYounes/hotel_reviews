from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="hotel-reviews-absa",
    version="1.0.0",
    author="Almutaz Younes",
    author_email="almutaz.younes@example.com",
    description="Aspect-Based Sentiment Analysis for Arabic Hotel Reviews using BERT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlmutazYounes/hotel_reviews",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
    },
    entry_points={
        "console_scripts": [
            "hotel-reviews-train=hotel_reviews.train_model:main",
            "hotel-reviews-app=hotel_reviews.flask_app.app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "hotel_reviews": ["Data/raw/*.txt", "flask_app/templates/*.html", "flask_app/static/*"],
    },
    keywords="nlp, sentiment-analysis, arabic, bert, hotel-reviews, aspect-extraction",
    project_urls={
        "Bug Reports": "https://github.com/AlmutazYounes/hotel_reviews/issues",
        "Source": "https://github.com/AlmutazYounes/hotel_reviews",
        "Documentation": "https://github.com/AlmutazYounes/hotel_reviews#readme",
    },
) 