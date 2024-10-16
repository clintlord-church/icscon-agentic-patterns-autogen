# Setup

## API Keys

1. Create a new file in the root directory called `.env` that looks like .env-example  
2. Fill in the values for the API keys in the `.env` file  

 NOTE:  
 - You don't need to have keys for Fireworks.ai, Anthropic or Google if you don't use those models.

 ## Installing modules

 This project depends on pyenv and pipenv.  To install the dependencies, run the following commands:

    pipenv install --python=$(pyenv which python)