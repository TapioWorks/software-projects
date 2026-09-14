*** Settings ***
Documentation    Reusable keywords for user management

*** Keywords ***
Start User Management Tests
    Log    Starting User Management Tests

Finish User Management Tests
    Log    Finished User Management Tests

Validate User
    [Arguments]    ${user}    ${expected_username}    ${expected_role}    ${expected_active}
    Log    Validating user: ${expected_username}
    Should Be Equal    ${user}[username]    ${expected_username}
    Should Be Equal    ${user}[role]    ${expected_role}
    Should Be Equal    ${user}[active]    ${expected_active}
