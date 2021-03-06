import unicodedata
import ast
import file_save_load as fsl

######################################################
#               adding new budgets
######################################################

fileNameDataset = 'imdb_dataset_v7_no_plots'
fileNameBudgets = '_wiki_plot_for_' + fileNameDataset
actors_amount = 6

movies = fsl.read_from_file(fileNameDataset, actors_amount)

# with open('files/datasetV_20161116-203716') as csvfile:
#     reader = csv.DictReader(csvfile, delimiter = "\t")
#     for entry in reader:
#         movies[
#             entry["title"]
#         ] = {
#         "director":     entry["director"],
#         "rating":       entry["rating"],
#         "votes":        entry["votes"],
#         "year":         entry["year"],
#         "genre":        entry["genre"],
#         "gross":        entry["gross"],
#         "budget":       entry["budget"],
#         "run-time":     entry["run-time"] ,
#         "actor1":       entry["actor1"],
#         "actor1_rank":  entry["actor1_rank"],
#         "actor1_sex":   entry["actor1_sex"],
#         "actor2":       entry["actor2"],
#         "actor2_rank":  entry["actor2_rank"],
#         "actor2_sex":   entry["actor2_sex"],
#         "actor3":       entry["actor3"],
#         "actor3_rank":  entry["actor3_rank"],
#         "actor3_sex":   entry["actor3_sex"],
#         "actor4":       entry["actor4"],
#         "actor4_rank":  entry["actor4_rank"],
#         "actor4_sex":   entry["actor4_sex"],
#         "actor5":       entry["actor5"],
#         "actor5_rank":  entry["actor5_rank"],
#         "actor5_sex":   entry["actor5_sex"],
#         "actor6":       entry["actor6"],
#         "actor6_rank":  entry["actor6_rank"],
#         "actor6_sex":   entry["actor6_sex"],
#         "plot":         entry["plot"]
#         }

new_plots = {}

with open('files/' + fileNameBudgets) as file:
    for entry in file:
        temp = ast.literal_eval(entry)
        title = temp[1]
        plot = temp[0]
        new_plots[title] = plot

c = 0
for title in movies:
    if title in new_plots:
        movies[title]["plot"] = unicodedata.normalize('NFKD', new_plots[title]).encode('ascii','ignore')
        c += 1

print "new plot found for:", c

# for title in movies.keys():
#     if movies[title]["budget"] == "no_info":
#         movies.pop(title, None)

print "amount of movies with plot" , len(movies)


fsl.save_to_dataset(movies,actors_amount)

# f = open('files/datasetV_' + str(time.strftime("%Y%m%d-%H%M%S")), 'w')
#
# f.write("title\t" +
#         "director\t" +
#         "rating\t" +
#         "votes\t" +
#         "year\t" +
#         "genre\t" +
#         "gross\t" +
#         "budget\t" +
#         "run-time\t" +
#         "actor1\t" +
#         "actor1_rank\t"
#         "actor1_sex\t"
#         "actor2\t" +
#         "actor2_rank\t" +
#         "actor2_sex\t" +
#         "actor3\t" +
#         "actor3_rank\t" +
#         "actor3_sex\t" +
#         "actor4\t" +
#         "actor4_rank\t" +
#         "actor4_sex\t" +
#         "actor5\t" +
#         "actor5_rank\t" +
#         "actor5_sex\t" +
#         "actor6\t" +
#         "actor6_rank\t" +
#         "actor6_sex\t" +
#         "plot" + "\n"
#         )
# for title in movies:
#     entry = movies[title]
#     f.write(title + "\t" +
#             str(entry["director"]) + "\t" +
#             str(entry["rating"]) + "\t" +
#             str(entry["votes"]) + "\t" +
#             str(entry["year"]) + "\t" +
#             str(entry["genre"]) + "\t" +
#             str(entry["gross"]) + "\t" +
#             str(entry["budget"]) + "\t" +
#             str(entry["run-time"]) + "\t" +
#             str(entry["actor1"]) + "\t" +
#             str(entry["actor1_rank"]) + "\t" +
#             str(entry["actor1_sex"]) + "\t" +
#             str(entry["actor2"]) + "\t" +
#             str(entry["actor2_rank"]) + "\t" +
#             str(entry["actor2_sex"]) + "\t" +
#             str(entry["actor3"]) + "\t" +
#             str(entry["actor3_rank"]) + "\t" +
#             str(entry["actor3_sex"]) + "\t" +
#             str(entry["actor4"]) + "\t" +
#             str(entry["actor4_rank"]) + "\t" +
#             str(entry["actor4_sex"]) + "\t" +
#             str(entry["actor5"]) + "\t" +
#             str(entry["actor5_rank"]) + "\t" +
#             str(entry["actor5_sex"]) + "\t" +
#             str(entry["actor6"]) + "\t" +
#             str(entry["actor6_rank"]) + "\t" +
#             str(entry["actor6_sex"]) + "\t" +
#             str(entry["plot"]) + "\n")
# f.close()
