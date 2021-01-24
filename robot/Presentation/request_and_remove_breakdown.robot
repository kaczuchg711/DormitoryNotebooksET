*** Settings ***
Library  SeleniumLibrary
Library  Dialogs

Resource  ../Resources/login.robot

*** Test Cases ***
Breakdown
    Startt
    Normal loging  1  DS B1 Bydgoska  student1  pomidorowa
    Request breakdown
    log out
    Normal loging  1  DS B1 Bydgoska  porter1  pomidorowa
    Remove breakdown
    Exitt
*** Keywords ***
Remove breakdown
    Go to request breakdown page
    pause execution
    Click Button  xpath=/html/body/div/table/tbody/tr[last()]/th[7]/button
    pause execution

Request breakdown
    pause execution
    Go to request breakdown page
    pause execution
    Click element  xpath=/html/body/section/div/div/form/button
    pause execution

Go to request breakdown page
    [Arguments]  ${description}
    Click element  xpath=/html/body/section/div/div/div[2]/form/button
    Wait Until Element Is Visible  xpath=//*[@id="id_description"]
    Input Text  xpath=//*[@id="id_description"]  ${description}