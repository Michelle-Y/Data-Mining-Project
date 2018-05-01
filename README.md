# Be Smart Twitter
**Nicholas Montoya**
**Ziyang Yang**
**Zihan Zhou**

## Description
     Nowadays, social media have tons of users, and millions of people share opinions on different aspects of life everyday. It’s interesting to figure out how people express their sentiments through different words, emojis, etc. This paper and research serves to provide a better understanding about human sentiment on social media, especially in Twitter. Also we want to find the emotions behind a series of words, used to gain an understanding of the attitudes, opinions and emotions expressed within an online mention.
     Our project will serve as a study of sentiment analysis based on Twitter data. The applications of sentiment analysis are broad and powerful. For example, the shifts in sentiment on social media have been shown to correlate with shifts in the stock market. In this project, the research will draw motivation from people to understand and analyze the people’s opinions more efficiently.

## Questions Sought to Answer

### How does people’s mood change according to the time period of a day?  Are any specific words associated with this shift?

From what we found, the sentiment expressed on Twitter does change throughout the day. For example, positive sentiment peaks in the morning while negative sentiment tends to remain relatively constant throughout the day. An interesting item we found is that in negative sentiment clusters in the morning, words like "shop", "purchase", and "buy" have a high frequency. However at night, those same words appear in positive sentiment clusters. Also, we found that tweets have a higher emotional intensity during mid-day times. We believe this is due to the fact that many people are at school or work and may be browsing online. While they are not interacting with friends as much, they are sharing a large amount of URLs that led us to believe people are looking at more news sources during these times.

### How do people use the Emojis/Emoticons (‘:-)’) to express their real sentiments? What are some downfalls in current language processing techniques regarding this and what could improve them?

There are a lot of emojis present in tweets and they can be a bit ambiguous. Vader, the sentiment analysis tool we ended up using in the end, is a popular tool to process natural language from social media posts. We found that sarcastic use of emojis is still hard to interpret and Vader tended to incorrectly score these tweets. We also found a library within NLTK that can look at the preceding and following words in order to account for context.

### How can we apply this knowledge?
Due to what we found about peoples positive and negative sentiment, we could create models for advertising purposes to display ads for purchasing clothes for example in the evening when people seem to have a more receptive view towards spending money. Similarly, we could schedule the release of non-urgent news stories to target the largest amount of viewers.

For improving language processing, if we had more time we would've started this on our own. We believe that taking the set of tweets containing emojis and scoring them differently will produce more accurate results. Vader handles sarcasm already so given the context, it should be able to realize that there is ironic text surrounding the emoji so the value of the smiley face should add to the existing sentiment rather than contradicting it.

## Link to final video:
put link here

## Link to final project paper:
put link here
