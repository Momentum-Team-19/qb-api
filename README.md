# QuestionBox API

Documentation for endpoints in the QuestionBox API is available at https://questionbox-api.herokuapp.com/docs/

## What you can use this API to do

- Register a new user
- Logging in and out with token-based authentication
- Create a new question if you are logged in
- Post an answer to a question if you are logged in
- Get a list of all questions.
- Get a single question with all its answers.
- Get a list of all the questions you have posted, if you are logged in.
- Get a list of all the answers you have posted, if you are logged in.
- Mark an answer as accepted if you are the original author of the question
- Delete a question if you are its original author, whether answered or unanswered. If it is deleted, all associated answers will also be deleted.
- Authenticated users can bookmark or save a question or answer they like.
- Get a list of all your bookmarks if you are logged in.
- Search for keywords in the database by supplying a search term. The search term will be matched against the question title and body.
