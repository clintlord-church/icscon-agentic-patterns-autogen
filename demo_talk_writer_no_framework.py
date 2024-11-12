from lang_chain_models import Model
from ClintsCoolAgent import ClintsCoolAgent
import json, os

model = Model.AzureGPT4oMini

# ANSI escape codes for color
RED = "\033[31m"
RESET = "\033[0m"  # Resets the color to default

def log_and_print(log, text):
    print(text)
    log.write(text + "\n")

# create a talk planner
talk_planner_agent = ClintsCoolAgent(model, """
    You are an expert sacrament meeting talk planner for The Church of Jesus Christ of Latter-day Saints.
    You will only be given the topic of the talk and then you will create a talk outline.
    The talk outline should include atleast an introduction, three main points, and a conclusion, but can include more.
    Format the outline in a json array in which each description of the talk section is a string.
    No other content should be included in the response.  It should only be a RAW json array (with no additional markup) in this format:
    ["Description of the first section", "description of the second section", "description of the third section", "description of the fourth section"]
    """
)

# create a talk writer
talk_writer_agent = ClintsCoolAgent(model, """
    You are an expert sacrament meeting talk writer for The Church of Jesus Christ of Latter-day Saints.
    You will be given the topic of the talk, the content of talk that has been written so far, the title of the next section of the talk, the number of sections remaining after the current one, your prior draft of this section (if any) and feedback from the reviewer (if any).
    You should then create or refine the new talk section and then return the new talk section.
    The tone of the talk should be familiar, friendly and personal.  It should not sound like an essay or a book.  It should be specific and avoid vague generalities.  It should not repeat the same ideas or phrases from prior sections of the talk.
    You should not make any concluding remarks until the final section of the talk.
    The response should only contain the text for the new section of the talk and should NOT include any commentary about the new section or commentary about the feedback.
    Do not send back any of the content that had already been written before this new section.
    It should only contain the text for the new section of the talk.
    """
)

# create a talk reviewer
talk_reviewer_agent = ClintsCoolAgent(model, """
    You are an expert sacrament meeting talk reviewer for The Church of Jesus Christ of Latter-day Saints.
    You will be given the topic of the talk, the talk that has been written so far, the new section of the talk that has just been written, the number of sections remaining after the current one.
    You should then review the new section in context of what has already been writen and provide feedback on how the new section could be improved.
    Watch for things like clarity, doctrinal accuracy, and relevance to the topic.
    The tone of the talk should be familiar, friendly and personal.  It should not sound like an essay or a book. It should be specific and avoid vague generalities. It should not repeat the same ideas or phrases from prior sections of the talk. 
    The concluding remarks should only be included in the final section of the talk.
    Only respond with feedback for the new section, not the entire talk.
    """
)

title = "The Atonement of Jesus Christ"

# get the current script running directory
current_dir = os.path.dirname(os.path.realpath(__file__))

# if the talks directory doesn't exist, create it
if not os.path.exists("talks"):
    os.makedirs("talks")

log = open(f"talks/{title}-{model}.log", "w")
try:
    talk_no_review = []
    talk = []

    # Get the talk plan from the planner agent
    plan = talk_planner_agent.respond(title)
    list = json.loads(plan)

    log_and_print(log, f"{RED}**** Talk Plan ****{RESET}")
    log_and_print(log, "\n".join(list))
    log_and_print(log, "")

    # Loop through the sections of the talk and write and review each section
    for section in list:
        # Write the new section
        new_section = talk_writer_agent.respond(f"""
    TOPIC: {title}\n
    TALK_CONTENT: {"\n".join(talk)}\n
    NEXT_SECTION_TITLE: {section}\n
    NUMBER_OF_REMAINING_SECTIONS: {len(list) - list.index(section) - 1}\n
    PRIOR_DRAFT: None\n
    REVIEWER_FEEDBACK: None
    """)
        
        talk_no_review.append(new_section)

        log_and_print(log, f"{RED}**** New Section ****{RESET}")
        log_and_print(log, new_section)
        log_and_print(log, "")

        # Review the new section
        feedback = talk_reviewer_agent.respond(f"""
    TOPIC: {title}\n
    TALK_CONTENT: {"\n".join(talk)}\n
    NEW_SECTION: {new_section}
    NUMBER_OF_REMAINING_SECTIONS: {len(list) - list.index(section) - 1}\n
    """)
        
        log_and_print(log, f"{RED}**** Review/Feedback ****{RESET}")
        log_and_print(log, feedback)
        log_and_print(log, "")
        
        # Rewrite and refine the new section based on the feedback
        new_section = talk_writer_agent.respond(f"""
    TOPIC: {title}\n
    TALK_CONTENT: {"\n".join(talk)}\n
    NEXT_SECTION_TITLE: {section}\n
    NUMBER_OF_REMAINING_SECTIONS: {len(list) - list.index(section)}\n
    PRIOR_DRAFT: {new_section}\n
    REVIEWER_FEEDBACK: {feedback}
    """)

        log_and_print(log, f"{RED}**** Refined Section ****{RESET}")
        log_and_print(log, new_section)
        log_and_print(log, "")
        
        talk.append(new_section)

    #log.write("Final Zero Shot Token Count: " + str(talk_zero_shot_writer_agent.get_token_count()) + "\n")
    log_and_print(log, f"Final Planner Token Count: {str(talk_planner_agent.get_token_count())}")
    log_and_print(log, f"Final Writer Token Count: {str(talk_writer_agent.get_token_count())}")
    log_and_print(log, f"Final Reviewer Token Count: {str(talk_reviewer_agent.get_token_count())}")

    open(f"talks/{title}-{model}.txt", "w").write("\n".join(talk))
    open(f"talks/{title}-{model}-no_review.txt", "w").write("\n".join(talk_no_review))
    #open(f"talks/{title}-{model}-zero_shot.txt", "w").write(zero_shot)
finally:
    log.close()

