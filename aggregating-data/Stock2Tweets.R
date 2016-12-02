
#map the rows to the data frame
library(lubridate)

StockPrices <- read.csv("~/Documents/StockPrices.csv", stringsAsFactors = FALSE)
Tweets <- read.csv("~/Documents/Tweets.csv")


day <- substr(Tweets$tweet_created, 0, 10)
Tweets$day <- day(ymd(day))

day <- gsub("/","-", StockPrices$Date)
StockPrices$day <- day(mdy(day))

#function that gets the airline, and day and then returns the row that it corresponds to in stockPrices
mapper <- function(airline, day){
  row <- StockPrices[(StockPrices$Airline == airline) & (StockPrices$day == day), c(2, 4:9)]
  if(nrow(row) == 0) {
    return(rep(NA, 7))
  }else {
    return(row)
  }
}

#set up empty rows for this
Tweets[,names(StockPrices)[c(2, 4:9)]] <- NA

#i hate this its so inefficient
for(i in 1:nrow(Tweets)) {
  Tweets[i,17:23] = mapper(as.character(Tweets$airline[i]), Tweets$day[i])
}

write.csv(Tweets, file = "Tweets_stocks.csv", row.names = FALSE)


