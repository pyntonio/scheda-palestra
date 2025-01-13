# PyGPT

# Web Application with FastAPI and OpenAI Integration  

This web application is built with **FastAPI** and integrates various modules leveraging **OpenAI's API** to provide functionalities such as virtual assistants, content generation, psychological support, business tools, and educational resources. The app exposes several APIs to interact with these features.

## Main Features  

The app provides a set of tools, each accessible via API. The main functionalities include:  

- **Personal Assistant:** Manage reminders and to-do lists.  
- **Creative Writing:** Automatically generate stories and creative content.  
- **Language Translation:** Translate text into different languages.  
- **Customer Support:** Automated responses for customer service.  
- **Social Media Content Creation:** Generate posts for social media.  
- **Motivation and Psychological Support:** Motivational quotes and psychological support tools.  
- **Business Tools:** Decision support and data analysis.  
- **Educational Tools:** Create lesson plans and generate quizzes.  

## Technologies Used  

- **FastAPI:** Framework for building APIs.  
- **OpenAI API:** For content generation (creative writing, automated responses, translations).  
- **Python:** Programming language used to develop the app.  
- **Uvicorn:** ASGI server to run the application.  

## Project Structure  

The project's directory structure is as follows:  

```
my_app/
│
├── oroscope/  
│   ├── natale_card.py 
│   └── oroscope.py  
│     
│
├── lang/  
│   ├── prompts.py  
│   └── responses.py   
│
├── pdf_generator/  
│   └── pdf_creator.py   
├── models.py    
│
└── app.py  # Main interface integrating all modules




{
"nome": "Antonio",
"data_nascita": "2024-12-12",
"ora_nascita": "23:00",
"luogo_nascita": "45.8091199,8.8374398",
"lingua": "it",
"tipi": "generico"
}
```



## How to Run the App  
```bash
# Crea un nuovo ambiente virtuale
C:\Python312\python.exe -m venv venv

# Attiva l'ambiente virtuale
.\venv\Scripts\activate

# Installa swisseph nel nuovo ambiente
pip install -r requirement.txt
```

1. **Clone the repository**  
   ```bash  
   git clone https://github.com/your-repo/my_app.git  
   cd my_app  
   ```

2. **Create a virtual environment (optional but recommended)**  
   ```bash  
   python -m venv venv  
   source venv/bin/activate  # On Windows: venv\Scripts\activate  
   ```

3. **Install dependencies**  
   ```bash  
   pip install -r requirements.txt  
   ```

4. **Set your OpenAI API key**  
   Add your OpenAI API key in the respective files, such as `personal_assistant.py`, `language_assistant.py`, etc.  

5. **Run the application**  
   ```bash  
   uvicorn app:app --reload  
   ```  

   The app will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).  

## Available APIs  

### **1. To-Do List Management**  

- **Endpoint:** `/tasks`  
  **Method:** `GET`  
  **Description:** Returns all tasks.  
  - **Output:** A list of tasks with names and due dates.  

  **`curl` Example:**  
  ```bash  
  curl -X 'GET' 'http://127.0.0.1:8000/tasks'  
  ```  

- **Endpoint:** `/tasks`  
  **Method:** `POST`  
  **Description:** Adds a new task.  
  - **Input:**  
    ```json  
    {  
      "task": "Buy milk",  
      "due_date": "2024-11-22"  
    }  
    ```  

  **`curl` Example:**  
  ```bash  
  curl -X 'POST' 'http://127.0.0.1:8000/tasks' -H 'Content-Type: application/json' -d '{"task": "Buy milk", "due_date": "2024-11-22"}'  
  ```  

### **2. Creative Writing**  

- **Endpoint:** `/generate_story/{theme}`  
  **Method:** `GET`  
  **Description:** Generates a creative story based on a given theme.  
  - **Input:** `theme` (String)  

  **`curl` Example:**  
  ```bash  
  curl -X 'GET' 'http://127.0.0.1:8000/generate_story/adventure'  
  ```  

### **3. Text Translation**  

- **Endpoint:** `/translate`  
  **Method:** `GET`  
  **Description:** Translates text into a target language.  
  - **Input:** `text` (String), `target_language` (String)  

  **`curl` Example:**  
  ```bash  
  curl -X 'GET' 'http://127.0.0.1:8000/translate?text=Hello%20world&target_language=Spanish'  
  ```  

### **4. Automated Customer Support**  

- **Endpoint:** `/respond`  
  **Method:** `GET`  
  **Description:** Generates an automated response to a customer message.  
  - **Input:** `message` (String)  

  **`curl` Example:**  
  ```bash  
  curl -X 'GET' 'http://127.0.0.1:8000/respond?message=I%20have%20a%20question%20about%20my%20order'  
  ```  

### **5. Motivational and Psychological Support**  

- **Endpoint:** `/motivational_quote`  
  **Method:** `GET`  
  **Description:** Returns a random motivational quote.  

  **`curl` Example:**  
  ```bash  
  curl -X 'GET' 'http://127.0.0.1:8000/motivational_quote'  
  ```  

## Contribution  

If you would like to contribute to this project, feel free to fork the repository and submit a pull request with your changes. Ensure you test all functionalities locally before submission.  

## License  

This project is distributed under the **MIT License**. See the LICENSE file for more details.  
```

This English `README.md` provides a clear explanation of the app's features, structure, and usage, making it accessible for an international audience.
