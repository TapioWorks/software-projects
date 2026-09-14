*** Settings ***
Documentation    Practice with Robot Framework resource files
Resource    common.resource


*** Test Cases ***
Create And Validate User
    Create User    max    secret123
    Validate User    max    max

Validate Active User
    Validate User Is Active    ${True}
