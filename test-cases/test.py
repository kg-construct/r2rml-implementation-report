import os
import sys
import csv
from configparser import ConfigParser, ExtendedInterpolation

import psycopg2
from rdflib import Graph, RDF, Namespace, compare
import mysql.connector


def test(config, g):
    database_system = config["properties"]["database_system"]
    print("Deployment docker container for " + database_system + "...")

    if database_system == "mysql":
        os.system("docker-compose -f databases/docker-compose-mysql.yml stop")
        os.system("docker-compose -f databases/docker-compose-mysql.yml rm --force")
        os.system("docker-compose -f databases/docker-compose-mysql.yml up -d && sleep 30")
    elif database_system == "postgresql":
        os.system("docker-compose -f databases/docker-compose-postgresql.yml stop")
        os.system("docker-compose -f databases/docker-compose-postgresql.yml rm --force")
        os.system("docker-compose -f databases/docker-compose-postgresql.yml up -d && sleep 30")
    else:
        print("Database system declared in config file must be mysql or postgresql")
        return
    results = [["tester", "platform", "testid", "result"]]

    for database_uri, p, o in g.triples((None, RDF.type, RDB2RDFTEST.DataBase)):
        d_identifier = g.value(subject=database_uri, predicate=DCELEMENTS.identifier, object=None)
        d_title = g.value(subject=database_uri, predicate=DCELEMENTS.title, object=None)
        database = g.value(subject=database_uri, predicate=RDB2RDFTEST.sqlScriptFile, object=None)
        print("**************************************************************************")
        print("Using the database: " + d_identifier + " (" + d_title + ")")

        print("Loading in " + config["properties"]["database_system"] + " system the file:" + database)
        with open('databases/' + database) as f:
            contents = f.read()

        if database_system == "mysql":
            cnx = mysql.connector.connect(user='r2rml', password='r2rml', host='127.0.0.1', database='r2rml')
            cursor = cnx.cursor()
            cursor.execute(contents, multi=True)
            cnx.close()

        elif database_system == "postgresql":
            if "VARBINARY(200)" in contents:
                contents = contents.replace("VARBINARY(200)", "BYTEA").replace("X'", "'\\\\x")
            cnx = psycopg2.connect("dbname='r2rml' user='r2rml' host='localhost' password='r2rml'")
            cursor = cnx.cursor()
            cursor.execute(contents)
            cnx.commit()
            cnx.close()

        for test_uri, p, o in g.triples((None, RDB2RDFTEST.database, database_uri)):
            t_identifier = g.value(subject=test_uri, predicate=DCELEMENTS.identifier, object=None)
            t_title = g.value(subject=test_uri, predicate=DCELEMENTS.title, object=None)
            purpose = g.value(subject=test_uri, predicate=TESTDEC.purpose, object=None)
            expected_output = bool(g.value(subject=test_uri, predicate=RDB2RDFTEST.hasExpectedOutput, object=None))
            print("-----------------------------------------------------------------")
            print("Testing R2RML test-case: " + t_identifier + " (" + t_title + ")")
            print("Purpose of this test is: " + purpose)
            r2rml = g.value(subject=test_uri, predicate=RDB2RDFTEST.mappingDocument, object=None)
            os.system("cp " + t_identifier + "/" + r2rml + " r2rml.ttl")
            expected_output_graph = Graph()
            if expected_output:
                output = g.value(subject=test_uri, predicate=RDB2RDFTEST.output, object=None)
                expected_output_graph.parse("./" + t_identifier + "/" + output, format="nquads")

            os.system(config["properties"]["engine_command"])

            # if there is output file
            if os.path.isfile(config["properties"]["output_results"]):
                # and expected output is true
                if expected_output:
                    output_graph = Graph()
                    output_graph.parse(config["properties"]["output_results"],
                                       format=config["properties"]["output_format"])
                    # and graphs are equal
                    if compare.isomorphic(expected_output_graph, expected_output):
                        result = "passed"
                    # and graphs are distinct
                    else:
                        result = "failed"
                # and expected output is false
                else:
                    result = "failed"
            # if there is not output file
            else:
                # and expected output is true
                if expected_output:
                    result = "failed"
                # expected output is false
                else:
                    result = "passed"

            results.append([config["metadata"]["tester"], config["metadata"]["engine"], t_identifier, result])
            print(t_identifier + "," + result)

    os.system("rm r2rml.ttl")
    if database_system == "mysql":
        os.system("docker-compose -f databases/docker-compose-mysql.yml stop")
        os.system("docker-compose -f databases/docker-compose-mysql.yml rm --force")
    elif database_system == "postgresql":
        os.system("docker-compose -f databases/docker-compose-postgresql.yml stop")
        os.system("docker-compose -f databases/docker-compose-postgresql.yml rm --force")

    with open('results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(results)

    print("Generating the RDF results using EARL vocabulary")
    os.system("java -jar rmlmapper.jar -m mapping.rml.ttl -o results.ttl -d")
    os.system("rm metadata.csv")


if __name__ == "__main__":

    config_file = str(sys.argv[1])
    if not os.path.isfile(config_file):
        print("The configuration file " + config_file + " does not exist.")
        print("Aborting...")
        sys.exit(1)

    config = ConfigParser(interpolation=ExtendedInterpolation())
    config.read(config_file)

    g = Graph()
    g.parse("./manifest.ttl", format='turtle')
    RDB2RDFTEST = Namespace("http://purl.org/NET/rdb2rdf-test#")
    TESTDEC = Namespace("http://www.w3.org/2006/03/test-description#")
    DCELEMENTS = Namespace("http://purl.org/dc/elements/1.1/")

    metadata = [
        ["tester_name", "tester_url", "tester_contact", "test_date", "engine_version", "engine_name", "engine_created",
         "engine_url"],
        [config["tester"]["tester_name"], config["tester"]["tester_url"], config["tester"]["tester_contact"],
         config["engine"]["test_date"],
         config["engine"]["engine_version"], config["engine"]["engine_name"], config["engine"]["engine_created"],
         config["engine"]["engine_url"]]]

    with open('metadata.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(metadata)

    test(config, g)
