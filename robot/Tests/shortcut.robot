*** Settings ***
Library  SeleniumLibrary
Library  Dialogs

Resource  ../Resources/login.robot
Resource  ../Resources/rent.robot

*** Test Cases ***
Rent Prezentation
    Startt
    Normal loging  1  DS B1 Bydgoska  student1  pomidorowa
    Go to the vacum cleaner rent page
    Choose item to rent  2. odkurzacz
    Rent selected item
    pause execution
    Turn Back
    Exitt