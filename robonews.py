from GoogleNews import GoogleNews
import nltk
from newspaper import Article
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
nltk.download('punkt')
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from GoogleNews import GoogleNews
from newspaper import Article
from newspaper import Config
import pandas as pd
import nltk
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import matplotlib
matplotlib.axes.Axes.pie
matplotlib.pyplot.pie

#Pesquisa que funciona sucesso
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.103 Safari/537.36'
config = Config()
config.browser_user_agent = user_agent
config.request_timeout = 9

googlenews=GoogleNews(start='02/20/2020',end='02/23/2021',lang="pt")
googlenews.search('eletrobras,hidroeletricas,dolar')
result=googlenews.result()
df=pd.DataFrame(result)
print(df.head())
for i in range(2,3):
    googlenews.getpage(i)
    result=googlenews.result()
    df=pd.DataFrame(result)
list=[]
textos = []
analyzer = SentimentIntensityAnalyzer()
notas = []

for ind in df.index:
    dict={}
    article = Article(df['link'][ind],config=config)
    article.download()
    article.parse()
    article.nlp()
    dict['Date']=df['date'][ind]
    dict['Media']=df['media'][ind]
    dict['Title']=article.title
    dict['Article']=article.text
    dict['Summary']=article.summary
    dict['Notas']=analyzer.polarity_scores(article.summary)['compound']
    notas.append(analyzer.polarity_scores(article.summary)['compound'])
    textos.append(article.summary)

    list.append(dict)
news_df=pd.DataFrame(list)
news_df.to_excel("articles.xlsx")
#news_df

nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('portuguese')#set(STOPWORDS)

tudo = " ".join(s for s in textos)

wordcloud2 = WordCloud(stopwords=stopwords,background_color="black",
                      width=1600, height=800).generate(tudo)
plt.imshow(wordcloud2)
plt.axis("off")
plt.savefig("petrobras.png")
plt.show()

somatorio = 0
total = len(notas)
sentimento = []
positivo = 0
negativo = 0
neutro = 0
labels = 'Positivo', 'Negativo', 'Neutro'
for n in notas:
  somatorio = somatorio + n
  if(n > 0):
    positivo = positivo + 1    
  elif(n < 0):
    negativo = negativo + 1    
  else:   
    neutro = neutro + 1
    
sentimento.append(positivo)
sentimento.append(negativo)
sentimento.append(neutro)

# print("Total " + str(somatorio))
# print("Média " + str(somatorio/total))

#news_df.plot.pie(y='Notas', figsize=(5, 5))


#add colors
colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']

# Creating plot 
fig = plt.figure(figsize =(10, 7)) 
plt.pie(sentimento, labels = labels, autopct='%1.0f%%', pctdistance=0.7, labeldistance=1.2,shadow=True, startangle=5,colors=colors,textprops={'fontsize': 23})
plt.axis('equal')  

# show plot 
plt.tight_layout()
plt.savefig("pizza.png")
plt.show() 
