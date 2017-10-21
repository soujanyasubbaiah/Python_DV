
# coding: utf-8

# BUAN 6340 - Homework 1

# In[1]:

import numpy 
import matplotlib.pyplot as plt
import csv
import os
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.plotly as py
import plotly.graph_objs as go
get_ipython().magic('matplotlib inline')

os.chdir('C:/Users/souja/Desktop/Python HW 1/') #User's path goes here


# Loading Data from 4 different years

# In[2]:

f='all_house_senate_2010.csv'
d2010 = pd.read_csv(f, dtype={"dis_amo": str}) 

f='all_house_senate_2012.csv'
d2012 = pd.read_csv(f, dtype={"dis_amo": str}) 

f='all_house_senate_2014.csv'
d2014 = pd.read_csv(f, dtype={"dis_amo": str}) 

f='all_house_senate_2016.csv'
d2016 = pd.read_csv(f, encoding='ISO-8859-1', dtype={"dis_amo": str}) 


# Concatenating data from 4 years to one data frame

# In[3]:

data = pd.concat([d2010, d2012, d2014, d2016])
len(data)


# Data cleaning - Removed '$' and ',' from column dis_amo

# In[4]:

data['dis_amo'] = data['dis_amo'].str.replace('$', '') 
data['dis_amo'] = data['dis_amo'].str.replace(',', '') 
data['dis_amo'] = data['dis_amo'].astype(float)


# In[5]:

# There were 2 values: CREDIT CARD PROCESSING FEES/CREDIT CARD PROCESSING FEE. Replaced them to match cause they both mean the same
data['dis_pur_des'] = data['dis_pur_des'].str.replace('CREDIT CARD PROCESSING FEES', 'CREDIT CARD PROCESSING FEE')


#         Visualizations

# Bar graph to show the No of candidates in each year

# In[6]:

#Dataframe showing no of candidates each year
No_of_can = data.groupby('ele_yea').can_id.nunique()
No_of_can = pd.DataFrame({'Year':No_of_can.index, 'No of Candidates':No_of_can.values})

#Plotting graph
import plotly
from plotly.graph_objs import Scatter, Layout
plotly.offline.init_notebook_mode(connected=True)

#Plotting the graph
trace1 = go.Bar(
    x= No_of_can['Year'],
    y= No_of_can['No of Candidates'],
    name='No. of candidates each year'
)
data1 = [trace1]
layout = go.Layout(
    barmode='group', title='No of candidates each year',xaxis = dict(title = 'Year'),yaxis = dict(title = 'No of candidates')
)

fig = go.Figure(data=data1, layout=layout)
plotly.offline.iplot(fig, filename='width-bar')


# Interestingly, the no of candidates has decreased yearly. 2010 had the highest no of candidates and 2016 had the least

# .....

# Bar graph to show Average Expenditure in each year

# In[7]:

#Plotting graph
bar = sns.barplot(x='ele_yea',y='dis_amo',data=data, palette='rainbow')
bar.set(xlabel='YEAR', ylabel='Average Disbursement Amount', title='AVERAGE EXPENDITURE EACH YEAR')


# 2012 has the highest avg expenditure. 2014 had the least expenditure.

# ....

# Violin plot for Yearly Expenditure according to the Type of Office 
#    (H- House,
#    S- Senate,
#    P- President)

# In[8]:

sns.set(style="ticks")
b = sns.factorplot(x="ele_yea", y="dis_amo", data=data, kind= 'violin', size = 7, palette= 'Set1' ,hue= 'can_off')
b.fig.get_axes()[0].set_yscale('log')
b.set(xlabel= 'YEAR',ylabel= 'DISBURSEMENT AMOUNT', title='OFFICE-WISE EXPENDITURE EACH YEAR')


# ....

# Graph depicting Candidates with the highest expenditure between 2010-2016

# In[9]:

#Data showing the top 10 candidates that had the highest expenditure
can_amt_spent = data.groupby('can_nam').sum()['dis_amo']
can_amt_spent = can_amt_spent.nlargest(10)
can_amt_spent = pd.DataFrame({'Candidate':can_amt_spent.index, 'Total amount spent':can_amt_spent.values})
can_amt_spent


# In[10]:

