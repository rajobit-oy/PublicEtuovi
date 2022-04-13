*** Settings ***
Library           Collections
Library           RPA.Browser.Selenium
Library           RPA.Robocorp.WorkItems    
Library           RPA.Tables
Library           Etuovi
Library           String
Library           pythonSheet
*** Tasks ***
Consume items
    
    [Documentation]    Login and then cycle through work items.
    ...    
    #Exception Handling    BUSINESS,sad sd    lisaa
    #Set Work Items    HelloLibrary    
    ${Login OK}=    Run Keyword And Return Status
    ...    Login
    IF    ${Login OK}
        Log    opened etuovi, starting to handle items
        For Each Input Work Item    Handle item
    ELSE
        ${error_message}=    Set Variable
        ...    Unable to go to Etuovi,please check it works.
        Log    ${error_message}    level=ERROR
        Release Input Work Item
        ...    state=FAILED
        ...    exception_type=APPLICATION
        ...    message=${error_message}
    END

*** Keywords ***

Exception Handling
    [Documentation]    sets item failed, also does logging and restarting browser
    ...    Tags: OwnException
    [Arguments]    ${output}    ${payload} 
    @{words}=    Split String    ${output}       ,

    ${error_message}=    Set Variable
    ...    Failed to handle item for: ${payload}.
    
    IF    """${words}[0]""" == "BUSINESS"
        ${et}    Set Variable    BUSINESS
        ${error_message}=    Set Variable
        ...    Failed to download PDF for: ${payload}.
        Log    ${error_message}    level=WARN
        
    ELSE
        ${et}    Set Variable    APPLICATION
        Log    ${error_message}    level=ERROR
    END
    ExceptionWorkItemLogging
    Release Input Work Item
    ...    state=FAILED
    ...    exception_type=${et}
    ...    message=${error_message}

    Exception Restart
    Log    logging in again, because we got error!
    Login
Login
    [Documentation]
    ...    Opens Etuvoi and navigates to search
    NavigateToSearch

Action for item
    [Documentation]
    ...    Handles one page of Etuovi
    [Arguments]    ${payload}
    Log    handling item: ${payload}
    Handle Page    ${payload}[href]

Handle item

    [Documentation]    Handles one item and also does error handling for the item
    
    ${payload}=    Get Work Item Payload
    ${Item Handled}    ${output}=    Run Keyword And Ignore Error
    ...    Action for item    ${payload}
  
    IF    "${Item Handled}" == "PASS"
        Log    ${payload} item handled succesfully!
        #Setting robotCompleted variable, to know that this item was really finished by robot.
        Set Work Item Variable    robotCompleted    True
        Save Work Item
        Release Input Work Item    DONE
    ELSE
        # Giving a good error message here means that data related errors can
        # be fixed faster in Control Room.
        Exception Handling      ${output}    ${payload}
    END
