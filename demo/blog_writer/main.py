import json
from argparse import ArgumentParser

from hydra.utils import instantiate
from omegaconf import OmegaConf
from sherpa_ai.agents import QAAgent, UserAgent
from sherpa_ai.events import EventType

from outliner import Outliner


def get_qa_agent_from_config_file(
    config_path: str,
) -> QAAgent:
    """
    Create a QAAgent from a config file.

    Args:
        config_path: Path to the config file

    Returns:
        QAAgent: A QAAgent instance
    """

    config = OmegaConf.load(config_path)

    agent_config = instantiate(config.agent_config)
    qa_agent: QAAgent = instantiate(config.qa_agent, agent_config=agent_config)

    return qa_agent



def get_user_agent_from_config_file(
    config_path: str,
) -> UserAgent:
    """
    Create a UserAgent from a config file.

    Args:
        config_path: Path to the config file

    Returns:
        UserAgent: A UserAgent instance
    """

    config = OmegaConf.load(config_path)

<<<<<<< HEAD
=======
    agent_config = instantiate(config.agent_config)
>>>>>>> 0795538cbd9b08b3bc4f2342a59b2baa1e712017
    user: UserAgent = instantiate(config.user)

    return user



if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--config", type=str, default="agent_config.yaml")
    parser.add_argument("--transcript", type=str, default="transcript.txt")
    args = parser.parse_args()

    writer_agent = get_qa_agent_from_config_file(args.config)
    reviewer_agent = get_user_agent_from_config_file(args.config)

    outliner = Outliner(args.transcript)
    blueprint = outliner.full_transcript2outline_json(verbose=True)
    if blueprint.startswith("```"):
        # The first and last lines are code block delimiters; remove them
        lines = blueprint.split("\n")[1:-1]
        pure_json_str = "\n".join(lines)
    else:
        pure_json_str = blueprint

    with open("blueprint.json", "w") as f:
        f.write(pure_json_str)

<<<<<<< HEAD
=======
    #with open("blueprint.json", "r") as f:
    #    pure_json_str = f.read()

>>>>>>> 0795538cbd9b08b3bc4f2342a59b2baa1e712017
    parsed_json = json.loads(pure_json_str)

    blog = ""
    thesis = parsed_json.get("Thesis Statement", "")
    blog += f"# Introduction\n{thesis}\n"
    arguments = parsed_json.get("Supporting Arguments", [])
    for argument in arguments:
        blog += f"## {argument['Argument']}\n"
        evidences = argument.get("Evidence", [])
        for evidence in evidences:
            writer_agent.shared_memory.add(EventType.task, "human", evidence)
            result = writer_agent.run()

<<<<<<< HEAD
            reviewer_input = (
                "\n"
                "Please review the paragraph generated below. "
                "Type 'yes', 'y' or simply press Enter if everything looks good. "
                "Else provide feedback on how you would like the paragraph changed."
                "\n\n"
                + result
            )
            reviewer_agent.shared_memory.add(EventType.task, "human", reviewer_input)

            decision = reviewer_agent.run()
            decision_event = reviewer_agent.shared_memory.get_by_type(EventType.result)
            decision_content = decision_event[-1].content

            if decision_content == []:
                break

=======

            reviewer_input= "\n" + "Please review the paragraph generated below. Type 'yes', 'y' or simply press Enter \
                if everything looks good. Else provide feedback on how you would like the paragraph modified." \
                + "\n\n" + result
            reviewer_agent.shared_memory.add(EventType.task, "human", reviewer_input)

            decision = reviewer_agent.run()
            decision_event= reviewer_agent.shared_memory.get_by_type(EventType.result)
            decision_content=decision_event[-1].content

            if decision_content == []:
                break
            #
>>>>>>> 0795538cbd9b08b3bc4f2342a59b2baa1e712017
            if decision_content.lower() in ["yes", "y", ""]:
                pass
            else:
                writer_agent.shared_memory.add(EventType.task, "human", decision_content)
                result = writer_agent.run()
<<<<<<< HEAD

=======
            # writer_agent.belief = Belief()
>>>>>>> 0795538cbd9b08b3bc4f2342a59b2baa1e712017
            blog += f"{result}\n"

    with open("blog.md", "w") as f:
        f.write(blog)

    print("\nBlog generated successfully!\n")
