*** Settings ***
Documentation    Suite description
Library  SeleniumLibrary
Resource  ../../Resources/login.robot
Test Setup       Startt
Test Teardown    Exitt
*** Variables ***
${user_name} =  tkacza
${password} =  pomidorowa
${wrong password} =  za slona pomidorowa
${browser} =  firefox
${min waiting time} =  5
${successful adress page after login} =  http://0.0.0.0:8000/choice/
${login adress page} =  http://0.0.0.0:8000/
*** Test Cases ***
Normal Login
    Normal Login  1

Brute force
    [Tags]    DEBUG
    Select organization  1
    Try a few times give wrong password  3
    Element Text Should Be  xpath=/html/body/div/section/div/div/div[2]/form/p    too many attempts wait a moment
    Should fail log in
    Close Browser
    After a few seconds do login correct  5


#    todo ip should not be in blocked user
*** Keywords ***
After a few seconds do login correct
    [Arguments]  ${seconds}
    Sleep  ${seconds}
    Startt
    Normal Login  1

Give right values to log in and send
    Input Text  xpath=//*[@id="id_email"]  ${user_name}
    Input Password  xpath=//*[@id="id_password"]  ${password}
    Click Button  xpath=/html/body/div/section/div/div/div/form/input[4]

Try a few times give wrong password
    [Arguments]  ${times}
    FOR    ${INDEX}    IN RANGE    0   ${times}
        Input Text  xpath=//*[@id="id_email"]  ${user_name}
        Input Password  xpath=//*[@id="id_password"]  ${Wrong Password}
        Click Button  xpath=/html/body/div/section/div/div/div/form/input[4]
    END

Should fail log in
    Give right values to login and send
    Location Should Be   ${login adress page}