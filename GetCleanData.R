
#initiate the library to getData
library(quantmod)

findDetails<- function(companyname){

  getSymbols(companyname,src = 'yahoo')
  if(substr(companyname,start = 1,stop = 1)=="^"){
    companyname=substr(companyname,start = 2,stop = nchar(companyname))
  }
  
  #Get the data as a dataframe and and a Date column to it
  
  df<-as.data.frame(coredata(get(companyname)))
  Date<-index(get(companyname))
  df<-cbind(Date,df)
  
  
  #find indexes of NA data
  myList = c()
  for(i in 1:nrow(df)){
    if(is.na(df[i,2])){
      myList<-c(myList,i)
    }
  }
  
  #delete NA rows
  if(!is.null(myList)){
    df<-df[-myList,]
  } 
  companyname<-gsub('.','_',x = companyname,fixed = TRUE)
   #output the proper csv file
   #the file is written to "./Data/Raw"
  folder <- paste(paste("./Data/",companyname,sep=""),"/",sep="")
  fileName <-"Raw.csv"
  dir.create(folder, showWarnings = FALSE)
  write.csv(paste(folder,fileName,sep = ""),x=df,row.names = F,eol = "\n")
  
  print(companyname )
  #print(length(myList))

}
#retrieve arguments from command line

args<- commandArgs(trailingOnly=TRUE)
if(length(args)== 0){
  args<-as.vector(read.csv("Companies.txt")[,1])
}

dir.create("./Data/", showWarnings = FALSE)

for(i in args){
  # print(i)
  findDetails(i)
  # Sys.sleep(1)
  # print(i)
}
print("Completed")
