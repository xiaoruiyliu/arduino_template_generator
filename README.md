# Arduino Code Template Generator

## Frontend

Before you start, make sure you [have `node.js` installed](https://nodejs.org/en/download), then in the terminal under the main directory, run:
```
npm install
```

To start the frontend webpage, in the terminal under the main directory, run:
```
npm start
```
This should automatically open up a webpage. You can also start the webpage by using the url `http://localhost:3000/` in your browser.

## Backend

Before you start, make sure you install the following dependencies by running:
```
pip3 install flask
pip3 install flask_cors
```
> feel free to add the Template.py dependencies here as well for the final version of the Readme :)

In a terminal *separated from the one the frontend program is running on*, run:
```
python server.py
```

Note that the two program should be running at the same time for them to communicate.
They should both be able to automatically update any changes made to the code, however, when editting the backend code, the backend server will terminate on syntax error.
So make sure both the frontend and backend program are running before testing it out!