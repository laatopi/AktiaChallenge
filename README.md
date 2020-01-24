## Aktia Challenge

This is a short technical test made for Aktia.

It consists of two tasks for the Enron email dataset from https://www.cs.cmu.edu/~./enron/ , and was done with python 3.7, using pipenv.

The tasks were following:

1) Calculate how many emails were sent from each sender address to each recipient.
2) Calculate the average number of emails received per day per employee per day of week (monday, tuesday, etc.).

and running the main file will result in two .csv files, corresponding for each task, in the /output folder of this repository.

## Running the script

First you need to download the Enron email dataset from the link above, and extract the root folder of the zip called 'maildir' to the root of the project. This is required in order for the script to work.

There are two ways to run the script, using pipenv directly, or building a docker image that uses pipenv.
Both ways take care of the dependencies, and no extra installing should be required if you have working versions of either two programs.

Both ways require you to clone this repository first using:

```
git clone git@github.com:laatopi/AktiaChallenge.git
```


#### Running with pipenv

After cloning the repository, go to the root of the repository and run the following commands:

```
pipenv install 
pipenv run python src/main.py
```

#### Running with Docker

After cloning the repository, go to the root of the repository and run the following commands.

```
docker build -t challenge .
docker run -v $(pwd)/output:/app/output -v $(pwd)/maildir:/app/maildir challenge
```
#### After running
After running, the output files are created to 'output' folder of this repository.
The cells of the outputted csv files are seperated by comma, so when opening them make sure that the correct seperator is selected.



## Comments and thoughts about the challenge

I used around 8 hours of time to do this project, divided to two days, and I also did a really quick bugfix after the initial return on the code that delivers the result of task 2.

The task was fun but at the sametime at times difficult.
