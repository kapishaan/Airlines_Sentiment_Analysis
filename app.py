import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

st.title('Sentimental Analysis')


# createing a sidebar Widget
st.sidebar.title("Customization")
st.sidebar.markdown("Additional filters and customizations")
st.markdown("This is the application regarding Sentimental Analysis")

DATA_URL = "data/Tweets.csv"

# Load data
@st.cache_data(persist = True)
def load_data(data_url):
    data = pd.read_csv(data_url)
    data['tweet_created'] = pd.to_datetime(data["tweet_created"])
    return data

data = load_data(DATA_URL)

#adding widgets to sidebar

st.sidebar.subheader("show random tweets")
random_tweets = st.sidebar.radio('sentimentaltype',('positive', 'negative', 'neutral'), key = "sentiment_radio")

#query dataframe for random tweets

st.subheader("Random tweets")
st.markdown(data.query('airline_sentiment == @random_tweets')[["text"]].sample(n=1).iat[0,0])

# data visualization

st.subheader("Visualization")
st.sidebar.markdown("Number of tweets by sentiment")


#select box widget
select = st.sidebar.selectbox("Visualization_Type:",['Histogarm','Pie Chart'], key = '2')
sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count_df = pd.DataFrame({'sentiment':sentiment_count.index,'tweets':sentiment_count.values})

if not st.sidebar.checkbox("Hide_Visualization",True):
    st.markdown("Number of tweets by sentiment")    
    if select == "Histogram":
        fig = px.bar(sentiment_count_df ,x ='sentiment' ,y ='tweets' ,color = 'tweets' ,height=500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count_df, values ='tweets', names ='sentiment') 
        st.plotly_chart(fig)

st.sidebar.subheader("When and Where users are tweeting from?")
hour = st.sidebar.slider("Hour of Day", 0,23)
modified_data = data[data['tweet_created'].dt.hour == hour]

if not st.sidebar.checkbox("Hide Tweets Map", True, key = 'map_checkbox'):
    st.markdown("### Tweet locations based on the time of day")
    st.markdown("%i tweets between %i:00 and %i:00" % (len(modified_data), hour, (hour + 1)% 24))
    st.map(modified_data)
    if st.sidebar.checkbox("Show raw data table", False):
        st.write(modified_data)

st.sidebar.subheader("breakdown airline tweets by sentiment")
choice = st.sidebar.multiselect('Pick airlines',
                                ('US Airways', 'United', 'American', 'Southwest', 'Delta', 'Virgin america'), key="3")

if len(choice) > 0:
    choice_data = data[data.airline.isin(choice)]
    fig_choice = px.histogram(choice_data, x='airline', y='airline_sentiment', histfunc = 'count',
                              color = 'airline_sentiment',
                              facet_col = 'airline_sentiment',
                              labels = {'airline_senitment': 'tweets'}, height = 600, width = 800)
    st.plotly_chart(fig_choice)

st.sidebar.header("World Cloud")
word_sentiment = st.sidebar.radio('Display WorldCloud for sentiment:', ('positive','negative','neutral'),key = '4')

if not st.sidebar.checkbox("Hide WorldCloud", True, key = '5'):
    st.subheader("Word cloud")
    df = data[data['airline_sentiment'] == word_sentiment]
    word = ''.join(df['text'])

    processed_words = ''.join(
        [word for word in word.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color ='White', width =800, height= 640).generate(
        processed_words)
    wordcloud_fig = plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()