plot = sns.factorplot(x= 'Total amount spent', y='Candidate',data=can_amt_spent, palette='Set1', size=7)
plot.fig.get_axes()[0].set_xscale('log')
plot.set(title='CANDIDATES WITH HIGHEST EXPENDITURE', xlabel='Total amount spent', ylabel='Candidate Name')
plt.show()
# a.info()


# Linda McMahon spent the highest and a substantially higher amount than the second candidate, Rob Portman.

# ....

# Graph showing top reasons of expenditure

# In[11]:

#Data showing top 'Purpose of expenditure'
topPurpose = data['dis_pur_des'].value_counts()
topPurpose = topPurpose.head(20)
topPurpose = pd.DataFrame({'Disbursement Purpose':topPurpose.index, 'Number of Disbursements':topPurpose.values})
topPurpose


# In[12]:

ax = sns.factorplot(x="Number of Disbursements", y="Disbursement Purpose", data=topPurpose, palette='Set1', kind='bar', size=7)
ax.set(title='TOP PURPOSE of EXPENDITURE', xlabel='Number of Disbursements', ylabel='PURPOSE')


# Payroll and salary had the highest expenditure, followed by travel

# ....

# Graph showing Top Categories of expenditure in each year

# In[13]:

#Preparing data for each year
d2010['dis_amo'] = d2010['dis_amo'].str.replace('$', '') 
d2010['dis_amo'] = d2010['dis_amo'].str.replace(',', '') 
d2010['dis_amo'] = d2010['dis_amo'].astype(float)

d2012['dis_amo'] = d2012['dis_amo'].str.replace('$', '') 
d2012['dis_amo'] = d2012['dis_amo'].str.replace(',', '') 
d2012['dis_amo'] = d2012['dis_amo'].astype(float)

d2014['dis_amo'] = d2014['dis_amo'].str.replace('$', '') 
d2014['dis_amo'] = d2014['dis_amo'].str.replace(',', '') 
d2014['dis_amo'] = d2014['dis_amo'].astype(float)

d2016['dis_amo'] = d2016['dis_amo'].str.replace('$', '') 
d2016['dis_amo'] = d2016['dis_amo'].str.replace(',', '') 
d2016['dis_amo'] = d2016['dis_amo'].astype(float)

#Top 5 categories in each year
d10 = d2010.groupby('cat_des').agg({'dis_amo':'sum'}).reset_index().sort_values('dis_amo', ascending=0).rename(columns={'dis_amo':'Total Disbursement', 'cat_des':'Category'}).head(5)
d12 = d2012.groupby('cat_des').agg({'dis_amo':'sum'}).reset_index().sort_values('dis_amo', ascending=0).rename(columns={'dis_amo':'Total Disbursement', 'cat_des':'Category'}).head(5)
d14 = d2014.groupby('cat_des').agg({'dis_amo':'sum'}).reset_index().sort_values('dis_amo', ascending=0).rename(columns={'dis_amo':'Total Disbursement', 'cat_des':'Category'}).head(5)
d16 = d2016.groupby('cat_des').agg({'dis_amo':'sum'}).reset_index().sort_values('dis_amo', ascending=0).rename(columns={'dis_amo':'Total Disbursement', 'cat_des':'Category'}).head(5)



# In[14]:

#Plotting graph

from plotly import tools
trace1 = go.Scatter( 
   x = d10['Category'],
   y = d10['Total Disbursement'],
   mode = 'line',
   name = '2010',
   marker = dict(
      size = 10,
      color = 'rgba(255, 190, 193, .9)',
      line = dict(
          width = 2
      )
   )
)
  
trace2 = go.Scatter( 
   x = d12['Category'],
   y = d12['Total Disbursement'],
   mode = 'line',
   name = '2012',
   marker = dict(
      size = 10,
      color = 'rgba(255, 190, 193, .9)',
      line = dict(
          width = 2
      )
       
   )
)
trace3 =  go.Scatter( 
   x = d14['Category'],
   y = d14['Total Disbursement'],
   mode = 'line',
   name = '2014',
   marker = dict(
      size = 10,
      color = 'rgba(255, 190, 193, .9)',
      line = dict(
          width = 2
      )
   )
)
trace4 = go.Scatter( 
   x = d16['Category'],
   y = d16['Total Disbursement'],
   mode = 'line',
   name = '2016',
   marker = dict(
      size = 10,
      color = 'rgba(255, 190, 193, .9)',
      line = dict(
          width = 2
      )
   )
)

