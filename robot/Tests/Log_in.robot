*** Settings ***
Documentation    Suite description
Library  SeleniumLibrary
Resource  ../Resources/res1.robot
*** Variables ***
${user_name} =  tomekkacza
*** Test Cases ***
Log in
    Log in  ${user_name}