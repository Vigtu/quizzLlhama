from crewai import Agent, Task, Crew, Process
from crewai_tools import CSVSearchTool
import os
#import sys

#sys.path.append('.venv\Lib\site-packages\crewai_tools')

os.environ["OPENAI_API_BASE"] = 'https://api.groq.com/openai/v1'
os.environ["OPENAI_MODEL_NAME"] ='llama3-70b-8192' 
os.environ["OPENAI_API_KEY"] ='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'

search_tool = CSVSearchTool(filepath='Dataset\DataScienceQA.csv')

reader = Agent(
    role = "questions and answers reader",
    goal = "accurately read the questions and answers data. and provide this knowledge to 'teacher' agent",
    backstory = "You are an expert in reading and interpreting question-and-answer data, was developed to \
                support educational environments. Your primary role is to accurately extract and provide knowledge \
                to 'Professor Sage', ensuring precise and relevant information is shared with students. This \
                collaboration enhances the learning experience by making complex information accessible and \
                understandable.",
    verbose = True,
    allow_delegation = False,
    tools = [search_tool]
)

teacher = Agent(
    role = "data science teacher",
    goal = "educate students effectively using precise and relevant data insights provided by 'reader' agent",
    backstory = "Professor Sage is a dedicated data science teacher with a mission to make complex concepts \
                understandable for students. Working closely with 'reader' agent, the questions and answers reader, \
                Professor Sage leverages the accurate and contextually relevant information provided to enhance \
                the educational experience. This partnership ensures that students receive clear and precise knowledge, \
                fostering a deeper understanding of data science.",
    verbose = True,
    allow_delegation = True
)

def main_query(query):

    reader_task = Task(
        description = f"Find the answer to the question: '{query}' in the CSV file.",
        agent = reader,
        expected_output = "The relevant answer to the query from the CSV file"
    )

    teach_task = Task(
        description = "Use the structured summary of questions and answers data provided by the 'reader' agent to educate students effectively.",
        agent = teacher,
        expected_output = "A clear and precise answer to the user's question"
    )

    crew = Crew(
        agents = [reader, teacher],
        tasks = [reader_task, teach_task],
        process = Process.sequential
    )

    output = crew.kickoff(inputs={'query:': query})
    return output

while True:
    ask_question = input("Ask a question about Data Science (or type 'exit' to quit): ")
    if ask_question.lower() == 'exit':
        break
    answer = main_query(ask_question)
    print("Teacher's Answer:", answer)



