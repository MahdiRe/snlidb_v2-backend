# snlidb_v2-backend

This is the prototype of the research project, 'Modifying the SNLIDB' that allows the users to access the database using Sinhala natural language.
SNLIDB refers to Sinhala Natural Language Interface to Database.

This project contains 8 APIs. Only 2 APIs are perform core functionality and they are discussed below.

1) /query/generate (POST) - To convert Sinhala natural query to SQL
2) /query/execute (POST) - To execute SQL query

This system is able to generate SQL queries such as.
* SELECT, UPDATE, DELETE, INSERT
* Support conditions

We use Sinling library (https://github.com/ysenarath/sinling) for the syntax analysis purposes.

The UI for this project is available in: https://github.com/MahdiRe/snlidb_v2-ui
An explainantion video for this project: https://youtu.be/WvUnArGED3I

Some useful files are added such as,
* SNLIDB_v2 APIs.xlsx - Provide all API informations of this project
* SNLIDB_v2 test cases.xlsx - Provide 173 hand-annotated possible Sinhala natural language queries (with tested outputs)
* SNLIDB_v2.sql - Database sample records for testing purpose
* SNLIDB_v2.postman_collection.json - Postman collection of this project
* Implementation guide.pptx - Step by step implementation guide

Thank you!
