# R2RML Implementation report

Test the capabilities of your R2RML engine with the [R2RML test cases](https://www.w3.org/2001/sw/rdb2rdf/test-cases/). Use the resources provided in this repository to automatically generate an EARL report with your results. Following the configuration steps to include your results in the [R2RML implementation report ](https://kg-construct.github.io/r2rml-implementation-report/).

**IMPORTANT INFORMATION ABOUT THE R2RML IMPLEMENTATION REPORT:** 
- This repository does NOT include any engine report
- The implementation report follows a decentralized approach, developers only have to provide (via PR) a link to their EARL reports
- The support resources provided here (test-cases folder) to generate the reports can be: forked, downloaded or cloned but no PR with the report is needed
- Read carefully the documentation provided, and open an issue if you have any question or doubt.

## Requirements for running the implementation report:

- Linux based OS
- Docker and docker-compose
- Python
- Java

## RDBMS coverage and properties info:

- MySQL (`port = 3306`)
- PostgreSQL (`port = 5432`)

Connection properties for any RDBMS are: `database = r2rml, user = r2rml, password = r2rml`.

For testing purposes, **mapping path is invariable, it is always `test-cases/r2rml.ttl`**


## Steps to include your results in the R2RML implementation report website:

We follow a decentralized approach to query and obtain the results for the R2RML parsers that want to include their results in the R2RML implementation report website. More in detail, we use [Walder](https://github.com/KNowledgeOnWebScale/walder) to generate the website, querying the EARL reports provide by any R2RML-parser developer. The steps to include your results in the implementation report are:

1. Have an access point for your results (it could be a LDF server, RDF dump, SPARQL endpoint, etc.). As the reports are not very heavy, the easiest way to provide the results could be an RDF dump uploaded to GitHub repository (e.g., https://raw.githubusercontent.com/[YOUR-USER]/[YOUR-REPO]/main/test-cases/results.ttl). We explain how to generate the R2RML test-cases report in the next section.
2. Fork this repository.
3. Add the access point in the [WALDER config file](https://github.com/kg-construct/r2rml-implementation-report/blob/main/docs/config.yaml#L10).
4. Make a pull request to include the results in the website.

Overview of the configuration steps:
![Configuration setp](misc/config.png?raw=true "Configuration setp")


## Steps to generate the results from the R2RML test-cases:

1. Fork, clone or download this repository.
2. Include the test-cases in your development, you can:
	- Copy the complete test-cases folder into your engine repository (e.g., in a testing folder in the master branch or in a new testing branch).
	- Include the executable file(s) of your engine inside the test-cases folder.
3. Install the requirements of the script `python3 -m pip install -r test-cases/requirements.txt`
4. Modify the test-cases/config.ini file with your information. For configurating your engine, remember that the path of the **mapping file is always test-cases/r2rml.ttl**. For example:

```
[tester]
tester_name: David Chaves # tester name
tester_url: https://dchaves.oeg-upm.net/ # tester homepage
tester_contact: dchaves@fi.upm.es # tester contact

[engine]
test_date: 2021-01-07 # engine test-date (YYYY-MM-DD)
engine_version: 3.12.5 # engine version
engine_name: Morph-RDB # engine name
engine_created: 2013-12-01 # engine date created (YYYY-MM-DD)
engine_url: https://morph.oeg.fi.upm.es/tool/morph-rdb # URL of the engine (e.g., GitHub repo)


[properties]
database_system: [mysql|postgresql] # choose only one
output_results: ./output.ttl # path to the result graph of your engine
output_format: ntriples # output format of the results from your engine
engine_command: java -jar morph-rdb.jar -p properties.properties # command to run your engine
```

5. Run the script `python3 test.py config.ini`
6. Your results will appear in `test-cases/results.ttl` in RDF and in `test-cases/results.csv` in CSV.
7. Upload or update the obtained results the access point you have provided in the configuration step.
8. For each new version of your engine, repeat the process from step 4 to 7.


Overview of the testing steps:
![Testing setp](misc/test.png?raw=true "Testing setp")

