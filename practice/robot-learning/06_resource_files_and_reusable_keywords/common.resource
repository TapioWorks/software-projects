*** Settings ***
Documentation    Reusable keywords for user-related tests

*** Keywords ***
Create User
    [Arguments]    ${username}    ${password}
    Log    Creating user: ${username}
    Log    Password provided: ${password}

Validate User
    [Arguments]    ${username}    ${expected_username}
    Should Be Equal    ${username}    ${expected_username}

Validate User Is Active
    [Arguments]    ${active}
    Should Be True    ${active}
