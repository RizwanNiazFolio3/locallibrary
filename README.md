# locallibrary
A locallibrary website made using the tutorials mentioned in the third week of the python training plan

How to run:
1. run pip install pipenv
2. in the root folder of the repository, (The one containing the Pipfile and Pipfile.lock files) run pipenv install
3. run pipenv shell to start the python virtual environment (All of the required dependancies should be installed because of the previous step)
5. create the database using py manage.py migrate
6. run server using py manage.py runserver
7. navigate to http://127.0.0.1:8000/ in your local web browser

edit - 2/7/2021:
The website was successfully deployed to Heroku on the following URL
https://tim-moose-37514.herokuapp.com/catalog/

two test users were also created to check the functionality:

Username: User1, Password: Strong_password
Username: User2, Password: Strong_password
User2 is in the librarian group and as such has more permissions than user 1:
The view pages for creating, updating, and deleting Authors and Books can be accessed by User2. Just go to the book list or author list pages to change them
