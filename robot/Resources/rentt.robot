*** Keywords ***
Go to the vacum cleaner rent page
    Click button  xpath=/html/body/section/div/div/div[4]/form/button
    Wait Until Element Is Visible  xpath=/html/body/h2

Choose item to rent
    [Arguments]  ${number with item name}
    Select From List By Label  xpath=//*[@id="id_items"]  ${number with item name}

Rent selected item
    Click button  xpath=/html/body/div[2]/form/button
    Wait Until Element Is Visible  xpath=/html/body/h2

Turn Back
    Click button  xpath=/html/body/div[2]/form/button
    Page Should Contain Element  xpath=//*[@id="id_items"]
    Page Should Contain Element  xpath=/html/body/div[2]/form/button

