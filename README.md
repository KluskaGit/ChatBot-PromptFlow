<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
  </ol>
</details>


## About The Project


### Built With
* [Python](https://www.python.org/)
* [PromptFlow](https://microsoft.github.io/promptflow/)
* [Streamlit](https://streamlit.io/)

## Getting Started

### Prerequisites
* Python 3.8 or higher
* Azure OpenAI API key
* Azure OpenAI Base URL
* Model deployed in Azure AI Foundry (gpt-4.1-mini or o4-mini)

### Installation
1. Clone the repo
   ```sh
   git clone git@github.com:KluskaGit/ChatBot-PromptFlow.git
   ```
2. Install the required packages 
    * Using uv 
    ```sh
        uv sync
    ```
    * Using pip
    ```sh
        pip install -r requirements.txt
    ```
3. Set up environment variables
   * Create a `.env` file in the root directory of the project based ont the `.env_template` file.

## Usage
1. Activate the virtual environment
    ```sh
        source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
2. Run the Streamlit app
    ```sh
        streamlit run app.py
    ```
    or
    ```sh
        uv run streamlit run app.py
    ```