fig = tools.make_subplots(rows=2, cols=2, subplot_titles=('2010 - Top Categories', '2012 - Top Categories',
                                                         '2014 - Top Categories', '2016 - Top Categories'))

fig.append_trace(trace1, 1, 1)
fig.append_trace(trace2, 1, 2)
fig.append_trace(trace3, 2, 1)
fig.append_trace(trace4, 2, 2)

fig['layout'].update(margin=go.Margin(t=50, b=120), height=800, width=900, title='Top 5 Categories' +
                                                 ' with highest disbursement each year')

plotly.offline.iplot(fig, filename='make-subplots-multiple-with-titles')


# "Administrative/Salary/Overhead" has had the highest expenses in all years. The expenditure on Advertising is a top category from 2012 onwards.
# Travel expenditure increased in 2016.
# 

# ....

# Graph showing Total Expenditure in each State on the US map

# In[15]:

import plotly.plotly as py
import pandas as pd
import plotly
from plotly.graph_objs import Scatter, Layout
plotly.offline.init_notebook_mode(connected=True)


df = data

for col in df.columns:
    df[col] = df[col].astype(str)

scl = [[0.0, 'rgb(242,240,247)'],[0.2, 'rgb(218,218,235)'],[0.4, 'rgb(188,189,220)'],            [0.6, 'rgb(158,154,200)'],[0.8, 'rgb(117,107,177)'],[1.0, 'rgb(84,39,143)']]

#Creating a list with all State abbreviations
df['can_off_sta'].unique()
states=list(set(df['can_off_sta']))
# state_dis_amo[states]


# In[16]:

#Plotting graph
import plotly.plotly as py
import pandas as pd
import plotly
from plotly.graph_objs import Scatter, Layout
plotly.offline.init_notebook_mode(connected=True)

#Dataframe that contains Total expenditure in each state
df['dis_amo'] =  df['dis_amo'].astype(float)

state_dis_amo = df.groupby('can_off_sta').sum()['dis_amo']
state_no_candidates = df.groupby('can_off_sta').can_id.nunique()


data3 = [ dict(
        type='choropleth',
        colorscale = scl,
        autocolorscale = True,
        locations = states,
        z = state_dis_amo[states],
        locationmode = 'USA-states',
#         text = df['text'],
        marker = dict(
            line = dict (
                color = 'rgb(255,255,255)',
                width = 2
            ) ),
        ) ]

layout = dict(
        title = 'State-wise total disbursements',
        geo = dict(
            scope='usa',
            projection=dict( type='albers usa' ),
            showlakes = False,
            lakecolor = 'rgb(255, 255, 255)'),
             )
    
fig = dict( data=data3, layout=layout )
plotly.offline.iplot( fig, filename='d3-cloropleth-map' )
# py.iplot( fig, filename='d3-cloropleth-map' )


# Hover over each state to see the expenditure. California has the highest and Wyoming has the least expenditure. 

# ....

# Graph showing No of candidates in each state on US map

# In[17]:

#Dataframe that contains No of candidates in each state
state_no_candidates = df.groupby('can_off_sta').can_id.nunique()

#Plotting graph
data4 = [ dict(
        type='choropleth',
        colorscale = scl,
        autocolorscale = False,
        locations = states,
        z = state_no_candidates[states],
        locationmode = 'USA-states',
#         text = df['text'],
        marker = dict(
            line = dict (
                color = 'rgb(255,255,255)',
                width = 2
            ) ),
        ) ]

layout = dict(
        title = 'State-wise no. of candidates',
        geo = dict(
            scope='usa',
            projection=dict( type='albers usa' ),
            showlakes = True,
            lakecolor = 'rgb(255, 255, 255)'),
             )
    
fig = dict( data=data4, layout=layout )
plotly.offline.iplot( fig, filename='d3-cloropleth-map' )
# py.iplot( fig, filename='d3-cloropleth-map')


# Hover over each state to see the No of candidates. California has the highest and Vermont has the least. 

# ....

# I was curious about how much of the expenditure went to charitable causes. So i did some analyses based on charitable donations.

# Graph that shows the total amount spent on Charity each year

# In[18]:

#Creating a DF that has only the disbursements toward Charity/Donation
char_yea = data[data['dis_pur_des'].str.contains("charity", na=False, case=False)
              | data['dis_pur_des'].str.contains("donation", na=False, case=False)
              | data['dis_pur_des'].str.contains("charitable", na=False, case=False)]

