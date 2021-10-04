#*************************************************************
#*************************************************************
# Importing all the required modules
#*************************************************************
#*************************************************************


import os
import time
import getpass
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


#*************************************************************
#*************************************************************
# All the function definitions
#*************************************************************
#*************************************************************

#function is_int checks if the given string is integer
#Return - True is string is integer otherwise 
def is_int(s):

    try:
        int(s)
        return True
    except ValueError:
        return False

#Below are the functions that formats the questions text to valid bb learn import format

def format_multiple_choice_question(questionText, file2, eachQuestions):

    questionImportString = "MC" + "\t"
    questionImportString += questionText + "\t"

    for i in range(4, len(eachQuestions)):
        questionImportString += eachQuestions[i] + "\t"
        if (i == 4):
            questionImportString += "correct" + "\t"
        else:
            questionImportString += "incorrect" + "\t"

    questionImportString += "\n"

    file2.write(questionImportString)

def format_multiple_answer_question(questionText, file2, eachQuestions):

    questionImportString = "MA" + "\t"
    questionImportString += questionText + "\t"

    for i in range(4, len(eachQuestions)):
        questionImportString += eachQuestions[i] + "\t"
        if (i == 4):
            questionImportString += "correct" + "\t"
        else:
            questionImportString += "incorrect" + "\t"

    questionImportString += "\n"

    file2.write(questionImportString)

def format_true_false_question(questionText, file2):

    questionImportString = "TF" + "\t"
    questionImportString += questionText + "\t"
    questionImportString += "true"
    questionImportString += "\n"

    file2.write(questionImportString)

def format_essay_question(questionText, file2, eachQuestions):

    questionImportString = "ESS" + "\t"
    questionImportString += questionText + "\t"
    if(len(eachQuestions) > 3):
        #Get the Answer Text
        if(not((len(eachQuestions) == 4) and (eachQuestions[3] == "Answer"))):
            if(len(eachQuestions) == 5):
                eachQuestions[3] += " " + eachQuestions[4]
                eachQuestions.pop(4)
            answerText = eachQuestions[3].split("Answer ")[1]
            questionImportString += answerText + "\t"
    
    questionImportString += "\n"

    file2.write(questionImportString)

def format_short_answer_question(questionText, file2, eachQuestions):

    questionImportString = "SR" + "\t"
    questionImportString += questionText + "\t"
    if(len(eachQuestions) > 3):
        #Get the Answer Text
        if(not((len(eachQuestions) == 4) and (eachQuestions[3] == "Answer"))):
            if(len(eachQuestions) == 5):
                eachQuestions[3] += " " + eachQuestions[4]
                eachQuestions.pop(4)
            answerText = eachQuestions[3].split("Answer ")[1]
            questionImportString += answerText + "\t"
    
    questionImportString += "\n"

    file2.write(questionImportString)

