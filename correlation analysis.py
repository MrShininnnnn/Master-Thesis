# coding: utf-8
import numpy as np
import pandas as pd
import time
import datetime

np.random.seed(12)

get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns; sns.set(color_codes=True)

plt.rcParams['axes.labelsize'] = 14
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12
matplotlib.rcParams['axes.unicode_minus']=False
sns.set_style("darkgrid",{"font.sans-serif":['simhei', 'Arial']})
pd.options.mode.chained_assignment = None  # default='warn'
pd.options.display.max_columns = 999

data = pd.read_csv('data_set_v2.csv')
# ['scopus' 'doi' 'title' 'type' 'year' 'source' 'page' 'volume'
#  'reader_count' 'link' 'given-name' 'sur_name' 'citedby_count' 'h_index'
#  'doc_total' 'citeby_doc' 'coauthors_total']
data = data.drop(['scopus','doi'],axis=1)
data.info()

data = data.drop(['title','source','link','page','volume','given-name','sur_name'],axis=1)
data.drop_duplicates()
data = data.dropna(how='any')
data.info()
# Features to represent the first author’s academic capital consists of 
# 1. h-index, 
# 2. cited by count, 
# 3. document count,
# 4. cited by document count,
# 5. co-authors count
data.describe()

sum_type = data.groupby('type').size()
print(sum_type)
sum_type.describe()

sum_year = data.groupby('year').size()
print(sum_year)
sum_year.describe()

fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(12,12))
# citedby_count
ax1 = data.plot.scatter(x='citedby_count', y='reader_count', color='#4473C5', fontsize=12, ax=axes[0,0])
ax1.set_xlabel('citedby_count', fontsize=15)
ax1.set_ylabel('reader_count', fontsize=15)
# h_index
ax2 = data.plot.scatter(x='h_index', y='reader_count', color='#4473C5', fontsize=12, ax=axes[0,1])
ax2.set_xlabel('h_index', fontsize=15)
ax2.set_ylabel('reader_count', fontsize=15)
# doc_total
ax3 = data.plot.scatter(x='doc_total', y='reader_count', color='#4473C5', fontsize=12, ax=axes[1,0])
ax3.set_xlabel('doc_total', fontsize=15)
ax3.set_ylabel('reader_count', fontsize=15)
# citedby_doc
ax4 = data.plot.scatter(x='citedby_doc', y='reader_count', color='#4473C5', fontsize=12, ax=axes[1,1])
ax4.set_xlabel('citedby_doc', fontsize=15)
ax4.set_ylabel('reader_count', fontsize=15)
# coauthors_total
ax5 = data.plot.scatter(x='coauthors_total', y='reader_count', color='#4473C5', fontsize=12, ax=axes[2,0])
ax5.set_xlabel('coauthors_total', fontsize=15)
ax5.set_ylabel('reader_count', fontsize=15)
# reader_count
ax6 = data.plot.scatter(x='reader_count', y='reader_count', color='#4473C5', fontsize=12, ax=axes[2,1]);
ax6.set_xlabel('reader_count', fontsize=15)
ax6.set_ylabel('reader_count', fontsize=15)

matplotlib.rc("legend", fontsize=20)

JG1 = sns.lmplot("citedby_count", "reader_count", data=data, size=5)
plt.xlabel('citedby_count', fontsize=18)
plt.ylabel('reader_count', fontsize=18)

JG2 = sns.lmplot("h_index", "reader_count", data=data, size=5)
plt.xlabel('h_index', fontsize=18)
plt.ylabel('reader_count', fontsize=18)

JG3 = sns.lmplot("doc_total", "reader_count", data=data, size=5)
plt.xlabel('doc_total', fontsize=18)
plt.ylabel('reader_count', fontsize=18)

JG4 = sns.lmplot("citedby_doc", "reader_count", data=data, size=5)
plt.xlabel('citedby_doc', fontsize=18)
plt.ylabel('reader_count', fontsize=18)

JG5 = sns.lmplot("coauthors_total", "reader_count", data=data, size=5)
plt.xlabel('coauthors_total', fontsize=18)
plt.ylabel('reader_count', fontsize=18)

sns.jointplot(x="citedby_count", y="reader_count", data=data, size=5)
plt.xlabel('citedby_count', fontsize=18)
plt.ylabel('reader_count', fontsize=18)

g = sns.lmplot(x='citedby_count', y='reader_count', col='year',data=data, col_wrap=3, size=3)
g = g.set(xlim=(0, 800), ylim=(0, 750),xticks=[200, 400, 800], yticks=[250, 500, 750]).fig.subplots_adjust(wspace=.02)

data0 = data[['reader_count', 'citedby_count','h_index', 'doc_total', 'citedby_doc', 'coauthors_total']]
corr = data0.corr()

sns.set(font_scale=2)
fig, ax = plt.subplots(figsize=(10,10))
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True
cmap = sns.diverging_palette(220, 10, as_cmap=True)
sns.heatmap(corr, mask=mask, cmap='Blues', vmax=.7,
            center=0,square=True, linewidths=.5,
            cbar_kws={"shrink": .5},ax=ax)

corr

from sklearn.cross_validation import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, matthews_corrcoef
from sklearn.linear_model import LinearRegression

X = data0[['citedby_count']]
y = data0[['reader_count']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)
print(X_train.shape, y_train.shape)
print (X_test.shape, y_test.shape)

linreg = LinearRegression()
model=linreg.fit(X_train, y_train)
y_pred = model.predict(X_test)
      
print('Coefficients:', linreg.coef_)
print("Mean squared error: %.2f" % mean_squared_error(y_test, y_pred))
print('Variance score: %.3f' % r2_score(y_test, y_pred))
print(model.get_params(deep=True))

import statsmodels.api as sm

model = sm.OLS(y_train, X_train)
res = model.fit()
res.params
print(res.summary())

from scipy.stats import pearsonr

def calculate_pvalues(df):
    df = df.dropna()._get_numeric_data()
    dfcols = pd.DataFrame(columns=df.columns)
    pvalues = dfcols.transpose().join(dfcols, how='outer')
    for r in df.columns:
        for c in df.columns:
            pvalues[r][c] = round(pearsonr(df[r], df[c])[1], 4)
    return pvalues

calculate_pvalues(data0)

