*** Settings ***
Library  SeleniumLibrary
Library  Dialogs

Resource  ../Resources/login.robot
Resource  ../Resources/rentt.robot

*** Test Cases ***
Rent Prezentation
    Startt
    Normal loging  1  DS B1 Bydgoska  student1  pomidorowa
    pause execution
    Go to the vacum cleaner rent page
    pause execution
    Choose item to rent  2. odkurzacz
    pause execution
    Rent selected item
    pause execution
    Turn Back
    pause execution
    Exitt