#Total amount to Charity every year
char_yea = char_yea.groupby('ele_yea').agg({'dis_amo' :sum}).reset_index()
char_yea = char_yea.sort_values('dis_amo' , ascending=0).rename(columns={'ele_yea' : 'Year', 'dis_amo' : 'AMOUNT SPENT ON CHARITY'})
char_yea = char_yea.sort_values('Year')


# In[19]:

#Plotting graph
import plotly.plotly as py
import plotly.graph_objs as go

trace1 = go.Scatter(
    x = char_yea['Year'],
    y = char_yea['AMOUNT SPENT ON CHARITY'],
    line = dict(
        color = ('rgb(205, 12, 167)'),
        width = 6,)
)
data_don = [trace1]

# Edit the layout
layout = dict(title = 'Trend of Charitable Donations by Year',
              xaxis = dict(title = 'Year'),
              yaxis = dict(title = 'Total Amount donated'),
              )

fig = dict(data=data_don, layout=layout)
plotly.offline.iplot(fig, filename='styled-line')


# Donations to charity saw a downward trend from 2010 to 2014 and increased again in 2016. It was the highest in 2010 and least in 2014.

# ....

# Stacked Bar Chart showing proportion of Amount spent on Charity vs Others each year

# In[20]:

#Creating a DF that has only the disbursements toward Charity/Donation
char_s = data[data['dis_pur_des'].str.contains("charity", na=False, case=False)
              | data['dis_pur_des'].str.contains("donation", na=False, case=False)
              | data['dis_pur_des'].str.contains("charitable", na=False, case=False)]


#Avg amount spent on Charity
char_s = char_s.groupby('ele_yea').agg({'dis_amo' :'mean'}).reset_index()
char_s


# In[21]:

#Creating a DF that has only the disbursements toward Others(non-Charity)
oth = data[(data['dis_pur_des'].str.contains("charity", na=False, case=False) == False)
              | (data['dis_pur_des'].str.contains("donation", na=False, case=False) == False)
              | (data['dis_pur_des'].str.contains("charitable", na=False, case=False) == False)]

#Avg amount spent on Non-Charity
oth = oth.groupby('ele_yea').agg({'dis_amo':'mean'})
oth = oth.reset_index().rename(columns={'dis_amo':'Average Expenditure' })
oth


# In[22]:

#Plotting graph

import plotly
from plotly.graph_objs import Scatter, Layout
plotly.offline.init_notebook_mode(connected=True)

trace1 = go.Bar(
    x=char_s['ele_yea'],
    y=char_s['dis_amo'],
    name='Charity'
)
trace2 = go.Bar(
    x=oth['ele_yea'],
    y=oth['Average Expenditure'],
    name='Others'
)

data2 = [trace2, trace1]
layout = go.Layout(title='Average Amount spent on Charity vs Others', 
              xaxis = dict(title = 'Year'),
    barmode='stack'
)

fig = go.Figure(data=data2, layout=layout)
plotly.offline.iplot(fig, filename='grouped-bar')


# The proportion of Charity to Other Expenses is almost the same through the years. Approximately 30-35% of the total expenditure was to Charity. 

# ....

# Heatmap showing Ten Candidates that donated the highest to Charity 

# In[23]:

#Creating a DF that has only the disbursements toward Charity/Donation
charity = data[data['dis_pur_des'].str.contains("charity", na=False, case=False)
              | data['dis_pur_des'].str.contains("donation", na=False, case=False)
              | data['dis_pur_des'].str.contains("charitable", na=False, case=False)]


#Top 20 candidates that made the highest payment to charity
charity = charity.groupby('can_nam').agg({'dis_amo' :sum}).reset_index()
charity = charity.sort_values('dis_amo' , ascending=0).tail(1).rename(columns={'can_nam' : 'Candidate', 'dis_amo' : 'AMOUNT SPENT ON CHARITY'})
charity


# In[24]:

#Plotting graph
e = charity.pivot_table(values='AMOUNT SPENT ON CHARITY',columns='Candidate')
sns.heatmap(e)


# In[58]:

a = data[data['ele_yea'].str.contains("2016", na=False, case=False)]

a.groupby('can_nam').agg({'dis_amo':'sum'}).sort_values('dis_amo', ascending=0).head(10)


# Elijah Cummings had the highest expenses for Charity.
