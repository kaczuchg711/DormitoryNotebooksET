*** Settings ***
Documentation    Suite description
Library  SeleniumLibrary
*** Variables ***
${user_name} =  tomekkacza
*** Test Cases ***

Brute force
    [Tags]    DEBUG
    Open Browser  http://0.0.0.0:8000  firefox
    Click Button  xpath=/html/body/div/section/div/div[1]/form/button
    Click element  xpath=//*[@id="id_dorms"]
    wait until element is visible   xpath=/html/body/div/section/div/div/div/form/select/option[5]
    click element   xpath=/html/body/div/section/div/div/div/form/select/option[5]


    @{Passwords}    Create List    pomidorowa1  pomidorowa2  pomidorowa3
    :FOR    ${Wrong Password}    IN    @{Passwords}
        Input Text  xpath=//*[@id="id_email"]  ${user_name}
        Input Password  xpath=//*[@id="id_password"]  ${Wrong Password}
        Click Button  xpath=/html/body/div/section/div/div/div/form/input[4]
#        Sleep  1s
    END

    Element Text Should Be  xpath=/html/body/div/section/div/div/div[2]/form/p  Wait 5s