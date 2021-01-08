*** Settings ***
Library  SeleniumLibrary
Library  Dialogs

Resource  ../Resources/login.robot
*** Variables ***
${user_name} =  tomekkacza
*** Test Cases ***

Shortcut
    Startt
    Normal loging  1  DS B1 Bydgoska  student1  pomidorowa
    Click button  xpath=/html/body/section/div/div/div[5]/form/button
    Sleep  1
        Pause Execution

    Click button  xpath=/html/body/section/div/div/form/input[2]
    Exitt