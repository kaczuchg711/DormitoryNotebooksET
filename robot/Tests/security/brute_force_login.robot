*** Settings ***
Documentation    Suite description
Library  SeleniumLibrary
*** Variables ***
${user_name} =  tkacza
${password} =  pomidorowa
${min waiting time} =  5
${successful adress page after login} =  http://0.0.0.0:8000/choice/
${login adress page} =  http://0.0.0.0:8000/
*** Test Cases ***
Normal Login
    Normal Login

Brute force
    [Tags]    DEBUG
    Open Browser  ${login adress page}  firefox
    Log out
    Select organization  1
    Try 4 times give wrong password
    Element Text Should Be  xpath=/html/body/div/section/div/div/div[2]/form/p    too many attempts wait a moment
    Should fail log in
    Close Browser
    After 5s do login correct


#    todo ip should not be in blocked user
*** Keywords ***
Normal Login
    Open Browser  ${login adress page}  firefox
    Log out
    Select organization  1
    Give right values to log in and send
    Location Should Be   ${successful adress page after login}
    Log out
    Close Browser

After 5s do login correct
    Sleep  5
    Normal Login

Give right values to log in and send
    Input Text  xpath=//*[@id="id_email"]  ${user_name}
    Input Password  xpath=//*[@id="id_password"]  ${password}
    Click Button  xpath=/html/body/div/section/div/div/div/form/input[4]

Try 4 times give wrong password
        @{Passwords}    Create List    pomidorowa1  pomidorowa2  pomidorowa3  pomidorowa4
    FOR    ${Wrong Password}    IN    @{Passwords}
        Input Text  xpath=//*[@id="id_email"]  ${user_name}
        Input Password  xpath=//*[@id="id_password"]  ${Wrong Password}
        Click Button  xpath=/html/body/div/section/div/div/div/form/input[4]
    END

Should fail log in
    Give right values to login and send
    Location Should Be   ${login adress page}

Choose dorm
    [arguments]   ${dorm}=5
    wait until element is visible   xpath=/html/body/div/section/div/div/div/form/select/option[${dorm}]
    click element   xpath=/html/body/div/section/div/div/div/form/select/option[${dorm}]

Select organization
    [arguments]   ${organization}=1
    Click Button  xpath=/html/body/div/section/div/div[${organization}]/form/button

Log out
    Go To  ${login adress page}logout
