*** Settings ***
Documentation    Practice with keyword return values

*** Variables ***
${USERNAME}    max
${PASSWORD}    secret123

*** Test Cases ***
User Registration
    ${registered_user}=    Register User    ${USERNAME}    ${PASSWORD}
    Should Be Equal    ${registered_user}    ${USERNAME}

*** Keywords ***
Register User
    [Arguments]    ${username}    ${password}
    Log    Registering user: ${username}
    RETURN    ${username}