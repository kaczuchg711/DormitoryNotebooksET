*** Settings ***
Library  SeleniumLibrary
Library  Dialogs

Resource  ../Resources/login.robot

*** Test Cases ***
Rent Prezentation
    Startt
    Normal loging  1  DS B1 Bydgoska  student1  pomidorowa
    Go to request breakdown page
    log out
    Normal loging  1  DS B1 Bydgoska  porter1  pomidorowa
    Go to request breakdown page
    pause execution
    Exitt

*** Keywords ***
Request breakdown
    Go to request breakdown page
    Click element  xpath=/html/body/section/div/div/form/button

Go to request breakdown page
    Click element  xpath=/html/body/section/div/div/div[2]/form/button
    Wait Until Element Is Visible  xpath=//*[@id="id_description"]
    Input Text  xpath=//*[@id="id_description"]  przykladowy opis