import csv

movies ={}
movies_amount = 0

with open("IMDB_files_link/_filtered_data/movies.filtered") as data_file:
    reader = csv.reader(data_file, delimiter='\r')
    for line in reader:
        # line variable here is a list of strings, so we join it into one string
        full_line = " ".join(line)
        # partition returns 3-tuple: (part_before_delimiter, delimiter, part_after_delimiter)
        parted = full_line.partition("\t")
        title = parted[0]
        # in the part_after_delimiter we delete all \t characters
        year = parted[2].replace("\t","")
        # check year validity
        if year != "????" and int(year) >= 1986:
            movies[title]={"year": year}
        movies_amount += 1

print movies_amount, "all movies"
print len(movies), "movies amount after year filter"

######################################################
#               language filtering
######################################################

with open("IMDB_files_link/_filtered_data/language.filtered") as data_file:
    reader = csv.reader(data_file, delimiter='\r')
    for line in reader:
        # line variable here is a list of strings, so we join it into one string
        full_line = " ".join(line)
        # partition returns 3-tuple: (part_before_delimiter, delimiter, part_after_delimiter)
        parted = full_line.partition("\t")
        title = parted[0]
        # in the part_after_delimiter we delete all \t characters
        language = parted[2].replace("\t","")
        # if the language of the movie is not english delete its entry from movies
        # there are different language descriptions in the language.list
        # like for example: English	(English Subtitles), English	(Original Version) etc
        if language == "English" \
                or language == "English	(English Subtitles)" \
                or language == "English(English subtitles)" \
                or language == "English	(Original Version)" \
                or language == "English(Original version)" \
                or language == "English(original version)" \
                or language == "English(US)" \
                or language == "English(United States)" \
                or language == "English(original text)" \
                or language == "English	(English Version)":
            pass
        else:
            movies.pop(title, None)

print len(movies), "movies amount after language filter"

######################################################
#               ratings filtering
######################################################

with open("IMDB_files_link/_filtered_data/ratings.filtered") as data_file:
    reader = csv.reader(data_file, delimiter='\r')
    for line in reader:
        # line variable here is a list of strings, so we join it into one string
        full_line = " ".join(line)
        # We split the string back into list but double white space delimiter,
        # since column values have different lenghts.
        # Now we easily know which index element is what
        # This is how each entry will look after split:
        # ['', '2012000000', '72', '3.7', 'Ashbah (2014)']
        # ['', '0..0.12103', '23', '7.7', 'Ashbah Beyrouth (1998)']
        rating_data = full_line.split("  ")
        title = rating_data[4]
        rating = rating_data[3]
        votes = rating_data[2]
        if title not in movies:
            pass
        else:
            movies[title].update({  "votes": votes,
                                    "rating": rating})

for title in movies.keys():
    if "rating" not in movies[title]:
        movies.pop(title, None)

print len(movies), "amount of movies that have rating"

######################################################
#               director filtering
######################################################

directors_raw = []

with open("IMDB_files_link/_filtered_data/directors.filtered.new") as data_file:
    reader = csv.reader(data_file, delimiter='\n')
    for line in reader:
        full_line = " ".join(line)
        directors_raw.append(full_line)

directors_less_raw = []
temp = []
for line in directors_raw:
    # each director is separated by new line character, in our case its an empty list of strings
    if line != "":
        temp.append(line)
    else:
        directors_less_raw.append(temp)
        temp = []

movie_and_its_director = {}

for line in directors_less_raw:
    # first element is always director \t\t movie or director \t movie
    # if a director has only one movie
    if len(line) <= 1:
        # for example: ["'Kid Niagara' Kallet, Harry\tDrug Demon Romance (2012)  (co-director)"]
        full_line = " ".join(line)
        parted = full_line.partition("\t")
        director = parted[0]
        title = parted[2].replace("\t", "")
        title_parted = title.partition("  ")[0]
        movie_and_its_director[title_parted] = {"director": director}
    else:
        # for example: ["'t Hooft, Albert\tFallin' Floyd (2013)", '\t\tLittle Quentin (2010)',
        #  '\t\tTrippel Trappel Dierensinterklaas (2014)']
        first_line = line[0]
        parted = first_line.partition("\t")
        director = parted[0]
        title_first = parted[2].replace("\t", "")
        # we want to separate the title from the rest because imdb tends to add
        # extra info in the parathesis after the actual title
        # for example: Electric Shades of Grey (2001) (V)  (uncredited)
        # fortunately its separated by two white spaces after the actual title
        title_parted = title_first.partition("  ")[0]
        all_dir_movies = [title_parted]
        for remaining_title in line[1:len(line)]:
            remaining_title = remaining_title.replace("\t", "")
            title_parted = remaining_title.partition("  ")[0]
            all_dir_movies.append(title_parted)
        for title in all_dir_movies:
            movie_and_its_director[title] = {"director": director}

for title in movie_and_its_director:
    if title in movies:
        movies[title].update({"director": movie_and_its_director[title]["director"]})

for title in movies.keys():
    if "director" not in movies[title]:
        movies.pop(title, None)

print len(movies), "amount of movies that have directors"

######################################################
#               language filtering
######################################################