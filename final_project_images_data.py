'''
Author: Tri Cao
Class: ISTA 131
Section Leader: Abby

Description:
This Function will create the images for the final project. It has boxplots, barplots, and scatterplots with 
regression lines.
'''

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import pandas as pd
import numpy as np
import statsmodels.api as sm

def make_frame(fname):
    '''
    This function takes a filename and creates a data frame from the file.
    Parameters:
    :fname: a str, the name of the file being read
    Returns:
    :df: a DataFrame, the dataframe with the values from the file.
    '''
    df = pd.read_excel(fname, usecols= [0,1,2,3,4,6])
    return df

def pop(df, col):
    '''
    This function takes the dataframe give and the specific column name of data being selected.
    It will then go in and remove the rows with ts (tropical storm) in the category list.
    Parameters:
    :df: a DataFrame, this is the dataframe that we will analize
    :col: a str, the name of the  column to be assesed
    Returns:
    :df: a DataFrame, this dataframe has all the tropical storms removed.
    '''
    lst = []
    for i in range(len(df)):
        if df[col][i] == 'ts':
            lst.append(i)
    return df.drop(index = lst)

def get_freq(series):
    '''
    This function will find the frequencies of category of hurricanes
    Parameters:
    :series: a Series, this is the series that we will use to find the frequency of the hurricanes
    Returns:
    :freq: a list, this is the list with the frequencies of the hurricane categories
    '''
    freq = []
    series = series.tolist()
    for i in range(5):
        freq.append(series.count('h'+str(i+1))/len(series))
    return freq

def make_bar(series1, series2):
    '''
    This funciton will create a barplot with the two series parameters.
    Parameters:
    :series1: a Series, this is the first series that we will address, in this case it is the Eastern Carribean Data
    :series2: a Series, this is the second series that we will address, in this case it is the Western Carribean Data
    Returns:
    a plot, this is the plot that we have created.    
    '''
    df = pd.DataFrame(get_freq(series1))
    df[1]= get_freq(series2)
    df.columns = ['Eastern Carribean', 'Western Carribean']
    df.index = ['H1', 'H2', 'H3', 'H4', 'H5']

    n_groups = 5
    index = np.arange(n_groups)
    bar_width = 0.35
    ax = plt.subplot(111)
    ax.bar(index, df['Eastern Carribean'], bar_width, label = 'Eastern Carribean')
    ax.bar(index + bar_width, df['Western Carribean'], bar_width,  label = 'Western Carribean')

    plt.xticks(index + bar_width, ('H1', 'H2', 'H3', 'H4', 'H5'))
    plt.gcf().set_facecolor('lightcyan')
    plt.xlabel('Category', fontsize = 15)
    plt.ylabel('Probability', fontsize = 15)
    plt.title('Total Carribean Hurricanes', fontsize = 25)
    plt.legend()

def windspeed_values(df):
    '''
    This function will get the values of the windspeed from 1850 to 1949 and 1950 to the present.
    Parameters:
    :df: a DataFrame, this is the dataframe that we want to analyze
    Returns:
    :frame: a DataFrame, this is the dataframe with the data for the specified time frame above.
    '''
    lst_1850 = []; lst_1950 =[]
    for i in range(len(df)):
        if df['Year'][i] < 1950:
             if df['wind'][i]>73:
                lst_1850.append(df['wind'][i])
        if df['Year'][i] >= 1950:
            if df['wind'][i]>73:
                lst_1950.append(df['wind'][i])
    std_1850 = np.std(lst_1850)
    std_1950 = np.std(lst_1950)
    std = [std_1850, std_1950]
    lst_1850 = sum(lst_1850)/len(lst_1850)
    lst_1950 = sum(lst_1950)/len(lst_1950)
    years = [lst_1850, lst_1950]
    frame = pd.DataFrame(years,index = ['1850-1949','1950-Present']).T
    frame.loc[1] = std
    frame.index = ['Mean', 'St Dev']
    return frame

def get_total_wind(df1, df2):
    '''
    This function will combind the two dataframes and put it into 1
    Parameters:
    :df1: a DataFrame, this is the first frame that we want to add
    :df2: a DataFrame, this is the second frame that we want to add
    Returns:
    :total_wind: a DataFrame, this is the combined Data Frame.
    '''
    east_wind = windspeed_values(df1).T
    west_wind =windspeed_values(df2).T
    east_wind.loc[3] = west_wind.iloc[0]; east_wind.loc[4] = west_wind.iloc[1]
    east_wind.index = ['1850-1949 (East)','1950-Present (East)', 
            '1850-1949 (West)','1950-Present (West)']
    total_wind = east_wind.T
    return total_wind

def make_box(df):
    '''
    This function will create a box plot with the given data frame
    Parameters:
    :df: a DataFrame, this is the dataframe that we want to use to create a box plot
    Returns:
    a boxplot, this is the boxplot with the data above from the dataframe
    '''
    ax = plt.boxplot(df.T, labels = ['1850-1949 (E)','1950-Present (E)', 
            '1850-1949 (W)','1950-Present (W)'], patch_artist = True)
    plt.gcf().set_facecolor('lightcyan')
    plt.ylabel('Wind Speed (MPH)', fontsize = 24)
    plt.title('Average Wind Speed', fontsize = 25)

def make_scatter(frame):
    '''
    This function creates a scatterplot with the dataframe given and attaches a regression line to it.
    Parameters:
    :frame: a DataFrame, this is the dataframe that we want to use to create the scatter plot
    Returns:
    a scatterplot, this is the scatterplot with the data attached to it and a regression line on it.
    '''
    ax = frame
    ax.plot.scatter('Year', 'wind')

    x = ax['Year']
    X = sm.add_constant(x)
    model = sm.OLS(ax['wind'], X.astype(float))
    line = model.fit()
    line.summary()
    y = line.params['Year']*(x) + line.params['const']
    plt.gcf().set_facecolor('lightcyan')
    plt.plot(x,y, linewidth=2, color = 'red')
    plt.xlabel('Year', fontsize = 15)
    plt.ylabel('Wind Speed (MPH)', fontsize = 15)
    plt.title('Wind Speed of Carribean Hurricanes', fontsize = 24)
#==========================================================
def main():
    '''
    We will create the initial eastern and western dataframes and add them together. We then take the tropical storm
    data out of it in order to make sure the data is only hurricanes. Then we create the plots to represent the 
    data better.
    '''
    # put main code here, make sure each line is indented one level, and delete this comment
    
    western = make_frame( 'western_data.xlsx')
    eastern = make_frame( 'eastern_data.xlsx')
    total_frame = eastern.append(western,ignore_index=True) 
    
    western_nots = pop(western, 'cat.')
    western_nots.sort_values(by= ['cat.'], inplace = True)

    eastern_nots = pop(eastern, 'cat.')
    eastern_nots.sort_values(by= ['cat.'], inplace = True)

    total_nots = pop(total_frame, 'cat.')
    total_nots.sort_values(by= ['cat.'], inplace = True,ignore_index=True)

    e = pd.Series(eastern_nots['cat.'])
    w = pd.Series(western_nots['cat.'])

    
    si = windspeed_values(eastern).T
    we =windspeed_values(western).T
    si.loc[3] = we.iloc[0]
    si.loc[4] = we.iloc[1]
    si.index = ['1850-1949 (East)','1950-Present (East)', 
                '1850-1949 (West)','1950-Present (West)']

    tot = get_total_wind(eastern, western)

    make_bar(e,w)
    plt.figure()
    make_box(tot)
    make_scatter(total_nots)
    plt.show(all)

if __name__ == '__main__':
    main()
