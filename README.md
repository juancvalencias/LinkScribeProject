# LinkScribe
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
