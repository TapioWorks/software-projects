*** Settings ***
Documentation    Practice with resource files and reusable keywords

Library    Collections
Resource    common.resource
Variables    variables.py

Suite Setup       Start User Management Tests
Suite Teardown    Finish User Management Tests

*** Test Cases ***
Verify All Users Exist
    List Should Contain Value    ${USERS}    max
    List Should Contain Value    ${USERS}    alice
    List Should Contain Value    ${USERS}    bob

Check All Users
    FOR    ${user}    IN    @{USERS}
        Log    Checking user: ${user}
        Should Not Be Empty    ${user}
    END

Validate Max
    Validate User    ${MAX}    max    admin    ${True}

Validate Alice
    Validate User    ${ALICE}    alice    user    ${True}

Validate Bob
    Validate User    ${BOB}    bob    user    ${False}
