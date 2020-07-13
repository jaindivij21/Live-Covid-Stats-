# Live-Covid-Stats (City Specific, India only)
Python Project that provides the user with live stats to the user about Covid-19 Virus with respect to cities of India through an API. The same data can further be visualized through graphs.

Realtime data is fetched from the API: https://api.covid19india.org/districts_daily.json. The fetched data is stored into an sqlite3 database and thus after the user's query regarding the stats regarding COVID-19 virus in any Indian City; the active, recovered, confirmed cases and the number of deceased people are shown to the user that too on any specific date since April. 
Furthermore for intensive analysis; Matplotlib has been used to provide user with graphs for the same data for better analysis.

Run main.py for the Program. Note that your system must have pyhton installed to run the same.
