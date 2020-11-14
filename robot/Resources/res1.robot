*** Settings ***
Library  SeleniumLibrary

*** Variables ***
${USER_NAME} =  tomekkacza
*** Keywords ***
log in
    [Arguments]  ${user_name}
    Open Browser  http://0.0.0.0:8000  geckodriver
    Click Button  xpath=/html/body/div/section/div/div[1]/form/button
    Click element  xpath=//*[@id="id_dorms"]
    wait until element is visible   xpath=/html/body/div/section/div/div/div/form/select/option[5]
    click element   xpath=/html/body/div/section/div/div/div/form/select/option[5]
    Input Text  xpath=//*[@id="id_email"]  ${user_name}
    Input Password  xpath=//*[@id="id_password"]  pomidorowa
    Click Button  xpath=/html/body/div/section/div/div/div/form/input[4]

#Todo routing test