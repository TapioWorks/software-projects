*** Settings ***
Documentation    Practice with Robot Framework libraries

Library    Collections
Library    String

*** Test Cases ***
User Data Validation
    ${users}=    Create List    max    alice    bob
    List Should Contain Value    ${users}    alice
    List Should Contain Value    ${users}    bob

    ${uppercase_username}=    Convert To Upper Case    max
    Should Be Equal    ${uppercase_username}    MAX