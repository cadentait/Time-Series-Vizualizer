import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates = True, index_col = 'date')

# Clean data
df = df[-(df['value'] < df['value'].quantile(.025))& -(df['value'] > df['value'].quantile(.975))].count()


def draw_line_plot():
    # Draw line plot
    plot = df.plot(figsize = (20,5),
                  kind='line',
                  xlabel = 'Date',
                  ylabel='Page Views',
                  title = 'Daily freeCodeCamp Forum Page Views 5/2016-12/2019',
                  colormap = 'autumn')

    fig = plot.figure
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    #df.insert(1, column='Year', value=df.index.year)
    #df.insert(1, column='Month', value=df.index.month)
    df_new = df.copy().reset_index(inplace=True, parse_dates = True)
    df_new['Year'] = df.index.year
    df_new['Month'] = df.index.month
    bar_df = df_new.groupby(['Year', 'Month'])['value'].agg(np.mean).rename_axis(['Year', 'Month'])

    months = ['January', 
             'February',
             'March',
             'April',
             'May',
             'June',
             'July',
             'August',
             'September',
             'October',
             'November',
             'December']

    
    # Draw bar plot
    plt = bar_df.unstack().plot(figsize = (10,10), kind='bar', xlabel = 'Years', ylabel = 'Average Page Views')
    plt.legend(fontsize = 10, labels = months, title = 'Months')

    fig = plt.figure
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)

    fig, axis = plt.subplots(1,2, figsize=(15,10))

    sns.boxplot(data=df_box, 
                x='year', 
                y='value',
               ax= axis[0]).set(xlabel = 'Year', 
                               ylabel = 'Page Views', 
                               title = 'Year-wise Box Plot (Trend)')
    sns.boxplot(data=df_box, 
                x='month', 
                y='value',
               ax= axis[1],
               order = ['Jan', 'Feb', 'Mar', 'Apr', 
                        'May', 'Jun', 'Jul', 'Aug',
                        'Sep', 'Oct', 'Nov', 'Dec']
               ).set(xlabel = 'Month', 
                     ylabel = 'Page Views', 
                     title = 'Month-wise Box Plot (Seasonality)')  



    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
