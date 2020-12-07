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
Student logings
    Normal loging                                           1  DS B-1 Bydgoska  tomekkacza   pomidorowa
    Log out
    Student should not login to not associate dorm          1  DS4 Balon        tomekkacza   pomidorowa
    Log out
    Student should not login to not associate organization  2  Piast            tomekkacza   pomidorowa


Overvisor Login
    Normal loging                                              1  DS B-1 Bydgoska  mieczyslawa  pomidorowa
    Log out
    Overvisor can log in to any dorm in his organization       1  DS4 Balon        mieczyslawa  pomidorowa
    Log out
    Overvisor should not login to not associate organization   2  Piast            mieczyslawa   pomidorowa


Admin Login
    Admin should login any dorm           1  DS B-1 Bydgoska  tkacza  pomidorowa
    Log out
    Admin should login any organization   2  Piast            tkacza  pomidorowa

Brute force
    Normal loging
    Select organization  1
    Try a few times give wrong password  4
    Element Text Should Be  xpath=/html/body/div/section/div/div/div[2]/form/p    too many attempts wait a moment
    Should fail log in
    Close Browser
    After a few seconds do login correct  5

#    todo ip should not be in blocked user
*** Keywords ***
Admin should login any dorm
    [Arguments]  ${organization_id}  ${dorm_name}  ${login}  ${password}
    Normal loging   ${organization_id}  ${dorm_name}  ${login}  ${password}

Admin should login any organization
    [Arguments]  ${organization_id}  ${dorm_name}  ${login}  ${password}
    Normal loging   ${organization_id}  ${dorm_name}  ${login}  ${password}

Overvisor should not login to not associate organization
    [Arguments]  ${organization_id}  ${dorm_name}  ${login}  ${password}
    Failed loging   ${organization_id}  ${dorm_name}  ${login}  ${password}

Overvisor can log in to any dorm in his organization
    [Arguments]  ${organization_id}  ${dorm_name}  ${login}  ${password}
    Normal loging  ${organization_id}  ${dorm_name}  ${login}  ${password}

Student should not login to not associate dorm
    [Arguments]  ${organization_id}  ${dorm_name}  ${login}  ${password}
    Failed loging  ${organization_id}  ${dorm_name}  ${login}  ${password}

Student should not login to not associate organization
    [Arguments]  ${organization_id}  ${dorm_name}  ${login}  ${password}
    Failed loging  2  Piast  tomekkacza   pomidorowa

After a few seconds do login correct
    [Arguments]  ${seconds}
    Sleep  ${seconds}
    Startt
    Normal loging  1  DS B-1 Bydgoska  tomekkacza   pomidorowa

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