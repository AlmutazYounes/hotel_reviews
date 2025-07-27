import logging
import pandas as pd
import os
from seqeval.metrics import f1_score
from seqeval.scheme import IOB2
from simpletransformers.ner import NERModel


def txt_to_df(path):
    file1 = open(path, 'r')
    Lines = file1.readlines()
    word, tag, sent_num, line_num = [], [], [], 1
    for line in Lines:
        if line == "\n":
            line_num += 1
        else:
            word.append(line.split("\t")[0])
            tag.append(line.split("\t")[1].split("\n")[0])
            sent_num.append(line_num)
    df = pd.DataFrame(zip(sent_num, word, tag), columns=["Sentence #", "Word", "Tag"])
    return df


if __name__ == '__main__':
    # Get current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Update paths to use current directory
    train_path = os.path.join(current_dir, "Data", "raw", "train.txt")
    test_path = os.path.join(current_dir, "Data", "raw", "test.txt")
    model_output_dir = os.path.join(current_dir, "hotel_reviews_model")
    
    print(f"Training data path: {train_path}")
    print(f"Test data path: {test_path}")
    print(f"Model output directory: {model_output_dir}")
    
    # Check if files exist
    if not os.path.exists(train_path):
        print(f"Error: Training file not found at {train_path}")
        exit(1)
    
    if not os.path.exists(test_path):
        print(f"Error: Test file not found at {test_path}")
        exit(1)
    
    # Create model directory if it doesn't exist
    os.makedirs(model_output_dir, exist_ok=True)
    
    # Load data
    train_df = txt_to_df(train_path)
    test_df = txt_to_df(test_path)
    test_df.reset_index(drop=True, inplace=True)
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    transformers_logger = logging.getLogger("transformers")
    transformers_logger.setLevel(logging.WARNING)
    
    # Prepare data for simpletransformers
    train_df = pd.DataFrame(train_df.values, columns=['sentence_id', 'words', 'labels'])
    test_df = pd.DataFrame(test_df.values, columns=['sentence_id', 'words', 'labels'])
    
    print("Training data shape:", train_df.shape)
    print("Test data shape:", test_df.shape)
    
    # Initialize model
    aspect_model = NERModel("bert", "MutazYoune/Ara_DialectBERT",
                            labels=["B-A", "I-A", "O"],
                            args={"save_eval_checkpoints": False, 
                                  "save_steps": -1, 
                                  'overwrite_output_dir': True,
                                  "save_model_every_epoch": False,
                                  'reprocess_input_data': True, 
                                  "train_batch_size": 5, 
                                  'num_train_epochs': 2,
                                  "gradient_accumulation_steps": 5,
                                  "output_dir": model_output_dir,
                                  "learning_rate": 0.0001}, 
                            use_cuda=False)
    
    print("Starting model training...")
    # Train the model
    aspect_model.train_model(train_df)
    
    print("Training completed!")
    
    # Test the model
    print("Testing model...")
    test_df = test_df.iloc[:100]  # Test on first 100 examples
    a = test_df.groupby("sentence_id")
    gps = [a.get_group(key) for key, item in a]
    actual = [list(g.labels.values) for g in gps]
    sentences = [" ".join(i) for i in [[w for w in g.words.values] for g in gps]]
    
    predictions, raw_outputs = aspect_model.predict(sentences)
    pred = [[tag__ for word_ in s for word__, tag__ in word_.items()] for s in [sentence_ for sentence_ in predictions]]
    
    f1 = f1_score(actual, pred, mode='strict', scheme=IOB2)
    print(f"F1 Score: {f1}")
    
    print(f"Model saved to: {model_output_dir}") 