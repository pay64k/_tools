import csv, wikipedia, unicodedata, wptools
import time
import file_save_load as fsl

fileName = 'datasetV_20161118-080950'
actors_amount = 3

movies = fsl.read_from_file(fileName, 3)

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
# print movies["Get Him to the Greek (2010)"]


def compute_jaccard_index(list_1, list_2):
    list_1 = list_1.replace("(","").replace(")","")
    list_2 = list_2.replace("(","").replace(")","")
    set_1 = set(list_1.split())
    set_2 = set(list_2.split())
    return len(set_1.intersection(set_2)) / float(len(set_1.union(set_2)))

movies_with_no_budget = []
wiki_no_budget = []
wiki_budget_ok = []
different_budget_keys = set()

for title in movies:
    if movies[title]["budget"] == "no_info":
        full_title = title
        title_no_year = title.partition("(")[0]
        movies_with_no_budget.append([title_no_year,full_title])

counter = 0
# TODO Remove limits
for title in movies_with_no_budget:

    title_no_year = title[0]
    full_title = title[1]
    title_film = str(title_no_year + "(film)")
    year = title[1].partition("(")[2]
    year = year.replace("(","")
    year = year.replace(")","")
    try:
        search_results = wikipedia.search(title_no_year)
    except:
        print "Error on search_results"
        search_results =[]
        current_query = "no_results"

    search_results = [unicodedata.normalize('NFKD', x).encode('ascii','ignore') for x in search_results]

    # print "search_results for", title_no_year, search_results

    for result in search_results:
        if compute_jaccard_index(title_film,result) >= 1:
            # print "\n-----1-----\n"
            current_query = result
            break
        elif compute_jaccard_index(title_no_year,result) >=1:
            # print "\n-----2-----\n"
            current_query = result
            break
        elif compute_jaccard_index(title_no_year,result) >=1:
            # print "\n-----3-----\n"
            current_query = result
            break
        elif compute_jaccard_index(str(title_no_year + " (" + year + " film" + ")"),result) >=1:
            # print "\n-----4-----\n"
            current_query = result
            break
        # elif "film" in result:
        #     current_query = result
        #     break
        else:
            current_query = "no_results"

    # print "\tcurrent_query:", current_query , "/ for movie: ", full_title

    if current_query != "no_results":
        try:
            movie_page = wptools.page(current_query,silent=True).get_parse()
        except:
            print "error for:", current_query, " query"
            movie_page.infobox = None

        if movie_page.infobox is not None:
            # print "infobox for title:", title_no_year
            # print "\t", movie_page.infobox, "\n"

            if "budget" in movie_page.infobox:

                if movie_page.infobox["budget"] == "":
                    wiki_no_budget.append(["empty_info", full_title])

                else:
                    budget = movie_page.infobox["budget"]
                    wiki_budget_ok.append([budget, full_title])
                    different_budget_keys.add(budget)

            else:
                wiki_no_budget.append(["no_info", full_title])
        else:
            wiki_no_budget.append(["no_info_box", full_title])
    else:
        wiki_no_budget.append(["no_info_query", full_title])

    counter += 1
    print "Done with:",counter,"/",len(movies_with_no_budget)

print "BUDGET:\tmovies with info:", len(wiki_budget_ok), "\tmovies no info:", len(wiki_no_budget), "\tall movies with no info:", len(movies_with_no_budget)

f = open('files/_wiki_budg_for_' + fileName,'w')
f.write(str(time.strftime("%c")) + "\n")
f.write("BUDGET:\tmovies with info:" + str(len(wiki_budget_ok)) + "\tmovies no info:" + str(len(wiki_no_budget)) + "\tall movies with no info:" + str(len(movies_with_no_budget)) + "\n")

for entry in wiki_budget_ok:
    f.write(str(entry)+"\n")

f.close()

# do the same with plots here: