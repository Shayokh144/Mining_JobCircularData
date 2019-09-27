
# coding: utf-8

# In[1]:

import pandas as pd
import re


# In[2]:

dataFrame = pd.read_excel("newChakriDotComDataExl.xlsx")


# In[3]:

dataFrame.columns


# ## <span style="color:blue">Number of (Row, Col)</span>

# In[4]:

dataFrame.shape


# ## <span style="color:blue">Finding missing values in each col</span>
# 

# In[5]:

dataFrame.isnull().sum(axis = 0)


# ## <span style="color:blue">Workinh with location Col</span>

# In[6]:

# unique location values
locationList = list(dataFrame.location.unique())
print("num of unique val : ",len(locationList))


# In[7]:

def getSpecificLocationListFormLocationCol(rawLocationList):
    dataList = []
    for text in rawLocationList:
        text = str(text)
        text = text.lower()
        text = text.replace('/',',').replace('&',',')
        text = re.sub('[^a-zA-Z,]','',text)
        arr = text.split(',')
        data = arr[len(arr)-1].strip()
        if "bangladesh" in data:
            dataList.append("anywhere in Bangladesh")
        elif data != 'nan' and 'please' not in data:
            dataList.append(data)
        
    return dataList


# In[8]:

dataList =  getSpecificLocationListFormLocationCol(list(dataFrame.location))
print("specific location list after cleaning:\n", dataList)


# In[9]:

from collections import defaultdict
import operator
def getSortedFrequencyDict(dataList):
    freqDict = defaultdict(int)
    for word in dataList:
        freqDict[word] += 1
    sortedTuple = sorted(freqDict.items(), key=operator.itemgetter(1), reverse = True)
    return freqDict,sortedTuple


# In[10]:

freqDict,sortedTuple = getSortedFrequencyDict(dataList)
print('10 most occured job location: \n',sortedTuple[0:10])


# In[ ]:

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
def buildWordCloudFromDictWithCount(dataDict):
    stpWords = set(STOPWORDS)
    wordcloud =  WordCloud(background_color="black",width=800,height=800, max_words=60,min_font_size=10, stopwords = stpWords).generate_from_frequencies(dataDict)
    fig = plt.figure(figsize = (12,12), facecolor = None)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axix("off")
    plt.tight_layout(pad=0)
    fig.savefig('plot.png')
    plt.show()
    return
buildWordCloudFromDictWithCount(freqDict)


# In[ ]:



