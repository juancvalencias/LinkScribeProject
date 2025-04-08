# LinkScribe
## Introduction
Meet LinkScribe: Your Intelligent Link Manager

In today's digital world, we're constantly bombarded with links – articles to read later, products to consider, resources for projects, and social media posts we want to revisit. This deluge often leads to a chaotic mess of open tabs, scattered notes, and forgotten URLs. Sound familiar?

LinkScribe is designed to be your intelligent solution to this digital dilemma. It's more than just a bookmarking tool; it's a smart link management application that allows you to store, categorize, and understand your links without even needing to open them.

Imagine a world where you can quickly grasp the essence of a link, understand its context, and organize it effectively, all within a clean and intuitive interface. Whether you're a student juggling research papers, a professional tracking industry news, a creative gathering inspiration, or simply someone who wants to stay organized online, LinkScribe empowers you to take control of your digital information flow.

By providing essential context and allowing you to categorize and search your saved links, LinkScribe transforms your scattered collection into a valuable and easily accessible knowledge base. Stop wasting time opening countless tabs and start managing your digital life with LinkScribe.
## Why this app?

1. Digital Clutter and Information Overload
2. Time-Consuming and Inefficient Workflow

## Technical definition
- Facebook BART-large-CNN: A pre-trained transformer model specifically fine-tuned for text summarization. We utilize the facebook/bart-large-cnn architecture to automatically generate concise and informative summaries of the linked web pages without requiring the user to open them. This allows for quick understanding of the link's content and context.
- Web Scraping Model (Beautiful Soup): To extract the relevant textual content from web pages for summarization, LinkScribe employs Beautiful Soup. This Python library excels at parsing HTML and XML documents, enabling robust and efficient extraction of article text, product descriptions.
- MongoDB (NoSQL Database): We've chosen MongoDB, a NoSQL document database, for storing link data and associated metadata (summaries, tags, categories). The key reasons for this choice include:

    Flexibility: The schema-less nature of MongoDB allows us to easily adapt to varying content structures of different web pages and accommodate future feature additions without rigid schema migrations.
    Scalability: MongoDB is designed for horizontal scaling, making it well-suited for handling a potentially large volume of user data and links.
    Performance with Unstructured Data: Document databases excel at storing and querying JSON-like documents, which naturally represent the extracted link information and generated summaries.

- Streamlit (Frontend): Streamlit is used to build the user-friendly web interface. Its key facilities for LinkScribe include:
  - Rapid Development: Streamlit simplifies the process of creating interactive web applications with minimal code, allowing for quick prototyping and iteration.S
  - Seamless Integration with Python: As a Python-centric framework, it integrates smoothly with the backend logic and machine learning models.
## Application overview
In this application, the user will be able to enter a link from the web, this will be classified within the 16 predetermined categories:
1. Travel
2. Social 
3. Networking and Messaging
4. News
5. Streaming Services
6. Sports
7. Photographys
8. Law and Government
9. Health and Fitness
10. Games
11. E-Commerce
12. Forums
13. Food
14. Education
15. Computers and Technology 
16. Business/Corporate
17. Adult 

A brief description of the site will also be added.
The user will have the option to store his search in the database if preferred.

The application also has a search system of stored searches, just use a keyword and you will be able 
to see which ones match your search, providing the hyperlink, the category and a brief description of the page.

## Frontend and its content

Streamlit was used as user interface, here we can find a slide bar containing homepage and datapage, as in home and data, we will have a search bar as shown in the following pictures

![Home page](https://i.imgur.com/37I99E5.jpg "Home page")

## Backend and its content

### Used tools

The application architecture incorporates two primary classes: ScrapTool, responsible for extracting data from web pages, and TextClassifier. The TextClassifier class provides methods for categorizing user-provided web pages and includes a pre-trained Hugging Face model for content summarization.

For more information, visit the [Hugging Face Transformers library](https://huggingface.co/docs/transformers/index).

### Notebook

The training of the classification model was adapted from the work presented in the Kaggle notebook [Classification of websites](https://www.kaggle.com/code/hetulmehta/classification-of-websites) by hetulmehta, which explores the accuracy of various classification models.

### Data

This directory contains the trained models, including both the vector model and the classification model, along with the dataset used for their training.

### Database

This module establishes the database configuration for communication, storage, and search operations. It provides utility functions, encapsulated within the MongoDBHandler class, to facilitate these tasks.

## Frontend-backend communication

Built with FastAPI, the API offers three core methods: save to store data, search to retrieve information, and processing to manage and analyze links submitted by end-users.

## Considerations

- The database will work as long as you have MongoDB installed, in case you want to use the cloud service you should follow the following steps [MongoDB Cloud](https://www.mongodb.com/resources/products/platform/mongodb-atlas-tutorial).
- The classification model is specifically trained for English language content. Classifying web pages in other languages may result in inaccurate predictions.
- The scraping model extracts information, including images. However, in certain instances, image extraction may fail, resulting in their absence from the output.

## How to use
