*** Settings ***
Documentation     Basic Robot Framework practice using variables and custom keywords

*** Variables ***
${USERNAME_1}       max
${PASSWORD_1}       secret123

${USERNAME_2}    alice
${PASSWORD_2}    password456

*** Test Cases ***
User Registration Validation
    Validate Registration    ${USERNAME_1}    ${PASSWORD_1}    ${USERNAME_1}    ${PASSWORD_1}

    Validate Registration    ${USERNAME_2}    ${PASSWORD_2}    ${USERNAME_2}    ${PASSWORD_2}

*** Keywords ***
Validate Registration
    [Arguments]    ${username}    ${password}    ${expected_username}    ${expected_password}
    Should Be Equal    ${username}    ${expected_username}
    Should Be Equal    ${password}    ${expected_password}