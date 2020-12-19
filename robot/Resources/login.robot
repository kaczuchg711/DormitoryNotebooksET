*** Settings ***
Library  SeleniumLibrary


*** Variables ***
${login adress page}  http://127.0.0.1:8000/
${successful adress page after login}  http://127.0.0.1:8000/choice/
${dorm_name}  DS B1 Bydgoska
*** Keywords ***
Startt
    Open Browser  ${login adress page}  firefox
    Log out

Exitt
    Log out
    Close Browser

Normal loging
    [Arguments]  ${organization_id}  ${dorm_name}  ${login}  ${password}
    Select organization  ${organization_id}
    Input values to log in form and send it  ${dorm_name}  ${login}  ${password}
    Location Should Be   ${successful adress page after login}

Failed loging
    [Arguments]  ${organization_id}  ${dorm_name}  ${login}  ${password}
    Select organization  ${organization_id}
    Input values to log in form and send it  ${dorm_name}  ${login}  ${password}
    Location Should Be   ${login adress page}

Input values to log in form and send it
    [Arguments]  ${dorm_name}  ${user_name}  ${password}
    Select Dorm  ${dorm_name}
    Input Text  xpath=//*[@id="id_email"]  ${user_name}
    Input Password  xpath=//*[@id="id_password"]  ${password}
    wait until page contains element  xpath=/html/body/div/section/div/div/div/form/input[4]
    Click Button  xpath=/html/body/div/section/div/div/div/form/input[4]

Select organization
    [Arguments]   ${organization}=1
    Click Button  xpath=/html/body/div/section/div/div[${organization}]/form/button

Log out
    Go To  ${login adress page}logout

Select Dorm
    [Arguments]  ${dorm name}
    Select From List By Label  xpath=/html/body/div/section/div/div/div/form/select  ${dorm name}

#Todo routing test
