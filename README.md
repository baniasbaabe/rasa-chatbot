# Restaurant Chatbot with Rasa

## How to run

1. Clone the project
2. Create a virtual environment
`$ python -m venv venv`
3. Activate virtual environment
`$ venv\Scripts\activate`
4. Install packages
`$ pip install requirements.txt`
5. If there are no models in `/models` then
`$ rasa train`
6. Run the actions server
`$ rasa run actions`
7. Open a new terminal, go to the same directory, do Step 3, and run the rasa shell
`$ rasa shell`