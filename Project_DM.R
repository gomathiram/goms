my_data <- read.csv('C:/Users/Girijesh/Downloads/VideoFinalData.csv')
my_data_2 <- as.data.frame(my_data)
my_data_3 <- na.omit(my_data_2)
cl_name<- c("category_id",   "views", "likes", "dislikes",  "comment_count", "std_trending_date",
"std_publish_time",  "trending_year", "trending_month","trending_day", 
"trending_week", "publish_year","publish_month", "publish_day", "publish_week", 
"publish_hour"  , "no_days" , "view_rate" , "count_tags",  "count_title", "channel_score")
my_data_1 <- my_data_3[cl_name]

#Structure 
str_dat <- str(my_data_1)


my_data_1$publish_month <- as.factor(my_data_1$publish_month)
my_data_1$trending_year <- as.factor(my_data_1$trending_year)
my_data_1$trending_month <- as.factor(my_data_1$trending_month)
my_data_1$publish_year <- as.factor(my_data_1$publish_year)
my_data_1$publish_year <- as.factor(my_data_1$publish_year)
my_data_1$dislikes <- as.numeric(my_data_1$dislikes)

# aMit code:


#Step Binning
Bin_trending_day <- cut(my_data_1$trending_day, breaks = c(1,8,16,24,32), labels = c("1st week","2nd week", "3rd Week", "4th Week"))
Bin_trending_day[is.na(Bin_trending_day)] <- "3rd Week"
Bin_publish_day <- cut(my_data_1$publish_day, breaks = c(1,9,16,23,31), labels = c("1st week","2nd week", "3rd Week", "4th Week"))
Bin_publish_day[is.na(Bin_publish_day)] <- "3rd Week"
Bin_Publish_hour <- cut(my_data_1$publish_hour, breaks = c(0, 4, 8, 12, 16, 20, 24), labels = c("0-4","4-8","8-12","12-16","16-20","20-24"))
Bin_Publish_hour[is.na(Bin_Publish_hour)] <- "4-8"

my_data_1$publish_hour <- Bin_publish_day
my_data_1$trending_day <- Bin_trending_day
my_data_1$publish_hour <- Bin_Publish_hour


str(my_data_1)



#Split Data
library(caTools)
sample <-  sample.split(my_data_1, SplitRatio = 2/3)
train_viral <-   subset(my_data_1, sample == TRUE )
train_viral_1 <- train_viral[ c( "no_days", "views", "likes", "dislikes",  "comment_count" , "count_tags",  "count_title", "channel_score")]
train_viral_2 <- as.data.frame(sapply(train_viral_1, as.numeric))

test_viral <- subset(my_data_1, sample == FALSE)
test_viral_1 <-test_viral[c("no_days", "views", "likes", "dislikes",  "comment_count" , "count_tags",  "count_title", "channel_score")]
test_viral_2 <- as.data.frame(sapply(test_viral_1, as.numeric))

  
#Hitogrram:
multi.hist(train_viral_2)

#Log transformation of predictor variables
train_viral_log <- as.data.frame(log(train_viral_2 +1))
#Sqrt based transformation
train_viral_sqrt <- as.data.frame(sqrt(train_viral_2))

#Test set log transformation
test_viral_log <- as.data.frame(log(test_viral_2 + 1))

#Summary
summary(train_viral_log)
summary(train_viral_sqrt)

#Log Histogram:{chose Log based data transformation}
multi.hist(train_viral_log)

#Sqrt hist. still has skewness
multi.hist(train_viral_sqrt)


#Shapiro Normality Test
normality <- sapply(train_viral_log[1:5000, ], shapiro.test)
model <-  lm(no_days ~., train_viral_log)



#Ensure the number are not represented in scientific notation.
options(scipen= 999)
  
#Summary model
summary(model)

pred_viral <- predict(model, test_viral_log)
pred_viral_sq <- as.data.frame(round(exp(pred_viral)))
data.frame("predicted" = pred_viral_sq,"actual"= test_viral_2$no_days)

#Residuals
residuals_viral <- pred_viral_sq- test_viral_2$no_days

#Accuracy (function not working)
accuracy(pred_viral_sq,test_viral_2$no_days)

