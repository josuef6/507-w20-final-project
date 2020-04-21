# 507-w20-final-project

The project, through the command line, allows user input to identify how many records from each set of top-rated media type they would like between 50 and 250. So if a user inputs 50, they would have 100 total records, 50 from movies and 50 from shows.

Once they have identified a number the program will then pull information from the respective media types and print a formatted output after each media type is complete. The database is being created during this process and populated with the information from each recorded item. 

Once the scraping is complete and database is created, the user will then be able to use the command line to select different information from the database (using SQL queries) by selecting the number with the corresponding option:

      [1] Average Rating (out of 10) by First Movie Genre

      [2] Average Rating (out of 10) by Film Rating

      [3] Movies Data (All Movie Results)

      [4] Average Rating (out of 10) by Show Type

      [5] Average Rating (out of 10) by First Show Genre

      [6] Average Rating (out of 10) by Show Rating

      [7] Shows Data (All Show Results)

Plotly graphs will be used to display the Average Rating options (1, 2, and 4-6). While options 3 and 7 will print all the information from the respective media type (movies or shows) that were collected at the beginning of the program.

The user is to type ‘exit’ when they are ready to exit the program.
