#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on a day with no parking space


Student Name: Emmett Fitzharris

Student ID: R00222357

Cohort: evSD3

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt




def task1():
    moviesDf = pd.read_csv("movies.csv")

    # find unique genres
    numUnique = moviesDf['main_Genre'].nunique()
    print(f'{numUnique}\n')
    
    
    # group by main_genre
    groupDF = moviesDf.groupby('main_Genre')
    
    countPerGenre = groupDF['Title'].count().sort_values(ascending = False)
    
    
    # find max and min
    maxCount = countPerGenre.max()
    maxTitle = countPerGenre.idxmax() # research https://stackoverflow.com/questions/19818756/extract-row-with-maximum-value-in-a-group-pandas-dataframe
    print(f'{maxTitle} \n')
    
    minCount = countPerGenre.min()
    minTitle = countPerGenre.idxmin()
    print(f'{minTitle}\n')

    #find top 8
    top8 =countPerGenre.head(8)
    print(f'{top8}\n')


    # bar chart
    genres = top8.index
    movieCounts = top8.values

    plt.figure(figsize=(10, 6))
    plt.bar(genres, movieCounts, color='skyblue')
    plt.title('Top 8 Popular Genres')
    plt.xlabel('Genre')
    plt.ylabel('Number of Movies')
    
    minimumY =  min(movieCounts*0.95)
    plt.ylim(bottom=minimumY)
    plt.show()
    


def task2():
    moviesDf = pd.read_csv("movies.csv")


    # Split the 'Genre' column by comma into lists and then 'explode' it into separate rows for each genre    
    splitGenres = moviesDf['Genre'].str.split(',').explode()  # research https://stackoverflow.com/questions/12680754/split-explode-pandas-dataframe-string-entry-to-separate-rows
    
    #clean data
    cleanedGenres = splitGenres.str.strip()  
    genre_counts = cleanedGenres.value_counts()
    
    
    # Find the most and least common genre
    maxTitle = genre_counts.idxmax()
    minTitle = genre_counts.idxmin()

    
    print(f'{maxTitle}\n')    
    print(f'{minTitle}\n')

    
    
def task3(): # note: determined there are no low outliers, as the iqr * 1.5 brings the lower bound to a negative value. All low values are expected. 
    moviesDf = pd.read_csv("movies.csv")
    
    # Clean the 'Runtime' column
    moviesDf['Runtime'] = moviesDf['Runtime'].str.strip(' min').apply(pd.to_numeric, errors='coerce')

    
    # Calculate the first (Q1) and third (Q3) quartiles, and Inter Quartile Range
    quantile = moviesDf['Runtime'].quantile([0.25, 0.75])
    q1 = quantile[0.25]
    q3 = quantile[0.75]
    iqr = q3 - q1
    
    
    # lower and upper bounds for detecting outliers
    lower = q1 - (1.5 * iqr)
    upper = q3 + (1.5 * iqr)
    

    outliers = moviesDf[(moviesDf['Runtime'] < lower) | (moviesDf['Runtime'] > upper)]
    print(outliers[['Title', 'Runtime']].sort_values('Runtime', ascending = False))
    
    
    #boxplot
    plt.boxplot(moviesDf['Runtime'].dropna(), vert=False)  
    plt.title("Boxplot of Movie Runtimes")
    plt.xlabel("Runtime (minutes)")
    plt.show()
    
    
