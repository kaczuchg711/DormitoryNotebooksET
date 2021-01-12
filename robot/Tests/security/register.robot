*** Settings ***
Library  SeleniumLibrary
Resource  ../../Resources/login.robot
*** Variables ***
${organization_id}  1

*** Test Cases ***
Register
    Open browser  http://127.0.0.1:8000/  firefox
    Select organization  ${organization_id}
    Click Button  xpath=/html/body/div/section/div/div/div[2]/div/form/button
    Input Text  xpath=//*[@id="id_first_name"]  Norbert
    Input Text  xpath=//*[@id="id_last_name"]  Kalik
    Input Text  xpath=//*[@id="id_email"]  kalik@kalik.com
    Input Text  xpath=//*[@id="id_room"]  206
    Input Text  xpath=//*[@id="id_password1"]  pomidorowa
    Input Text  xpath=//*[@id="id_password2"]  pomidorowa
#    CLick Button  xpath=/html/body/div/section/form/button
#    BuiltIn.Sleep  2
#    Close Browser
