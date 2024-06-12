<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![LinkedIn][linkedin-shield]][linkedin-url]





<!-- TABLE OF CONTENTS -->
<details open="open">
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
        <li><a href="#pythonanywheredeploy">Python Anywhere Deployment</a></li>
        <li><a href="#herokudeploy">Heroku Deployment (OLD)</a></li>
      </ul>
    </li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

There are many great resources available online or on your mobile to learn languages, however, I didn't find one that really suit my needs so I created [this](https://dictionary-dash-app.herokuapp.com/) enhanced one. I want to create an application that let me save **relevant definitions and translations**, and allow me to **practice effectively** by focusing on where improvement is needed  -- I think this is it.

Here's why:
* Vocabulary is an essential part of learning a language
* A robust vocabulary improves all areas of communication — listening, speaking, reading and writing
* A larger vocabulary can be a stepping stone to higher levels of language fluency

Of course, no application will serve all people since your needs may be different. So I'll be adding more in the near future. You may also suggest changes by forking this repo and creating a pull request or opening an issue. Thanks to all the people who have contributed to expanding this application! Hope you enjoy it as much as I do!

A list of commonly used resources that I find helpful are listed in the acknowledgements.

### Built With

Major frameworks that I built the project with:
* [Dash](https://plotly.com/dash/)
* [Python Anywhere](https://www.pythonanywhere.com/)
* [Heroku (OLD)](https://www.heroku.com/)

It's built on top of the following public website:
* [Reverso](https://dictionary.reverso.net/)

Using webscraping with following open source library:
* [Beautiful Soup](https://beautiful-soup-4.readthedocs.io/en/latest/)

When dealing with text, understanding encoding is paramount:
* [L'encoding en python une bonne fois pour toute](http://sametmax.com/lencoding-en-python-une-bonne-fois-pour-toute/)
* [What does unicodedate normalize do in Python](https://stackoverflow.com/questions/51710082/what-does-unicodedata-normalize-do-in-python)
* [Python removing xa0 from String](https://stackoverflow.com/questions/10993612/python-removing-xa0-from-string)

<!-- GETTING STARTED -->
## Getting Started

Here is some instructions on how to set up the project locally.
Get a local copy up and running and follow these simple example steps.

### Prerequisites

You'll need to have Python installed on your machine.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/mathieu-calvo/Dico-App-Web-Scraping.git
   ```
2. Create and activate a virtual environment (example of how I do it, could be done differently)
   ```sh
   python -m venv venv 
   
   cd \venv\Scripts>
   
   activate
   ```
3. Install all dependencies into your virtual environment (I use pip)
   ```sh
   pip install -r requirements.txt
   ```
4. Launch the app locally
   ```sh
   python index.py
   ```
5. Go to URL indicated to see the app launched locally on your browser
   ```sh
   Dash is running on http://127.0.0.1:8050/
     * Serving Flask app "app" (lazy loading)
     * Environment: production
       WARNING: This is a development server. Do not use it in a production deployment.
       Use a production WSGI server instead.
     * Debug mode: on
   ```
### Python Anywhere Deployment

Moved to PythonAnwhere in 2024 when Heroku stopped being free. It is also easier to deploy. Free account is limited to one web app with 512MB of file storage (as of June 2024).

1. Transfer repository to PythonAnyWhere
- Create new PythonAnyWhere account
- Open new Bash console
- ```git clone [copy-paste clone link from GitHub]```

2. Create virtual environment on PythonAnyWhere and install libraries:
- ```mkvirtualenv myvirtualenv --python=/usr/bin/python3.8```
- ```cd [git repository name from step 1]``` here ```Dico-App-Web-Scraping```
- ```pip install -r requirements.txt```

3.	Add your new app to PythonAnyWhere:
- Click on Add a New Web App button
- Next 🡪 Flask 🡪 Python 3.8 🡪 Next
    
4.	Once all libraries from requirements.txt have been installed, go to Web tab if need be, 
- change the “Source Code” to: ```home/myusername/[git repository name from step 1]]```
- under the “Virtualenv” section, type ```myvirtualenv``` (which was the name you gave to your PythonAnyWhere virtual environment from step 2)
- under the “WSGI configuration file” section, update the file. 
    - Update the end of Project home’s path to match your app name. ```Dico-App-Web-Scraping```
    - Change last line of code to: ```from index import server as application```
    - Save the file
- go back to “Web” tab and refresh the app with the Reload button

Free accounts have only 512MB of file storage. If you delete an app, the virtual environment doesn’t get deleted with it. Therefore, to save space, remove the old virtual environment by opening your Bash and typing:
```rm -rf /home/myusername/.virtualenvs/myvirtualenv```

### Heroku Deployment (OLD)

Heroku can be quite confusing at first as it stores its own codebase for builds and deployments, and it not necessarily match what you have on Git, hence the confusion. 

If you like to keep your latest code in Git like I do, remember to always do the following:

1.
    ```sh
    git push heroku origin/main:main
    ```
2.
    ```sh
    heroku ps:scale web=1
    ```
3.
    ```sh
    heroku open
    ```
   
You may be asked to do ```heroku login``` first
   
<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- CONTACT -->
## Contact

Your Name - Mathieu Calvo

Project Link: [https://github.com/mathieu-calvo/Dico-App-Web-Scraping](https://github.com/mathieu-calvo/Dico-App-Web-Scraping)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [Deploying Dash apps using Python anywhere](https://www.youtube.com/watch?v=WOWVat5BgM4)
* [Heroku for Sharing Public Dash apps for Free](https://dash.plotly.com/deployment)
* [Getting started on Heroku with Python](https://devcenter.heroku.com/articles/getting-started-with-python)
* [From Prototype to Cloud: A Python Recipe Converter](https://www.justinmklam.com/posts/2018/04/python-flask-heroku-tutorial/?c=7013A000000txcVQAQ&utm_campaign=Onboarding-2.0-Deploy-1.1-Python&utm_medium=email&utm_source=nurture&utm_content=community&utm_term=flask-tutorial-recipe-converter)
* [Deploying Multi Page App to Heroku](https://community.plotly.com/t/deploying-multi-page-app-to-heroku-not-deploying-as-set-up/7877/4)
* [Set up automatic deploys from Git to Heroku](https://devcenter.heroku.com/articles/github-integration#automatic-deploys)
* [README Template](https://github.com/othneildrew/Best-README-Template)



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/mathieu-calvo-b72758a3
[product-screenshot]: images/screenshot.png