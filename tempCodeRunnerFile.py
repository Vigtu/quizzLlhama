import streamlit as st
import os
import csv
import logging
from crewai import Agent, Task, Crew, Process
from crewai_tools import BaseTool

# Initialize logging
logging.basicConfig(level=logging.DEBUG)

# Set the environment
os.environ["OPENAI_API_BASE"] = 'https://api.groq.com/openai/v1'
os.environ["OPENAI_MODEL_NAME"] = 'llama3-70b-8192'
os.environ["OPENAI_API_KEY"] = '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'

class CSVSearchTool(BaseTool):
    name: str = "CSVSearchTool"
    description: str = "Search for answers in a CSV file. The name of the file is 'DataScienceQA' and the file path is 'DataScienceQA.csv'."

    def _run(self, search_query: str, file_path: str = './DataScienceQA.csv') -> str:
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if search_query.lower() in row['Question'].lower():
                        return row['Answer']
            return "No answer found for the query."
        except FileNotFoundError:
            return f"File not found: {file_path}"

csv_search_tool = CSVSearchTool()

reader = Agent(
    role="questions and answers reader",
    goal="Accurately read the questions and answers data and provide this knowledge to the 'teacher' agent. Be careful to not answer the whole .csv file when you are reading.",
    backstory="You are an expert in reading and interpreting question-and-answer data, developed to support educational environments. Your primary role is to accurately extract and provide knowledge to 'Professor Sage', ensuring precise and relevant information is shared with students. This collaboration enhances the learning experience by making complex information accessible and understandable.",
    verbose=True,
    allow_delegation=False,
    tools=[csv_search_tool]
)

teacher = Agent(
    role="teacher",
    goal="Educate students effectively using precise and relevant data insights provided by the 'reader' agent",
    backstory="Professor Sage is a dedicated teacher with a mission to make complex concepts understandable for students. Working closely with the 'reader' agent, the questions and answers reader, Professor Sage leverages the accurate and contextually relevant information provided to enhance the educational experience. This partnership ensures that students receive clear and precise knowledge, fostering a deeper understanding of data science.",
    verbose=True,
    allow_delegation=False
)

def main_query(query):
    reader_task = Task(
        description=f"Find the answer to the question: '{query}'. Be careful to not answer the whole .csv file when you are reading.",
        agent=reader,
        expected_output=f"Answer the question: {query}",
        tools=[csv_search_tool]
    )

    teach_task = Task(
        description=f"Use the structured summary of questions and answers data provided by the 'reader' agent to explain the question made in '{query}'.",
        agent=teacher,
        expected_input=reader_task.expected_output,
        expected_output="A clear and precise answer to the user's question."
    )

    crew = Crew(
        agents=[reader, teacher],
        tasks=[reader_task, teach_task],
        process=Process.sequential
    )

    output = crew.kickoff(inputs={'search_query': query})
    return output

def main():
    st.set_page_config(page_title="Data Science Teacher", page_icon=":book:")

    st.header("Data Science Teacher Response Generator")
    message = st.text_area("Ask a question about Data Science")

    if message:
        st.write("Generating the best response...")
        try:
            logging.debug("Calling main_query")
            result = main_query(message)
            logging.debug(f"Result: {result}")
            st.info(result)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            logging.error(f"Exception: {str(e)}")

if __name__ == '__main__':
    logging.debug("Starting app")
    main()
