How to Run the Application
=======
1. Clone the github link into your folder task or
   paste this command on the terminal __git clone https://github.com/MuhalimHidayat/db_selaawi.git___
2. create python virtual environment __python3 -m venv .venv__
3. Activate the virtual environment __.venv/bin/activate__
4. run __pip -r install requirements.txt__
5. run __flask db init__ on root directory
6. run __flask db migrate -m "run apps"__ on root directory
7. run __flask db upgrade__ on root directory
8. run __npm install__ inside the app directory(cd app/ first)
9. run the application using __flask run__ on the terminal
