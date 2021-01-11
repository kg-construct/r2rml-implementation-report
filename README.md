# R2RML Implementation report

Test the capabilities of your R2RML engine with the [R2RML test cases](https://www.w3.org/2001/sw/rdb2rdf/test-cases/).
Use the resources provided in this repository to automatically generate an EARL report with your results.


## Requirements for running the implementation report:

- Linux based OS
- Docker and docker-compose
- Python
- Java

## RDBMS coverage:

- MySQL (port = 3306)
- PostgreSQL (port = 5432)

Connection properties for any RDBMS are: `database = r2rml, user = r2rml, password = r2rml`

## Steps to include your report:

1. Fork this repository.
2. Edit the file `info.csv` with the corresponding information of your engine.
	- Usually the URL of your EARL report would be: https://raw.githubusercontent.com/[YOUR-USER]/r2rml-implementation-report/main/test-cases/results.ttl
3. Pull request to the main repository with the updated information.
4. Clone the repository and copy the executable file (and other possible necessary files) of your engine to the test-cases folder.
5. Modify the test-cases/config.ini file with your information. Mapping path is always `test-cases/r2rml.ttl`.

Example of the config file:
```
[tester]
tester_name: David Chaves # tester name
tester_url: https://dchaves.oeg-upm.net/ # tester homepage
tester_contact: dchaves@fi.upm.es # tester contact

[engine]
test_date: 2021-01-07 # engine test-date 
engine_version: 3.12.5 # engine version
engine_name: Morph-RDB # engine name
engine_created: 2013-12-01 # engine date created (YYYY-MM-DD)
engine_url: https://morph.oeg.fi.upm.es/tool/morph-rdb # URL of the engine (e.g., GitHub repo)


[properties]
database_system: [mysql|postgresql]
output_results: ./output.ttl # path to the result files of your engine
output_format: ntriples # output format of the results from your engine
engine_command: java -jar morph-rdb.jar -p properties.properties # command to run your engine
```

6. Install the requirements of the script `python3 -m pip install -r requirements.txt`
7. Run the script `python3 test.py config.ini`
8. Your results will appear in `test-cases/results.ttl` in RDF and in `test-cases/results.csv` in CSV.

