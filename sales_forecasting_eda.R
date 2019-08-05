# Loading required libraries
load_packages <- function(packages_list){
  for(i in packages_list){
    if(i %in% installed.packages()){
      library(eval(i), character.only = TRUE)
      print(paste0("Loaded installed library: ", i))
    }else{
      install.packages(i)
      library(i, character.only = TRUE)
      print(paste0("Installed and loaded library: ", i))
    }
  }
}

required_packages <- c("data.table", "ggplot2", "forecast", "infotheo", "ggloop", "gridExtra")
load_packages(required_packages)

# Generate data
generate_data <- function(){
  seq_dates <- seq.Date(as.Date("2016-01-01"), as.Date("2019-04-01"), by = "month")
  seq_dates <- as.numeric(paste0(year(seq_dates), ifelse(nchar(month(seq_dates)) == 1, paste0(0, month(seq_dates)), month(seq_dates))))
  results <- data.table(yrmo = seq_dates, y = round(rnorm(length(seq_dates), mean = 100, sd = 30), 2))
  nVar <- 200
  for(i in 1:nVar){
    results[[paste0("X", i)]] <- round(rnorm(length(seq_dates), mean = runif(1, min = 10, max = 100), sd = runif(1, min = 5, max = 50)), 2)
  }
  return(results)
}

# Compute mutual information
compute_mi <- function(df, xVars, x_diff = FALSE, y_diff = TRUE){
  mi_with_y <- data.table()
  for(i in xVars){
    if(x_diff){
      X <- diff(df[[i]])
    }else{
      X <- df[[i]][-1]
    }
    if(y_diff){
      Y <- diff(df[[dependent_var]])
    }
    if(length(unique(df[[i]])) > 10){
      X_disc <- cut(X, breaks = 10)
    }else{
      X_disc <- X
    }
    if(length(unique(df[[dependent_var]])) > 10){
      Y_disc <- cut(Y, breaks = 10)
    }else{
      Y_disc <- Y
    }
    mi_with_y <- rbind(mi_with_y, data.table(x = i, y = dependent_var, mi = mutinformation(X_disc, Y_disc), correlation = cor(X, Y)))
  }
  mi_with_y <- mi_with_y[order(-mi)]
  return(mi_with_y)
}

# Generate correlation plots
get_correlation_plots <- function(df, mi_with_y, top_k = 10){
  g <- list()
  for(i in 1:10){
    X <- mi_with_y$x[i]
    g[[i]] <- ggplot(data = df) + geom_point(aes_string(x = df[[X]], y = df[[dependent_var]])) + ggtitle(paste0("Correlation between ", dependent_var, " and ", X)) + xlab(X) + ylab(dependent_var)
  }
  out <- grid.arrange(g[[1]], g[[2]], g[[3]], g[[4]], g[[5]], g[[6]], g[[7]], g[[8]], g[[9]], g[[10]], ncol = 2)
  return(out)
}

# Fittng ARIMA model
fit_arima <- function(df, y, train_end, xreg = NULL){
  df_train <- df[yrmo <= train_end]
  df_test <- df[yrmo > train_end]
  start_year <- as.numeric(substr(min(df_train$yrmo), 1, 4))
  start_month <- as.numeric(substr(min(df_train$yrmo), 5, 6))
  y_ts <- ts(df_train[[y]], frequency = 12, start = c(start_year, start_month))
  y_ts_diff <- diff(y_ts)
  if(!is.null(xreg)){
    xreg_train_df <- sapply(df_train[, xreg, with = FALSE], diff)
    xreg_test_df <- sapply(df_test[, xreg, with = FALSE], diff)
    fit <- auto.arima(y_ts_diff, xreg = xreg_train_df)
    test_forecast <- forecast(fit, h = nrow(df_test), xreg = xreg_test_df)
  }else{
    fit <- auto.arima(y_ts_diff)
    test_forecast <- forecast(fit, h = nrow(df_test))
  }
  train_forecast <- cumsum(c(y_ts[1], fit$fitted))
  test_forecast <- cumsum(c(tail(y_ts, 1), test_forecast$mean))[-1]
  results <- data.table(yrmo = df$yrmo, Actuals =  df$y, Forecast = c(train_forecast, test_forecast))
  results$label <- "train"
  results[yrmo > train_end, "label"] <- "test"
  return(results)
}

# Back-testing with ARIMA
back_testing <- function(df, y, train_end_start, test_end, xreg = NULL){
  # max_yr_mo <- max(df$yrmo)
  dates_list <- seq.Date(as.Date(paste0(train_end_start, "01"), "%Y%m%d"), as.Date(paste0(test_end, "01"), "%Y%m%d"), by = "month")
  dates_list <- as.numeric(paste0(year(dates_list),ifelse(nchar(month(dates_list)) == 1, paste0(0, month(dates_list)), month(dates_list))))
  results <- data.table()
  for(i in dates_list){
    if(!is.null(xreg)){
      res <- fit_arima(df, y, i, xreg = xreg)
    }else{
      res <- fit_arima(df, y, i)
    }
    res$train_end <- i
    res$window <- -1
    res[label == "test", "window"] <- 1:nrow(res[label == "test"])
    results <- rbind(results, res)
  }
  return(results)
}

# Main
df <- generate_data()
time_var <- "yrmo"
dependent_var <- "y"
df <- df[order(yrmo)]
xVars <- setdiff(colnames(df), c(time_var, dependent_var))
mi_with_y <- compute_mi(df, xVars)
print(get_correlation_plots(df, mi_with_y))

results <- back_testing(df, dependent_var, 201804, 201812, xreg = c("X1", "X2", "X3", "X4", "X5"))

ggplot() + geom_histogram(aes(x = diff(df$y)), bins = 15) + ggtitle("Distribution of Change in Demand Sales") + xlab("Change in demand sales") + ylab("Frequency")





