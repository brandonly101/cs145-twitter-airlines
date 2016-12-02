
#GOAL: merge all the twitter feeds into usable file

#------------------------------------------------------------

#function that gets the airline, and day and then returns the row that it corresponds to in stockPrices
#StockPrices is data frame
#return an array to put into the data frame
get_stock_info <- function(airline, date, stocks){
  row <- stocks[(stocks$Airline == airline) & (stocks$Date == date), c(2, 4:9)]
  if(nrow(row) == 0) {
    return(rep(NA, 7))
  }else {
    return(row)
  }
}

#------------------------------------------------------------

#OPERATES IN WORKING DIRECTORY
#airline is the official airline name (or what you want to call it)
#stock symbol has to match perfectly
#filename is the csv name
#RETURN: data frame with all the data aggregated

add_stocks <- function(airline, stock_symbol, filename) {
  
  csv_path <- paste(getwd(),"/", filename, sep = "")
  df <- read.csv(csv_path, stringsAsFactors = FALSE)
  
  #remove empty rows
  df <- df[(df$Date != ""),]
  
  #change date into usable form
  dates <- df$Date
  months <- substr(dates, 5, 7) #get the month
  days <- substr(dates, 9,10) #get the day
  years <- substr(dates, nchar(df$Date[1])-3, nchar(df$Date[1])) #get the year
  
  #convert months to numbers
  month_key <- c("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
  for(i in 1:12) {
    months[months == month_key[i]] <- i
  }
  
  #concatenate for YYYY-MM-DD and replace the date in the data frame
  df$Date <- paste(years, months, days, sep="-")
  df$Date <- ymd(df$Date)
  
  #find oldest and newest date to grab stocks
  start <- as.character(first(sort(df$Date)))
  end <- as.character(last(sort(df$Date)))
  
  stockdf <- stock_grabber(airline, stock_symbol, start, end)
  
  
  #MERGE STOCK INFO INTO TWITTER DATA FRAME
  
  #set up empty rows
  df[,names(stockdf)[c(2, 4:9)]] <- NA
  
  #replace all rows into the data frame
  for(i in 1:nrow(df)) {
    df[i,6:12] = get_stock_info(airline, df$Date[i], stockdf)
  }
  
  #add row with airline name
  df$Airline <- rep(airline, nrow(df))
  #reorder the rows
  reordered_names <- c(names(df)[13], names(df)[-c(3,4,13)], names(df)[c(3,4)])
  
  return(df[,reordered_names])
}

#------------------------------------------------------------

#SCRIPT TO GET ALL THE DATAFRAMES

files <- list.files(pattern="*.csv")  #all the files in this folder

#airline names corresponding to the files
airline_names <- c("American", "American", "Delta", "Delta", "Southwest", "Southwest", "United", "United", "US Airways", "US Airways", "Virgin America", "Virgin America")

#stock symbols according to files
stock_symbols <- c("AAL", "AAL", "DAL", "DAL", "LUV", "LUV", "UAL", "UAL", "AAL", "AAL", "VA", "VA")


df <- add_stocks(airline_names[1], stock_symbols[1], files[1])
for(i in 2:length(files)) {
  df <- rbind(df, add_stocks(airline_names[i], stock_symbols[i], files[i]))
}

write.csv(df, "tweets_stocks_testing.csv", row.names = FALSE)

