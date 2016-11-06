import os, re, helpers, sys
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from datetime import datetime


def min_hash(perm, data, reference_data):
    print "#---------------------------------------#\n" \
          "Staring minHash with", perm, "permutations\n" \
          "#---------------------------------------#"
    original_array = np.transpose(data)

    amount_of_permutations = perm
    hash_functions_array = [[0 for i in range(original_array.shape[1])] for ii in range(amount_of_permutations)]

    for permutation in range(amount_of_permutations):
        permuted_array = np.copy(original_array)
        np.random.shuffle(permuted_array)
        permuted_array = np.transpose(permuted_array)
        row_index = 0
        for row in permuted_array:
            column_index = 0
            for number in row:
                if number > 0:
                    hash_functions_array[permutation][row_index] = column_index
                    break
                column_index += 1
            row_index += 1
        print "Done with permutation #:", permutation + 1, "/", amount_of_permutations

    # each row corresponds to an article, each row index corresponds to article index in reference_data
    hash_functions_array = np.transpose(hash_functions_array)

    def jaccard_dist(set_1, set_2):
        intersection = len(set_1 & set_2)
        union = len(set_1 | set_2)
        return 1 - intersection / float(union)

    print "Creating buckets based on Jaccard distance..."

    buckets = {}
    amount_of_all_articles = len(hash_functions_array)

    # calculate similarities:
    for article_index, article in enumerate(hash_functions_array):
        similarities = []
        for remaining_article in range(article_index + 1, amount_of_all_articles):
            # print "for art:", article_index, "remaining are:", remaining_article
            similarity = jaccard_dist(set(hash_functions_array[article_index]),
                                      set(hash_functions_array[remaining_article]))
            current_article_id = reference_data[article_index]["id"]
            remaining_article_id = reference_data[remaining_article]["id"]
            similarities.append({{"id": remaining_article_id,
                                  "similarity": similarity}})
            buckets[current_article_id] = {"similar_articles": []}
            buckets[current_article_id]["similar_articles"].append({"id": remaining_article_id,
                                                                    "similarity": similarity})
        # print "Completed:", article_index, "/", amount_of_all_articles
        sys.stdout.write("\rCompleted:" + str(article_index + 1) + "/" + str(amount_of_all_articles))
        sys.stdout.flush()
    print "\n"
    for bucket in buckets.iteritems():
        print bucket
    print "#----------------- Done ----------------#"


# ------------- read in entries from all files -------------

if __name__ == '__main__':

    data_raw = []
    data_raw_filtered = []
    data_directory = "data"
    data_topics = []

    for file in os.listdir(data_directory):
        if file.endswith(".json"):
            data = helpers.read_file(data_directory + "/" + file)
            data_raw.append(data)

    for file in data_raw:
        for entry in file:
            if ("topics" in entry) and ("body" in entry):
                data_raw_filtered.append(entry)

    print "All articles loaded..."
    # print data_raw_filtered[0]
    # ------------------ create bag of words -----------------

    data_clean = []

    # TODO: remove amount restriction
    for entry in data_raw_filtered[:100]:
        words_list = re.sub("[^a-zA-Z]", " ", entry['body'])
        data_clean.append({"body": [w for w in words_list.lower().split()],
                           "topics": entry["topics"],
                           "id": entry["id"]})

    # print data_clean[0]

    data_words_only = []

    for article in data_clean:
        data_words_only.append(" ".join(article["body"]))  # glue all words together into a list of strings

    vectorizer = CountVectorizer(analyzer="word",
                                 tokenizer=None,
                                 preprocessor=None,
                                 stop_words='english'
                                 )

    _features = vectorizer.fit_transform(data_words_only)

    _features_array = _features.toarray()

    print "Got all features...", _features_array.shape

    # print train_data_features_array
    # ----------------------------------------
    # print data_clean
    min_hash(3, _features_array, data_clean)
