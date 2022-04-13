*** Settings ***
Library           Collections
Library           RPA.Excel.Files
Library           RPA.Tables
Library           Etuovi
Library           robocorpapi
#Library           RPA.Robocorp.WorkItems
Library           RPA.Cloud.Google
...               vault_name=GoogleSheets
...               vault_secret_key=service_account
#Library           pythonSheet
Suite Setup       Init Sheets    use_robocorp_vault=True

*** Variables ***
${SHEET_ID}       16wUrf8YvQ1KpIdwqXCHw7XqtBpUua7dHEYLO1_De6qA
${SHEET_RANGE}    2022!A:D

*** Keywords *** ***
Read values from the Google Sheet
    ${spreadsheet_content}=    Get Sheet Values
    ...    ${SHEET_ID}
    ...    ${SHEET_RANGE}
    IF    "values" in ${spreadsheet_content}
        Log Many    ${spreadsheet_content["values"]}
    END

Add values to the Google Sheet
    ${values}=    Evaluate    [["Mark", "The Monkey", 100000, 10000]]
    Insert Sheet Values
    ...    ${SHEET_ID}
    ...    ${SHEET_RANGE}
    ...    ${values}
    ...    ROWS


*** Tasks ***

Produce items
    [Documentation]
    ...    Navigates to Etuovi, gives wanted search parameters
    ...    Finds all Hrefs and creates worker items based on them
    Log    ${CURDIR}
    CreateWorkItems
