# QuizzLlhama

## Overview
QuizzLlhama is a Streamlit application that utilizes the CrewAI API to generate quiz questions based on given text inputs. This README provides instructions on how to set up the application on your local machine.

## Prerequisites
Before proceeding, ensure you have the following installed on your system:
- Python (version 3.10 or higher)
- pip (Python package installer)

## Installation Steps
### 1. Clone the Repository
Clone the project repository to your local machine using Git by running the following command in your terminal or command prompt:
git clone https://github.com/Vigtu/quizzLlhama.git


### 2. Navigate to Project Directory
Change your working directory to the project directory using the following command:
cd quizzLlhama


### 3. Install Dependencies
Install the required Python dependencies listed in the `requirements.txt` file using pip. Run the following command:
pip install -r requirements.txt


### 4. Set Up CrewAI API Key
To utilize the GROQ API within the application, ensure you have a CrewAI API key. Set your CrewAI API key as an environmental variable named `GROG_API_KEY` on your system.
https://groq.com/

Create a `.env` file in the project directory if it doesn't exist already. Add the following line to the `.env` file, replacing `sk-xxxxxxxxxxxxxxxxx` with your actual CrewAI API key:


## Running the Streamlit Application
Once you've completed the setup steps, you can run the Streamlit application using the following command:
streamlit run quizzLlhama.py

