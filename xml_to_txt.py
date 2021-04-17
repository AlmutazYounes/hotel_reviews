import xml.etree.ElementTree as ET
from string import punctuation
import qalsadi.lemmatizer
from tqdm import tqdm
import pandas as pd
import numpy as np
from tashaphyne.stemming import ArabicLightStemmer
ArListem = ArabicLightStemmer()
lemmer = qalsadi.lemmatizer.Lemmatizer()

def xmlto_txt(output_text_path, xml_path, output_file):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    sentences = []
    for sentence in root.iter("sentence"):
        text = sentence.find("text")
        opinions = sentence.findall("Opinions")
        if len(opinions) > 0:
            for opinions in sentence.iter("Opinions"):
                aspects = []
                for opinion in opinions.iter("Opinion"):
                    aspects.append(opinion.attrib)
                sentences.append({"text": text.text, "aspects": aspects})
        else:
            sentences.append({"text": text.text, "aspects": None})

    out = open(output_text_path, "w", encoding="utf-8")
    pad = 0
    global_aspect_count = 0
    for sentence in sentences:
        aspects = sentence["aspects"]
        text = sentence["text"]
        if aspects is None:
            pad += 1
            text = text.strip()
            words = text.split(" ")
            for word in words:
                if word.strip() is not "":
                    out.write(word + "\t" + "O" + "\n")
            out.write("\n")
        else:
            pad += 1
            dict = {}
            for aspect in aspects:
                target = aspect["target"]
                from_ = int(aspect["from"])
                to_ = int(aspect["to"])
                if target != "NULL" and from_ not in dict.keys():
                    dict[from_] = [target, from_, to_]
            keys = sorted(dict)
            if len(keys) > 0:
                dump = ""
                last_end = 0
                counter = 0
                for key in keys:
                    global_aspect_count += 1
                    vals = dict[key]
                    target = vals[0]
                    from_ = vals[1]
                    to_ = vals[2]
                    aspect_ = text[from_:to_]
                    temp = text[last_end:from_]
                    last_end = to_
                    if aspect_ == target:
                        storage = ""
                        aspect = target.split(" ")
                        i = 0
                        words = text[from_:to_ + 1].split(" ")
                        for asp in aspect:
                            kk = asp
                            for ww in words:
                                if asp in ww and len(ww) - len(asp) < 2:
                                    kk = ww
                                    # if len(asp) < len(ww):
                                    #     to_ = to_ - len(asp) + len(ww)
                                    # break
                            if i == 0:
                                storage = storage + kk + "\t" + "B-A" + "\n"
                                i += 1
                            else:
                                storage = storage + kk + "\t" + "I-A" + "\n"
                                i += 1

                        temp += storage
                        dump += temp

                        if counter == len(keys) - 1:
                            dump += text[to_:]

                        counter += 1
                    else:
                        print(aspect_)
                        print(target)
                        print("NO MATCH")
                        counter += 1
                if dump != "":
                    dump = dump.replace(" ", "\t" + "O" + "\n")
                    dump += "\t" + "O"
                    out.write(dump + "\n\n")
            else:
                text = text.strip()
                words = text.split(" ")
                for word in words:
                    if word.strip() is not "":
                        out.write(word + "\t" + "O" + "\n")
                out.write("\n")

    print(global_aspect_count)
    out.close()

    f = open(output_text_path, "r", encoding="utf-8")
    out = open(output_file, "w", encoding="utf-8")
    for line in tqdm(f):
        if line.strip() != "":
            line1 = line.split("\t")
            line2 = ''.join(c for c in line1[0])
            if line2.isnumeric():
                line2 = "<NUM>"
            # line2 = ''.join(c for c in line1[0] if c not in punctuation)
            # line2 = line2.strip()
            # line2 = line2.replace("...", "")
            # line2 = line2.replace(".", "")
            # line2 = line2.replace("،", "")
            # line2 = lemmer.lemmatize(line2)
            # line2 = ArListem.light_stem(line2)

            # if line2.strip() == "" or (len(line2) == 1 and line2 != "و"):

            if line2.strip() == "":
                continue
            else:
                out.write(line2 + "\t" + line1[1])
        else:
            out.write("\n")
    out.close()


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
    df = df.replace(r'^\s*$', np.nan, regex=True).dropna()
    return df
#
#
# output_text_path= "Data/raw/train_withspace.txt"
# xml_path= "Data/XML/Train_SB1.xml"
# output_file= "Data/raw/train.txt"
# xmlto_txt(output_text_path, xml_path, output_file)
#
#
# output_text_path= "Data/raw/test_withspace.txt"
# xml_path= "Data/manually cleaned XML/SB1_TEST_GOLD.xml"
# output_file= "Data/raw/test.txt"
# xmlto_txt(output_text_path, xml_path, output_file)
