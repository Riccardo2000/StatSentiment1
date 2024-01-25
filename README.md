# README for Sentiment Analysis and Data Visualization Tool
# Overview
This Python application is designed for data analysis and visualization. It supports loading, analyzing, and visualizing data from Excel files, performing sentiment analysis on Word documents, and editing data directly in the application.
# Approaches
I used two types of approaches:
Modular Approach: This method involves splitting the program into multiple function files, each handling specific tasks like file management, data analysis, and UI interactions. It's beneficial for organization, maintainability, and scalability, especially in larger projects.
Single Script Approach: All functionalities are contained within a single script. This is simpler and may be preferable for smaller projects, but it can become unwieldy as the program grows in complexity
# Features
Load and display data from Excel files.
Read and display text from Word documents.
Perform sentiment analysis on the loaded text using VaderSentiment.
Execute descriptive statistics, linear regression, and logistic regression analyses.
Create various types of plots (bar, line, scatter).
Conduct correlation analysis between chosen variables.
Edit data entries directly in the interface.
Save updated data back to Excel files.
# Installation
Ensure Python is installed and run the following to install dependencies:
# Library
` pandas` , `tkinter` , ` matplotlib` , ` docx` , ` sklearn` , ` vaderSentiment` 
# Copy code
pip install pandas scikit-learn matplotlib python-docx vaderSentiment
Usage
Start the application by running .python app.py
Use the GUI to load data, perform analyses, and visualize results.
For sentiment analysis, load a Word document and click the corresponding button.


# License
MIT.

