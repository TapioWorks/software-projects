*** Settings ***
Documentation    Practice with different Robot Framework variable types
Variables    variables.py

Library    Collections

*** Test Cases ***
Validate User Variables
    Should Be Equal    ${USERNAME}    max
    Should Be Equal    ${PASSWORD}    secret123
    Should Be Equal    ${ROLE}    admin

Validate Allowed Roles
    List Should Contain Value    ${ALLOWED_ROLES}    admin
    List Should Contain Value    ${ALLOWED_ROLES}    user

Validate User Dictionary
    Should Be Equal    ${USER}[username]    max
    Should Be Equal    ${USER}[role]    admin
    Should Be Equal    ${USER}[active]    ${True}
