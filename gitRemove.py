import os

git = "git rm --cached -r "
for i in os.listdir("./Data/"):
    # os.system(git +".\Data\\"+i+"\Data.csv")
    # os.system(git +".\Data\\"+i+"\Raw.csv")
    # os.system(git +".\Data\\"+i+"\PredictedValues.csv")
    os.system(git +".\Data\\"+i+"\data.meta")
    os.system(git +".\Data\\"+i+"\GBTregressor.p")

# git rm --cached -r <file>
