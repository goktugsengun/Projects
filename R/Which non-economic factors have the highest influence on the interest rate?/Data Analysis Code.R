#library
library(tidyverse)


# import data. (I cannot upload the data to github since it is 200 MB.)

data <- read.csv("/Users/goktugsengun/Desktop/Storytelling in Finance/The Project/Data_Seminar_2022/FMFM2019_seminar.csv")
data <- as_tibble(data)

# values that are used instead of NA
#sum(is.na(data[,c(3,4,5,6,36)]))

#1#"0"  where?: c(3,4,5,6,36)
data[,c(3:6,36)][data[,c(3:6,36)] == 0] <- NA
#sum(is.na(data[,c(3:6,36)]))

#2# "9999" where?: c(4,7,10,13)
data[,c(4,7,10,13)][data[,c(4,7,10,13)] == 9999] <- NA
#sum(is.na(data[,c(4,7,10,13)]))

#3# 999999  where?: c(8,9,12,54)
data[,c(8,9,12,54)][data[,c(8,9,12,54)] == 999999] <- NA
#sum(is.na(data[,c(8,9,12,54)]))

#4# 999999999 where?: c(11,14,47,57)
data[,c(11,14,47,57)][data[,c(11,14,47,57)] == 999999999] <- NA
#sum(is.na(data[,c(11,14,47,57)]))

#5# 9 where?: c(15,18:35,37,38,40,41,43,48:52,56)
data[,c(15,18:35,37,38,40,41,43,48:52,56)][data[,c(15,18:35,37,38,40,41,43,48:52,56)] == 9] <- NA
#sum(is.na(data[,c(15,18:35,37,38,40,41,43,48:52,56)]))

#6# 99 where?: c(17,46,51:53)
data[,c(17,46,51:53)][data[,c(17,46,51:53)] == 99] <- NA
#sum(is.na(data[,c(17,46,51:53)]))

#7# 7 where?: c(19:23,25:29)
data[,c(19:23,25:29)][data[,c(19:23,25:29)] == 7] <- NA
#sum(is.na(data[,c(19:23,25:29)]))

#8# 6 where?: c(19:23,25:29,50)
data[,c(19:23,25:29,50)][data[,c(19:23,25:29,50)] == 6] <- NA
#sum(is.na(data[,c(19:23,25:29,50)]))

#9# 4 where?: c(24,30:32,39)
data[,c(24,30:32,39)][data[,c(24,30:32,39)] == 4] <- NA
#sum(is.na(data[,c(24,30:32,39)]))

#10# 3 where?: c(24,30:32)
data[,c(24,30:32)][data[,c(24,30:32)] == 3] <- NA
#sum(is.na(data[,c(24,30:32)]))

#11# 8 where?: c(25:29)
data[,c(25:29)][data[,c(25:29)] == 8] <- NA
#sum(is.na(data[,c(25:29)]))

#12# 5 where?: c(30,32,56)
data[,c(30,32,56)][data[,c(30,32,56)] == 5] <- NA
#sum(is.na(data[,c(30,32,56)]))

#13# 999 where?: c(42,44,55)
data[,c(42,44,55)][data[,c(42,44,55)] == 999] <- NA
#sum(is.na(data[,c(42,44,55)]))

# number of NA
sum(is.na(data))

na_rows <- apply(is.na(data),1,sum)/ncol(data)
plot(na_rows,type="h")

data <- data[-which.max(na_rows),]

#after converting values into NA. I need to drop rows where interest rate is NA, since it is related to our research question:
data <- data %>% drop_na(Interest.Rate.at.Origination)


#missing values
missing_vals <- as.matrix(data %>% is.na %>% colSums)
missing_vals_rel <- round(100*missing_vals/nrow(data),2)

#unique values
unique_vals <- t(as.matrix(data %>% summarise_all(n_distinct)))
unique_vals_rel <-  round(100*unique_vals/nrow(data),2)
##############
data_summary <- data.frame(missing_vals, missing_vals_rel, unique_vals, unique_vals_rel)
colnames(data_summary) <- c("NAs", "NAs_rel", "Unique", "Unique_rel")
data_summary

one_unique <- rownames(data_summary)[which(data_summary$Unique==1)]
full_NA <- rownames(data_summary)[which(data_summary$NAs_rel==100)] 
high_NA <- rownames(data_summary)[which(data_summary$NAs_rel>99.9&data_summary$NAs_rel<100)] 

