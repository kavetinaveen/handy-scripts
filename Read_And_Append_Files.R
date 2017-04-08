############# How to read and append required files from too many files #############
library(readr) # Install readr package, if you don't have it....
path_to_directory <- c("/Users/nkaveti/Downloads/samplef/")
setwd(path_to_directory)

strt <- Sys.time()
FetchRequiredColumns <- function(path_to_directory){
  all_files <- list.files(path_to_directory)
  main_file <- c()
  for(i in all_files){
    cat(i, "\n")
    dat <- read_csv(i)
    main_file <- rbind(main_file, dat[, c("ID", "EmailId")])
  }
  main_file <- as.data.frame(main_file)
  write.csv(main_file, "main_file.csv", row.names = FALSE)
}
cat("Time Taken: ", Sys.time() - strt)