*** Settings ***
Library  SeleniumLibrary
Library  Dialogs

Resource  ../../Resources/login.robot
Resource  ../../Resources/rentt.robot

*** Test Cases ***
Rent
    Startt
    Normal loging  1  DS B1 Bydgoska  student1  pomidorowa
    Go to the vacum cleaner rent page
    Choose item to rent  2. odkurzacz
    Rent selected item
    Turn Back
    Exitt

When second user already renting then first user should be able rent this same kind thing
    Startt
    First User rent something
    Log out
    Normal loging  1  DS B1 Bydgoska  tkacza  pomidorowa
    Go to the vacum cleaner rent page
    Page Should Contain Element  xpath=/html/body/div[2]/form/button
    Log out
    Normal loging  1  DS B1 Bydgoska  student1  pomidorowa
    Go to the vacum cleaner rent page
    Turn Back
    Exitt

When second user already renting and first already reting somethink diffrent then first user should be able rent this same kind thing
    Startt
    First User rent something
    Log out

    Normal loging  1  DS B1 Bydgoska  tkacza  pomidorowa
    Go to the dryer rent page
    Rent drayer
    Go Back

    Go to the vacum cleaner rent page
    Page Should Contain Element  xpath=/html/body/div[2]/form/button
    Go Back
    Go to the dryer rent page
    Turn Back
    Log out

    Normal loging  1  DS B1 Bydgoska  student1  pomidorowa
    Go to the vacum cleaner rent page
    Turn Back
    Exitt


*** keywords ***
Go to the dryer rent page
    Click Button  xpath=/html/body/section/div/div/div[5]/form/button

Rent drayer
    Choose item to rent  1. suszarka
    Rent selected item

First User rent something
    Normal loging  1  DS B1 Bydgoska  student1  pomidorowa
    Go to the vacum cleaner rent page
    Choose item to rent  2. odkurzacz
    Rent selected item