col_del_ind <- match(unique(c(one_unique,full_NA,high_NA)),colnames(data)) # unique, because we can have some double counts
data <- data[,-col_del_ind]

dim(data)

########################
#select variables that might be related to our model: ( Q2 )

data <- data %>% select(c("Interest.Rate.at.Origination",  #y
                          "Number.of.Borrowers", #1   Borrowers info
                          "Borrower.Race1",
                          "Borrower.Ethnicity",
                          "Co.Borrower.Race1",        
                          "Co.Borrower.Ethnicity",
                          "Borrower.Gender",
                          "Co.Borrower.Gender",
                          "Age.of.Borrower",
                          "Age.of.Co.Borrower",              
                          "Borrower.Age.62.or.older",
                          "Co.Borrower.Age.62.or.older",
                          "US.Postal.State.Code", #2   Geographical info
                          "Metropolitan.Statistical.Area..MSA..Code",
                          "Rural.Census.Tract",              
                          "Persistent.Poverty.County",
                          "Area.of.Concentrated.Poverty",
                          "High.Opportunity.Area",
                          "Qualified.Opportunity.Zone..QOZ.",
                          "Purpose.of.Loan",    #3 Loan info
                          "Application.Channel",
                          "Occupancy.Code", #4   property type
                          "Property.Type"))
                  
plot_data_column(data, data$Number.of.Borrowers, data$Interest.Rate.at.Origination)

data$Interest.Rate.at.Origination

plot_data_column <- function (data, column, target) {
  if(is.factor(data[[target]])){
    if(is.numeric(data[[column]])){
      plotlimbox <- quantile(data[[column]],c(0.1,0.9),na.rm=TRUE) 
      ggplot(data, aes_string(x=target, y=column)) +
        geom_boxplot(outlier.shape = NA) +
        scale_y_continuous(limits = plotlimbox) +
        theme(legend.position = "none")
    }else{
      ggplot(data,aes_string(x=column,fill=target)) +
        geom_bar(position="fill") +
        theme(legend.position = "none")
    }
  }else{
    if(is.numeric(data[[column]])){
      plotlimscalex <- ifelse(min(data[[column]])==0,quantile(data[[column]],c(0,0.9999),na.rm=TRUE),quantile(data[[column]],c(0.0001,0.9999),na.rm=TRUE)) # as we have often data which starts with 0 and has a lot of 0's
      plotlimscaley <- ifelse(min(data[[target]])==0,quantile(data[[target]],c(0,0.9999),na.rm=TRUE),quantile(data[[target]],c(0.0001,0.9999),na.rm=TRUE))
      ggplot(data,aes_string(x=column,y=target)) +
        geom_point() +
        scale_y_continuous(limits = plotlimscaley) +
        scale_x_continuous(limits = plotlimscalex) +
        theme(legend.position = "none")
    }else{
      plotlimbox <- quantile(data[[target]],c(0.1,0.9),na.rm=TRUE) 
      ggplot(data, aes_string(x=column, y=target)) +
        geom_boxplot(outlier.shape = NA) +
        scale_y_continuous(limits = plotlimbox) +
        theme(legend.position = "none")
    }
  }
}

desc(data$)















                  
                  
                  
unique(data$Occupancy.Code)
#write.csv(data,"/Users/goktugsengun/Desktop/Storytelling in Finance/The Project/Data_Seminar_2022/cleandata.csv", row.names = FALSE)


#cleandata <- read.csv("/Users/goktugsengun/Desktop/Storytelling in Finance/The Project/Data_Seminar_2022/cleandata.csv")
#cleandata <- as_tibble(cleandata)
#dim(cleandata)


library(DescTools)

Desc(data$Interest.Rate.at.Origination)


colnames(data)

################ BORROWER INFO#############
data$Borrower.Race1 <- as_factor(data$Borrower.Race1)
data$Co.Borrower.Race1 <- as_factor(data$Co.Borrower.Race1)

Desc(Interest.Rate.at.Origination ~ Borrower.Race1, data)
Desc(Interest.Rate.at.Origination ~ Co.Borrower.Race1, data)
#their differences are negligible. And we think borrower 1 is more important, so we are it as our variable.
#interest rate is highest for black people and lower for Asian people.









data[, c("Borrower.Race1", "Co.Borrower.Race1")]


data$Borrower.Race1== data$Co.Borrower.Race1



Desc(data$Co.Borrower.Race1)


class(data$Borrower.Race1)

unique(data$Borrower.Race2)








