OUTPUT

![Screenshot 2024-05-04 194639](https://github.com/Hasibwajid/Ai-chatbot-based-on-intent-classification-using-Deep-learning-cnn/assets/72168225/8fa6d6c1-a494-478d-a67a-86af1b62f640)


**AI Chatbot Project**
**Overview**
This project is a simple AI-based chatbot developed using Python and TensorFlow. The chatbot is trained to understand and respond to user queries related to artificial intelligence (AI) concepts. It utilizes natural language processing (NLP) techniques and a deep learning model to interpret user input and generate appropriate responses.

**Features**

**Natural Language Understanding:** The chatbot employs NLP techniques to understand the intent behind user messages.

**Intent Classification:** It classifies user queries into predefined intent categories such as greetings, definitions, applications, and more.

**Response Generation:** Based on the predicted intent, the chatbot generates relevant responses from a predefined set of responses stored in a JSON file.

**Graphical User Interface (GUI):** The chatbot comes with a simple graphical user interface built using Tkinter, allowing users to interact with it via a text input field.

**Technologies Used**
Python
TensorFlow
Natural Language Toolkit (NLTK)
Tkinter (for GUI)

**Getting Started**
To run the chatbot:

**Clone the Repository:**

      git clone https://github.com/Hasibwajid/Ai-chatbot-based-on-intent-classification-using-Deep-learning-cnn.git
      cd chatbot
      
**Install Dependencies:**
      
      pip install -r requirements.txt
      
**Run the Training Script:**

    python train_chatbot.py
    
**Run the Chatbot Script:**

    python chatbot.py
    
**Interact with the Chatbot:**
Once the chatbot script is running, a graphical user interface (GUI) window will appear.
Type messages in the input field and press "Send" to interact with the chatbot.
The chatbot will classify your intent and provide appropriate responses based on the trained model.

**Modifying Chatbot Domain or Role**
The chatbot's domain or role can be modified to suit specific use cases or industries. Here's how you can customize it:

Update the intents in the intents.json file with new intents relevant to the desired domain or role.
Re-train the model by running the training script (train_chatbot.py) after updating the intents.
Adjust the response generation logic in the get_response() function of the chatbot.py script if necessary.
Test and iterate on the chatbot's performance with sample queries to ensure it understands and responds appropriately to the new domain or role.
