# cs145-twitter-airlines

Team Should Have Been Kobe Shots

Members:
- Roland Zeng
- Brendan Sio
- Menglin Ruan
- Simon Hua
- Brandon Ly

Most of the theory, implementation, and analysis details of our project is in our submitted report. This README.md
merely details how to use the code.

Before running the sentiment predictor (located in 'cs145-twitter-airlines/TweetSentModel/tweetsModel.py'):
* Before running the code, please check that the Kaggle tweets training data path is correct. This can be found on line
  186.
* You can test our sentiment predictor back onto the Kaggle training data by setting 'test_on_training_data' to 1. This
  can be found on line 190.
* If testing it out on other data, please be sure that 'file_dir_to_read' and 'file_to_read' are properly set to the
  file and directory you want to test our predictor on.
* If testing it out on custom data sheets, please be sure that the .csv files follow the same format as the testing
  data we used (located in 'cs145-twitter-airlines/tweets_stocks_testing.csv')

Before running the stock price predictor:
* Load up any IDE that is able to run R
* Open the Insighted_updated.pdf and copy and paste the code into the IDE to run OR run the R Markdown file (.rmd)
   -Make sure you change the name of the csv file to the csv file you want to run on
* The R code will generate the predicted stock prices
