How to Run the Application
=======
1. Clone the github link into your folder task or
   paste this command on the terminal __git clone https://github.com/MuhalimHidayat/db_selaawi.git___
2. run __cd db_selaawi__ (depend on folder that you get after clone or download as a zip) on terminal
3. create python virtual environment __python3 -m venv .venv__ inside **db_selaawi folder
4. Activate the virtual environment __.venv/bin/activate__
5. run __pip -r install requirements.txt__
6. run __cd app__
7. run __npm install__ inside the app directory(cd app/ first)
8. run __cd ..__ for back to previous folder
9. run the application using __flask run__ 

Activate tailwind server for optimize styling on this website
1. run __cd app__ (if it's not already in the app folder)
2. run __npx tailwindcss -i ./static/src/input.css -o ./static/dist/css/output.css --watch__
