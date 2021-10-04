This script will export bb learn test to the local computer and format test questions so that those questions from the exported test can be imported to bb learn again. Currently this script works for most used type of questions. There are some limitation of the script which are listed below. Read the limitations of the script before using it.

1.  This script only works if you have Microsoft authenticator app is set up for the authentication to log in to bb learn.
2.  This script currently only works on mac.
3.  It can export below listed type of questions.
	- Calculated Numeric
	- Either/Or
	- Essay
	- File Response
	- Fill in the Blank
	- Matching
	- Multiple Answer
	- Multiple Choice
	- Opinion Scale/Likert
	- Ordering
	- Short Answer
	- True/False
	*****Below type of question currently can't be imported*****
	- Fill in Multiple Blanks 
	- Jumbled Sentence
	- Quiz Bowl
4.  For the Multiple Choice and Multiple Answer questions, first option (Option "A") is always marked as a correct answer and all the other options are always marked as a incorrect answer by default. For True/False questions, "true" is always marked as a correct answer by default. Need to check the correct answer before importing questions to the bb learn.
5.  Either/Or questions are treated as a true/false questions and "true" is always selected as a correct answer by default.
6.  This script can't export images that are attached to the questions. Also, there isn't anyway to import questions with images to the BB learn so test questions which needs to attach images has to edited manually after the successful import.
7.  This script can't export files that are attached to the questions. Also, there isn't anyway to import questions with file attachment to the BB learn so test questions which needs to attach file has to edited manually after the successful import.
8.  Question feedback can't be imported back to bb learn so feedback has to be added to the question manually after the successful import.

Instruction on how to run the script.

Mac

1.  Open terminal. 
2.  Go to the Export_BBTest directory. 
    For example - If you put downloaded folder on desktop then following command will work.
   				 "cd desktop/Export_BBTest"
3.  Run exportBBTest.py script with python3. Following command will run it.
    "python3 exportBBTest.py"
4.  Script will ask for the link of the test. This script will only work if you provide it the link that is obtained by following below steps.
	1.  Right click on the test and open test in new tab. Copy the link of this new tab.
5.  Provide your bb learn username and password when asked.
6.  Enter the name for your exported test. 
7.  You may need to approve the request to sign in to BB learn.
8.  If export is successful then there will be a .txt file with your given name in the Export_BBTest directory.
9.  This .txt can be used to upload questions to bb learn test.

Helpful links:

1. https://help.blackboard.com/Learn/Instructor/Ultra/Tests_Pools_Surveys/Reuse_Questions/Upload_Questions



