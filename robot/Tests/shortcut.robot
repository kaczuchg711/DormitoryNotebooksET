*** Settings ***
Documentation    Suite description
Library  SeleniumLibrary
Resource  ../Resources/res1.robot
*** Variables ***
${user_name} =  tomekkacza
*** Test Cases ***
Shortcut
    Log in  ${user_name}
    Click Button  xpath=/html/body/section/div/div/div[4]/form/button

