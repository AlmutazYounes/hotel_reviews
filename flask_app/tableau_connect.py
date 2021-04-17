import tableauserverclient as TSC
from pandleau import *
import pandas as pd
from random import randint
import glob
from collections import Counter
import operator
from sentiment_prediction import make_predictions
from utils.clean_text import remove_punctuations, remove_diacritics, remove_repeating_char, light_stem, deEmojify

def publishtotableau(df, folder_path, projectid, datasource_name, auth_list, site='ABSA'):
    """
    Args:
        df: dataframe to publish
        folder_path: folder to store temp.hyper file generated
        projectid: Tableau Server Project ID
        datasource_name: Name of the datasource to publish
        auth_list: List-like with username on index 0, password on index 1
        site: Tableau server site
    """
    pandleau(df).to_tableau(folder_path + 'temp.hyper', add_index=False)

    tableau_auth = TSC.TableauAuth(auth_list[0], auth_list[1], site_id=site)
    server = TSC.Server('https://dub01.online.tableau.com/', use_server_version=True)

    with server.auth.sign_in(tableau_auth):
        mydatasourceitem = TSC.DatasourceItem(projectid, name=datasource_name)
        item = server.datasources.publish(mydatasourceitem, folder_path + 'temp.hyper', 'Overwrite')
        print("{} successfully published with id: {}".format(item.name, item.id))


def connect(test_sents, aspects_prds):
    category = [
        'FACILITIES#CLEANLINESS', 'FACILITIES#COMFORT', 'FACILITIES#DESIGN_FEATURES', 'FACILITIES#GENERAL',
        'FACILITIES#MISCELLANEOUS',
        'FACILITIES#PRICES', 'FACILITIES#QUALITY', 'FOOD_DRINKS#MISCELLANEOUS', 'FOOD_DRINKS#PRICES',
        'FOOD_DRINKS#QUALITY', 'FOOD_DRINKS#STYLE_OPTIONS', 'HOTEL#CLEANLINESS', 'HOTEL#COMFORT',
        'HOTEL#DESIGN_FEATURES', 'HOTEL#GENERAL', 'HOTEL#MISCELLANEOUS', 'HOTEL#PRICES',
        'HOTEL#QUALITY', 'LOCATION#GENERAL', 'ROOMS#CLEANLINESS', 'ROOMS#COMFORT',
        'ROOMS#DESIGN_FEATURES', 'ROOMS#GENERAL', 'ROOMS#MISCELLANEOUS', 'ROOMS#PRICES',
        'ROOMS#QUALITY', 'ROOMS_AMENITIES#CLEANLINESS', 'ROOMS_AMENITIES#COMFORT', 'ROOMS_AMENITIES#DESIGN_FEATURES',
        'ROOMS_AMENITIES#GENERAL', 'ROOMS_AMENITIES#MISCELLANEOUS', 'ROOMS_AMENITIES#PRICES', 'ROOMS_AMENITIES#QUALITY',
        'SERVICE#GENERAL']

    cat, catt = [], []
    for i in aspects_prds:
        rand = randint(0, len(category) - 1)
        for j in range(len(i)):
            cat.append(category[rand])
        catt.append(cat)
        cat = []
    final_df = pd.DataFrame(zip(test_sents["sentence"].values, aspects_prds, catt),
                            columns=["sentence", "word", "TEMP_category"])
    final_df = final_df[final_df.astype(str)['word'] != '[]']
    catt = [l for i in catt for l in i if l != ""]
    all_aspects = [l for i in aspects_prds for l in i if l != ""]
    test_sents_flat = [test_sents["sentence"].values[i] for i in range(len(aspects_prds)) for l in
                       range(len(aspects_prds[i]))]
    flat_df = pd.DataFrame(zip(test_sents_flat, all_aspects, catt),
                           columns=["test_sents_flat", "word_flat", "TEMP_category_flat"])




    flat_df["TEMP_sentiment_flat"] = make_predictions(flat_df)
    ###START Create a dict
    counts = Counter(all_aspects)
    a, aa = [], []
    myaspect_list = []
    for word, count in counts.items():
        if count > 5:
            a.append(word)
            a.append(count)
            myaspect_list.append(a)
            a = []
    sorted_x = sorted(counts.items(), key=operator.itemgetter(1))
    counts_df = pd.DataFrame(myaspect_list, columns=["aspect", "counts"])
    ###END Create a dict
    a = []
    for word in flat_df["word_flat"].values:
        word = remove_punctuations(word)
        word = remove_diacritics(word)
        word = remove_repeating_char(word)
        word = light_stem(word)
        word = deEmojify(word)
        a.append(word)
    flat_df["word_flat"] = a
    flat_df.to_csv("flat_df.csv")
    files = glob.glob('*.hyper')
    for f in files:
        os.remove(f)
    files = glob.glob('DataExtract*')
    for f in files:
        os.remove(f)
    publishtotableau(final_df, "test.hyper", "f73e9a9c-392a-41fe-8bd6-d053b2a47b06", "ABSA_data",
                     ['yitoji8784@astarmax.com', 'Mohtaz1!'])
    publishtotableau(flat_df, "test2.hyper", "f73e9a9c-392a-41fe-8bd6-d053b2a47b06", "ABSA_flat_data",
                     ['yitoji8784@astarmax.com', 'Mohtaz1!'])
    publishtotableau(counts_df, "counts_df.hyper", "f73e9a9c-392a-41fe-8bd6-d053b2a47b06", "ABSA_data_counts",
                     ['yitoji8784@astarmax.com', 'Mohtaz1!'])

    ############################################################################################################
