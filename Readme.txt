URI
---
[HTTPS] https://github.com/faugh22k/AerialSurvey.git
[SSH] git@github.com:faugh22k/AerialSurvey.git


creating a new repository on the command line
---------------------------------------------
echo # AerialSurvey >> Readme.md
git init
git add Readme.md
git commit -m "first commit"
git remote add origin https://github.com/faugh22k/AerialSurvey.git
git push -u origin master


push an existing repository from the command line
-------------------------------------------------
git remote add origin https://github.com/faugh22k/AerialSurvey.git
git push -u origin master


to setup account's default identity
for committing to repository using Git Shell command line
---------------------------------------------------------
git config --global user.email "your@example.com"
git config --global user.name "Your Name"

* omit --global to set identity only in this repository