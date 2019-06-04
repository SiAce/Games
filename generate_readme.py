import csv
with open("data.csv", newline='') as csvfile:
    gamesreader = csv.reader(csvfile)
    next(gamesreader)

    with open("README.md", "w") as readme_file:
        # Print title and description
        readme_file.write("# Games to Be Played\n\nThis repository lists all the games that I want to play.\n")
        
        # Print each genre as a header
        genre = ''
        for row in gamesreader:
            if row[1] != genre:
                genre = row[1]
                readme_file.write("\n## " + row[1] + "\n\n")
            
            # Check whether the game is finished
            if row[4] == '1':
                readme_file.write("- [x] ~~" + row[0] + "~~")
            elif row[4] == '0':
                readme_file.write("- [ ] " + row[0])

            # Print the name
            # readme_file.write(row[0])

            # Print the platform
            if row[2] == 'PlayStation':
                readme_file.write(" ![PS4](img/PS4.svg)")
            if row[2] == 'Xbox':
                readme_file.write(" ![Xbox](img/Xbox.svg)")
            if row[2] == 'Nintendo Switch':
                readme_file.write(" ![NS](img/NS.svg)")
            
            # Check whether the game is free
            if row[3] == '1':
                readme_file.write(" ![Free](img/free.svg)")

            readme_file.write("\n")