def format_order_question(questionText, file2, eachQuestions):

    questionImportString = "ORD" + "\t"
    questionImportString += questionText + "\t"

    #Reformat the eachQuestion list answer part
    if (len(eachQuestions[5]) == 2):
        totalOptions = int ((len(eachQuestions) - 6) // 4)

        for i in range(0, totalOptions):
            indexOfOptionToFormat = i + 5
            
            eachQuestions[indexOfOptionToFormat] += " " + eachQuestions[indexOfOptionToFormat + 1]
            eachQuestions.pop(indexOfOptionToFormat + 1)

        for i in range(0, totalOptions):
            indexOfOptionToFormat = i + 11
            
            eachQuestions[indexOfOptionToFormat] += " " + eachQuestions[indexOfOptionToFormat + 1]
            eachQuestions.pop(indexOfOptionToFormat + 1)

    numberOfOptions = int ((len(eachQuestions) - 6) / 2)
    for i in range(6 + numberOfOptions, len(eachQuestions)):
        questionImportString += eachQuestions[i].split(". ")[1] + "\t"    
    questionImportString += "\n"

    file2.write(questionImportString)

def format_matching_question(questionText, file2, eachQuestions):

    questionImportString = "MAT" + "\t"
    questionImportString += questionText + "\t"

    #Reformat the eachQuestion list answer part
    if (len(eachQuestions[5]) == 7):
        totalOptions = (len(eachQuestions) - 5) // 4

        for i in range(0, totalOptions):
            indexOfOptionToFormat = i + 5
            
            for j in range(0 , 3):
                eachQuestions[indexOfOptionToFormat] += " " + eachQuestions[indexOfOptionToFormat + 1]
                eachQuestions.pop(indexOfOptionToFormat + 1)
    
    totalOptions = len(eachQuestions) - 5
    correctOptionsString = []
    matchingQuestionString = []
    correctOptions = []

    for i in range(5, len(eachQuestions)):
        correctAnswerOption = eachQuestions[i].split(". ")[0]
        cureentChoiceOptionString = eachQuestions[i].split(". ")[1]
        cureentChoiceOption = cureentChoiceOptionString[len(cureentChoiceOptionString) - 1]
        matchingOptionAndCurrentChoiceString = eachQuestions[i].split(". ")[2]
        cureentChoiceString = matchingOptionAndCurrentChoiceString[0:len(matchingOptionAndCurrentChoiceString) - 2]
        matchingOption = matchingOptionAndCurrentChoiceString[-1]
        matchingOptionString = eachQuestions[i].split(". ")[-1]

        correctOptions.append(correctAnswerOption)
        matchingQuestionString.append(cureentChoiceString) 
        correctOptionsString.append(matchingOptionString)

    for i in range(0, totalOptions):
        questionImportString += matchingQuestionString[i] + "\t"
        questionImportString += correctOptionsString[(ord(correctOptions[i]) - 65)] + "\t"

    questionImportString += "\n"

    file2.write(questionImportString)

def format_file_response_question(questionText, file2):

    questionImportString = "FIL" + "\t"
    questionImportString += questionText + "\t"

    questionImportString += "\n"

    file2.write(questionImportString)

def format_fill_in_the_blank_question(questionText, file2, eachQuestions):

    questionImportString = "FIB" + "\t"
    questionImportString += questionText + "\t"

    if (eachQuestions[3].split(" ")[0] == "Evaluation" and  eachQuestions[3].split(" ")[1] == "Method"):
        eachQuestions.pop(3)

    for i in range(3, len(eachQuestions)):
        questionImportString += eachQuestions[i].split("Exact Match")[1] + "\t"

    questionImportString += "\n"

    file2.write(questionImportString)

def format_numeric_question(questionText, file2, eachQuestions):

    questionImportString = "NUM" + "\t"
    questionImportString += questionText + "\t"

    answerText = eachQuestions[-2].split("Answer ")[1]
    answerRange = eachQuestions[-1].split("Answer range +/- ")[1]

    questionImportString += answerText + "\t"
    questionImportString += answerRange + "\t"

    questionImportString += "\n"

    file2.write(questionImportString)

def format_opinion_question(questionText, file2):

    questionImportString = "OP" + "\t"
    questionImportString += questionText + "\t"

    questionImportString += "\n"

    file2.write(questionImportString)

def format_jumbled_sentence_question(questionText, file2):

    questionImportString = "JUMBLED_SENTENCE" + "\t"
    questionImportString += questionText + "\t"

    questionImportString += "\n"

    file2.write(questionImportString)

def format_quiz_bowl_question(questionText, file2):

    questionImportString = "QUIZ_BOWL" + "\t"
    questionImportString += questionText + "\t"

    questionImportString += "\n"

    file2.write(questionImportString)



#*************************************************************
#*************************************************************
# Start of the main script
#*************************************************************
#*************************************************************



#Getting chromedriver for selenium
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
#PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")

#Get URL of the take test page from the user
userUrl = input("Enter the link - ")

#Extract course id and content id from the take test page link entered by the user
course_id = userUrl.split("=")[1].split("&")[0]
content_id = userUrl.split("=")[2].split("&")[0]

#print(course_id)
#print(content_id)

#Required URL for exporting purpose
requiredUrl = "https://learn.dcollege.net/webapps/assessment/do/content/assessment?action=MODIFY&course_id="
requiredUrl += course_id 
requiredUrl += "&content_id=" 
requiredUrl += content_id 
requiredUrl += "&assessmentType=Test&method=modifyAssessment#contextMenu"
#print("https://learn.dcollege.net/webapps/assessment/do/content/assessment?action=MODIFY&course_id=_123_1&content_id=_10601777_1&assessmentType=Test&method=modifyAssessment#contextMenu" == requiredUrl)

#Get the username and password of the user and name for the test file 
userUsername = input("Enter your drexel username - ")
userPassword = getpass.getpass("Enter your bblearn password - ")
userTestFileName = input("Enter the name for your test - ")

driver = webdriver.Chrome(executable_path = DRIVER_BIN)

#opening bblearn link in the browser
driver.get("https://learn.dcollege.net/")

#Click on Sign in with Drexel Connect button
driver.find_element_by_id("caslink1").click()

#Find the username and password input area in drexel connect login page
username = driver.find_element_by_id("username")
password = driver.find_element_by_id("password")

#Enter user entered username and password
username.send_keys(userUsername)
password.send_keys(userPassword)

#Click on sign in button
driver.find_element_by_name("_eventId_proceed").click()

#Open test edit page
driver.get(requiredUrl)

#content_listContainer contains all the questions with the options and correct answer
questionContainer = driver.find_element_by_id("content_listContainer") 
allQuestions = questionContainer.text

#print(allQuestions)

#Quit the chrome drive
driver.close()

#Create .txt file name and give it a temp name
#Write and store allQuestions in that file
file = open(userTestFileName + "_temp.txt", "w")
file.write(allQuestions)
file.close()

#Reopen that file to read
file = open(userTestFileName + "_temp.txt", "r")
lines = file.read().splitlines()
file.close()
os.remove(userTestFileName + "_temp.txt")

#Create .txt file name and give it a user entered name
#Write and store allQuestions in the valid bb learn import format
file2 = open(userTestFileName + ".txt", "w")

#Store all the details of the questions in a questionList,
#Store all the questionList in finalQuestionsWithAllContentsList
questionList = []
finalQuestionsWithAllContentsList = []
totalQuestions = 0

for i in range(0, len(lines)):

    #Strip any whitespace from the start and end of the lines
    lines[i] = lines[i].strip()
    x = lines[i].split(".")
    
    if(is_int(x[0]) and (x[1] == "") and (int(x[0]) == totalQuestions + 1) ):
        #Count total number of questions in the file
        totalQuestions += 1
        finalQuestionsWithAllContentsList.append(questionList)
        questionList = []
    else:
        questionList.append(lines[i])

finalQuestionsWithAllContentsList.append(questionList)
finalQuestionsWithAllContentsList.pop(0)


for eachQuestions in finalQuestionsWithAllContentsList:

    #Get the questionType
    questionType = eachQuestions[0].split(":")[0]

    #Get the Quetion Text
    if (eachQuestions[2] == "Question"):
        eachQuestions[2] += " " + eachQuestions[3]
        eachQuestions.pop(3)

    questionText = eachQuestions[2].split("Question ")[1]

    #Need to remove Correct feedback and Incorrect feedback from eachQuestions list
    if (eachQuestions[-2] == "Incorrect Feedback"):
        eachQuestions.pop(-2)
        eachQuestions.pop(-1)
    if (eachQuestions[-2] == "Correct Feedback"):
        eachQuestions.pop(-2)
        eachQuestions.pop(-1)

    if(questionType == "Multiple Choice"):
        format_multiple_choice_question(questionText, file2, eachQuestions)
    elif(questionType == "Multiple Answer"):
        format_multiple_answer_question(questionText, file2, eachQuestions)
    elif(questionType == "True/False" or questionType == "Either/Or"):
        format_true_false_question(questionText, file2)
    elif(questionType == "Essay"):
        format_essay_question(questionText, file2, eachQuestions)
    elif(questionType == "Short Answer"):
        format_essay_question(questionText, file2, eachQuestions)
    elif(questionType == "Ordering"):
        format_order_question(questionText, file2, eachQuestions)
    elif(questionType == "Matching"):
        format_matching_question(questionText, file2, eachQuestions)
    elif(questionType == "Fill in the Blank"):
        format_fill_in_the_blank_question(questionText, file2, eachQuestions)
    elif(questionType == "File Response"):
        format_file_response_question(questionText, file2)
    elif(questionType == "Calculated Numeric"):
        format_numeric_question(questionText, file2, eachQuestions)
    elif(questionType == "Opinion Scale/Likert"):
        format_opinion_question(questionText, file2)
    elif(questionType == "Jumbled Sentence"):
        format_opinion_question(questionText, file2)
    elif(questionType == "Quiz Bowl"):
        format_opinion_question(questionText, file2)

print("**********")
print("Successfully exported " + str(totalQuestions) + " questions.")
print("All the questions are written in \"" + userTestFileName + ".txt\" file.")
print("All the questions are formatted so you can import the file to the bb learn.")
print("**********")

file2.close()
