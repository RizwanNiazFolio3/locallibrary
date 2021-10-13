### Basic circleci instalation
A new folder called .circleci was added to the root of the project, this folder contains the config.yml file which tells circleci how to configure and run tests on our project.

The steps taken to configure circleci were as follows:
Logging in to the circleci website using your github id will display all of your repositories.
![HomePage](https://user-images.githubusercontent.com/85993939/136358611-b161e85e-1778-4e15-bb70-6374e36b2e47.JPG)

simply click on the repository you need to configure integration testing for.

A modal window should pop up, asking you to add a config.yml file to the project. select the first option that asks you use a template to make the config.yml file and press let's go

Select the kind of template you want to add to the project. In our case, we chose python
![SelectSampleConfig](https://user-images.githubusercontent.com/85993939/136359408-efc8b7f7-e7e7-467a-8bdb-cb8d53973fc3.JPG)

A template config.yml file for python should be displayed. Each projects config.yml needs to be configured based on the exact specifications of the project, in our case, we replaced the config.yml with [this code](https://github.com/RizwanNiazFolio3/locallibrary/blob/eed49e695f6affe124ab2957477999bacc88f848/.circleci/config.yml)

After that, clicking on commit and run creates a new branch on the project using the main branch as a base. We can then create a pull request to merge these changes into main.

All future PRs will then run the tests of the branch that is being merged into the base branch.

### If the config.yml file already exists:
Simply create a new branch, containing the .circlci folder as shown here
![folder](https://user-images.githubusercontent.com/85993939/136382720-6aee6056-f3ca-4992-934d-8a58c568adb9.JPG)
This folder should simply contain the config.yml file needed to run circleci
![configYML](https://user-images.githubusercontent.com/85993939/136382754-7d5c11ee-ee70-4ce8-9e95-a33fafe17041.JPG)

push this branch to the origin remote and then go to the circleci website and login with github
You should see a list of all of your repositories.
Click on the repository you want to add continuous integration to and you should be shown a modal window like this
![CirclCItest](https://user-images.githubusercontent.com/85993939/136383360-9d1c92b0-97c4-4ccd-8a10-96ae8f28ec04.JPG)

Choose the second option, if you have not merged the branch to main, you may need to select a different branch in the textbox shown.

Simply clicking on let's go should install circle ci to the repo.
