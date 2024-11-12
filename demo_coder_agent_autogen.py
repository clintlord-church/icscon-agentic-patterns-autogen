from autogen import AssistantAgent, UserProxyAgent
from autogen.coding import DockerCommandLineCodeExecutor
import llm_configs, os

# "the code execution is successful and"
system_message = AssistantAgent.DEFAULT_SYSTEM_MESSAGE + " If the code execution is successful, do not write any new code, just respond with the word 'terminate'.  Don't use any external sources that require an API key or subscription access."
# Create an assistant agent that writes python code in response to a another agent's message
code_writer = AssistantAgent("code_writer", system_message=system_message, description="Writes python code", llm_config=llm_configs.azure_gpt4o_mini_llm_config)


# set the temp_dir to the current script directory
root_dir = os.path.dirname(os.path.realpath(__file__))
temp_dir_name = f"{root_dir}/working_dir"

docker_executor = DockerCommandLineCodeExecutor(
    timeout=60,  # Timeout for each code execution in seconds.
    work_dir=temp_dir_name,  # Use the temporary directory to store the code files.
    image="python:3-bookworm",  # Use the Python 3 Docker image.
)

user_proxy = UserProxyAgent(
    "user_proxy", 
    code_execution_config={ "executor": docker_executor }, 
    is_termination_msg=lambda msg: msg.get("content") and "terminate" in msg["content"].lower(),
    human_input_mode="TERMINATE"
)

result = user_proxy.initiate_chat(
    code_writer, 
    message="Download the video located at https://www.youtube.com/watch?v=xvFZjo5PgG0",
    # message="Find me the current stock price for Apple",
    # message="Create a file that contains the first 10000 prime numbers",
    max_turns=100)
