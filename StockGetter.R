
#install.packages("quantmod")
#install.packages("lubridate")
library(quantmod)
library(lubridate)


source <- "yahoo"

#airline <- "Yahoo"
#stock_symbol <- "YHOO"
#start <- "2005-01-01"
#end <- "2006-01-01"

#returns the data frame of stock information
stock_grabber <- function(airline, stock_symbol, start, end) {
  stockdf <- as.data.frame(getSymbols(stock_symbol, src=source, from = start, to = end, env = NULL))
  
  stockdf$date <- ymd(row.names(stockdf))
  stockdf$symbol <- rep(stock_symbol, nrow(stockdf))
  stockdf$airline <- rep(airline, nrow(stockdf))
  names(stockdf) <- c("Open", "High", "Low", "Close", "Volume", "Adj Close", "Date", "Stock Symbol", "Airline")
  stockdf <- stockdf[,c("Airline","Stock Symbol","Date", "Open", "High", "Low", "Close", "Volume", "Adj Close")]
}

csv_name <- cat(airline, "Stocks.csv", sep="")
write.csv(stockdf, file = csv_name, row.names = FALSE)

