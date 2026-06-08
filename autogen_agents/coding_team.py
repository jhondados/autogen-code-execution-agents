"""AutoGen v0.4 coding agent team."""
import autogen
from autogen.coding import DockerCommandLineCodeExecutor

config_list = [{"model": "gemini-1.5-pro", "api_type": "google"}]
llm_config = {"config_list": config_list, "temperature": 0.1}

executor = DockerCommandLineCodeExecutor(image="python:3.11-slim", timeout=120,
    work_dir="/tmp/autogen_workspace")

def create_coding_team():
    planner = autogen.AssistantAgent("Planner", llm_config=llm_config,
        system_message="You plan data analysis tasks. Break into clear coding steps.")
    coder = autogen.AssistantAgent("Coder", llm_config=llm_config,
        system_message="You write clean, efficient Python code. Always add error handling.")
    executor_agent = autogen.UserProxyAgent("Executor", code_execution_config={"executor": executor},
        human_input_mode="NEVER", max_consecutive_auto_reply=10)
    critic = autogen.AssistantAgent("Critic", llm_config=llm_config,
        system_message="You review code for bugs, efficiency and best practices.")
    return autogen.GroupChat(agents=[planner, coder, executor_agent, critic],
        messages=[], max_round=20, speaker_selection_method="round_robin")
