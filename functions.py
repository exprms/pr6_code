# funktion zum einlesen der Feeds und Ausgabe der Titel

def get_titles(url_list):
    import feedparser as fp
    # initialisiere leere Liste
    feed_titles = []

    # durchlaufe alle URLs
    for url in url_list:
        tempfeed = fp.parse(url)

        # schreibe alle Titel des i-ten feeds in die Liste
        feed_titles += [a.title for a in tempfeed.entries]

    # Entferne Duplikate:
    feed_titles = list(set(feed_titles))
    return(feed_titles)

def get_articles(sim_vector, titles, th):
    # findet alle Indizes mit eine similarity höher als th
    # Return Value ist Liste der Refernzindizes und den dazugehörigen Ähnlichen Indizes sowie
    # der Wert der cosinie-similarity
    import numpy as np

    # Alle Einträge größer als th,
    # ist im Prinzip eine Matrix als Vektor dargestellt
    x_temp  = ((sim_vector >= th) & (sim_vector < 0.999))

    # Indizes der Diagonaleintraege von x_temp
    ignore_index = [number*len(titles)+number for number in range(len(titles))]

    # da die Matrix symmetrisch ist, interessieren uns nur die
    # Einträge oberhalb der Diagonale: (das muss dann ein Vektor mit Länge N*(N-1)/2 sein,
    # wenn N die Länge der titelliste ist)
    search_index = []
    for i in range(len(titles)):
        search_index = search_index + [i*len(titles)+j for j in range(i+1,len(titles))]

    # indizes mit hohen similaritywerten und oberhalb der Diagonaleinträge:
    index_found = [item for item in search_index if x_temp[item]]

    # Rückrechnen der Indizes zu einem Indexpaar. Dieses indexpaar sind die Indizes der ähnlichen Titel:
    first = [int(np.floor(i/len(titles))) for i in index_found]
    second = [np.mod(i, len(titles)) for i in index_found]
    value = [sim_vector[i] for i in index_found]
    return (first, second, value)
