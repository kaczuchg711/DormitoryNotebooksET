*** Settings ***
Library  SeleniumLibrary
Library  Dialogs
Resource  ../Resources/res1.robot
Test Setup  log in  mieczyslawa

*** Test Cases ***
foo aaaaaaaaaa
    Click Button  xpath=/html/body/section/div/div/div[4]/form/button
    Click element  xpath=/html/body/section/div/div/form/select
    wait until element is visible   xpath=/html/body/section/div/div/form/select/option[3]
    click element   xpath=/html/body/section/div/div/form/select/option[3]
    Click Button  xpath=/html/body/section/div/div/form/input[2]
    Sleep  1s
    Close Browser