def task4():
    moviesDf = pd.read_csv("movies.csv")

    # Note, no null values were found. I confirmed this result with excels COUNTBLANK function, which agreed with my result in Pandas. 
    # I also checked to ensure that all entries were numeric, which did not result in any NaN values
    
    # ensuring values are numeric
    moviesDf['Rating'] = moviesDf['Rating'].apply(pd.to_numeric, errors='coerce')
    moviesDf['Number of Votes'] = moviesDf['Number of Votes'].apply(pd.to_numeric, errors='coerce')
    
    # checking for null values
    condition = moviesDf['Rating'].isnull() | moviesDf['Number of Votes'].isnull()
    filteredDf = moviesDf[condition]
    
    
    if filteredDf.empty:
        print("There are no null values in either the 'Rating' or 'Number of Votes' columns")
    else:
        print(moviesDf[condition])    
        
        moviesDf['Rating'] = moviesDf['Rating'].fillna(moviesDf['Rating'].mean()) # research https://stackoverflow.com/questions/18689823/pandas-dataframe-replace-nan-values-with-average-of-columns
        moviesDf['Number of Votes'] = moviesDf['Number of Votes'].fillna(moviesDf['Number of Votes'].mean())
        
        
    print(moviesDf['Rating'].corr(moviesDf['Number of Votes'])) 
    
    # Research: https://www.geeksforgeeks.org/how-to-calculate-correlation-between-two-columns-in-pandas/
    # This uses the Pearson Correlation Coeficient method, to compare the two values. 
    # Results can range from -1 to 1. This case returns a value of 0.2934730718727734
    # The above indicated that there seems to be a positive relationship between the two values
    
    plt.scatter(moviesDf['Rating'], moviesDf['Number of Votes'])
    plt.title('Relationship between Rating and Number of Votes')
    plt.xlabel('Rating')
    plt.ylabel('Number of Votes')
    plt.show()
        
    
    
def task5():
    # Read the movie and genre data
    moviesDf = pd.read_csv("movies.csv")
    genresDf = pd.read_csv("main-genre.txt", sep='\t')
    
    
    # Transpose the genre DataFrame and reset the index
    transposedGDf = genresDf.transpose().reset_index() 
    
    
    # Rename columns and drop the first row
    transposedGDf.columns = transposedGDf.iloc[0]
    transposedGDf = transposedGDf.drop(transposedGDf.index[0])
    
    
    # Clean the 'Synopsis' column
    moviesDf['Synopsis'] = moviesDf['Synopsis'].str.lower()
    moviesDf['Synopsis'] = moviesDf['Synopsis'].str.replace("[',.-]", "", regex=True)
    
    
    
    for col in transposedGDf.columns:
        #clean genre descriptions
        transposedGDf [col] = transposedGDf [col].str.lower()
        transposedGDf [col] = transposedGDf [col].str.replace("[',.-]", "", regex=True)
        
        # Combine descriptions into a single regular expression pattern
        descriptions = '|'.join(transposedGDf[col].dropna())
        pattern = r'\b{}\b'.format(descriptions)

        # Use regEx to get only the correct rows
        moviesDf[col] = moviesDf['Synopsis'].str.contains(pattern, case=False, regex=True)
    
        genreMovies = moviesDf[moviesDf[col]][['Title', col, 'main_Genre']]
        
        
        mostCommonGenre = genreMovies['main_Genre'].value_counts().idxmax()
        
        print(f"{col} {mostCommonGenre}")
        print()
        

    
    
def task6():
    
    """
    your code
    """
    moviesDf = pd.read_csv("movies.csv")

    
    # I will create a query which checks if there is a correlation between the number of films a director creates per year, and the mean rating. 
    # This is to check if quality over quantity holds true. 
    
    # Get the director's name from 'Cast Column. The column has multiple values separated by '|'
    moviesDf['Director'] = moviesDf['Cast'].str.split('|').str.get(0).str.replace('Director:', '').str.split(',').str.get(0).str.strip()
    
    directorStats = moviesDf.groupby(['Director', 'Release Year']).agg({'Title': 'count', 'Rating': 'mean'}).reset_index()
    directorStats.rename(columns={'Title': 'Films', 'Rating': 'Rating'})
    
    #find correlation
    correlation = directorStats['Number of Films'].corr(directorStats['Average Rating'])
    print("Correlation between the number of films and average rating: ", correlation)
    
    #scatterplot
    plt.scatter(directorStats['Films'], directorStats['Rating'], alpha=0.5)
    
    # From the result of -0.08195401149349008, there does not seem to be signifigant evidance of a positive or negative relationship. 
    # there are some extreme outliers however, which may indicate a mistake in logic
    
    plt.title('Number of Films vs. Average Rating by Director and Year')
    plt.xlabel('Number of Films')
    plt.ylabel('Average Rating')
    plt.show()
    

    
def main():
    task5()
    
    
if __name__ == '__main__':
    main()