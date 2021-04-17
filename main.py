import logging
import pandas as pd
from IPython.display import clear_output
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
    train_df = txt_to_df("/Users/mutaz/Desktop/Mutaz Thesis bert/Data/raw/train.txt")
    test_df = txt_to_df("/Users/mutaz/Desktop/Mutaz Thesis bert/Data/raw/test.txt")
    test_df.reset_index(drop=True, inplace=True)
    # test_df["Sentence #"] = test_df["Sentence #"].values
    logging.basicConfig(level=logging.INFO)
    transformers_logger = logging.getLogger("transformers")
    transformers_logger.setLevel(logging.WARNING)
    train_df = pd.DataFrame(train_df.values, columns=['sentence_id', 'words', 'labels'])
    test_df = pd.DataFrame(test_df.values, columns=['sentence_id', 'words', 'labels'])
    model_used = "/Users/mutaz/Desktop/Mutaz Thesis bert/hotel_reviews"
    mm, epp, lrr, f11, results = [], [], [], [], {}
    aspect_model = NERModel("bert", "{}".format(model_used),
                            labels=["B-A", "I-A", "O"],
                            args={"save_eval_checkpoints": False, "save_steps": -1, 'overwrite_output_dir': True,
                                  "save_model_every_epoch": False,
                                  'reprocess_input_data': True, "train_batch_size": 5, 'num_train_epochs': 2,
                                  "gradient_accumulation_steps": 5,
                                  "output_dir": "/Users/mutaz/Desktop/Mutaz Thesis bert"
                                , "learning_rate": 0.0001}, use_cuda=False)
    # aspect_model.train_model(train_df)
    test_df = test_df.iloc[:100]
    a = test_df.groupby("sentence_id")
    gps = [a.get_group(key) for key, item in a]
    actual = [list(g.labels.values) for g in gps]
    sentences = [" ".join(i) for i in [[w for w in g.words.values] for g in gps]]
    predictions, raw_outputs = aspect_model.predict(sentences)
    pred = [[tag__ for word_ in s for word__, tag__ in word_.items()] for s in [sentence_ for sentence_ in predictions]]
    clear_output()
    f1 = f1_score(actual, pred, mode='strict', scheme=IOB2)
    print(f1)