import json
import sys
import psycopg2
import psycopg2.extras

conn = psycopg2.connect("dbname=marcin user=marcin password=qwerty host=/var/run/postgresql port=5433")

def check_format(json_request):
    if ("function" not in json_request) or ("params" not in json_request):
        return False
    if (not isinstance(json_request["function"], str)) or (not isinstance(json_request["params"], dict)):
        return False
    return True

def prepare_response(status, data=None):
    if data is None:
        response = {
            "status": status
        }
    else:
        response = {
            "status": status,
            "data": data
        }
    return response

def check_if_init():
    if len(sys.argv) != 2:
        return False
    if sys.argv[1] != "--init":
        return False
    return True

def init():
    try:
        with conn:
            with conn.cursor() as curs:
                curs.execute(open("model fizyczny.sql", "r").read())
    except:
        return prepare_response("ERROR")
    return prepare_response("OK")

# add new flight to the database
def flight(params):
    values = []
    for i in range(len(params["airports"]) - 1):
        curr_airport = params["airports"][i]
        next_airport = params["airports"][i+1]
        values.append((params["id"], 
                        i, 
                        curr_airport["takeoff_time"], 
                        next_airport["landing_time"], 
                        curr_airport["airport"],
                        next_airport["airport"],
                        curr_airport["airport"],
                        next_airport["airport"]))
    try:
        with conn:
            with conn.cursor() as curs:
                psycopg2.extras.execute_batch(curs, 
                                            """INSERT INTO Flight_segment 
                                               VALUES (%s, %s, %s, %s, %s, %s,
                                                    (ST_MakeLine(
                                                        (SELECT ST_MakePoint(a.longitude, a.latitude)
                                                            FROM Airport a
                                                            WHERE a.iatacode = %s), 
                                                        (SELECT ST_MakePoint(a.longitude, a.latitude)
                                                            FROM Airport a
                                                            WHERE a.iatacode = %s))));""",
                                            values)
    except:
        return prepare_response("ERROR")
    return prepare_response("OK")

# search for flight segments with intersecting routes
# with route of given flight
def list_flights(params):
    try:
        with conn:
            with conn.cursor() as curs:
                curs.execute("""WITH POM AS
                                (SELECT *
                                    FROM Flight_segment f
                                    WHERE f.flight_id = %s
                                    ORDER BY f.segment_number)
                                SELECT f.flight_id, f.takeoff_airport, f.landing_airport, f.takeoff_time
                                FROM Flight_segment f
                                    JOIN POM ON f.flight_id <> POM.flight_id
                                    WHERE ST_Distance(f.route, POM.route) = 0.0
                                    ORDER BY f.takeoff_time DESC, f.flight_id ASC;""",
                            (params["id"],))
                res_data = []
                for record in curs:
                    result_dict = {
                        "rid": str(record[0]),
                        "from": record[1],
                        "to": record[2],
                        "takeoff_time": str(record[3])
                    }
                    res_data.append(result_dict)
    except:
        return prepare_response("ERROR")
    return prepare_response("OK", data=res_data)

# search for cities located closer than given distance
# from given flight route
def list_cities(params):
    try:
        with conn:
            with conn.cursor() as curs:
                curs.execute("""WITH Flight AS
                                (SELECT *
                                    FROM Flight_segment f
                                    WHERE f.flight_id = %s)
                                SELECT DISTINCT c.name, c.province, c.country
                                FROM City c
                                    JOIN Flight f ON ((ST_Distance(f.route, (ST_MakePoint(c.longitude, c.latitude))::geography) / 1000) < %s)
                                ORDER BY c.name;""",
                            (params["id"], params["dist"]))
                res_data = []
                for record in curs:
                    result_dict = {
                        "name": record[0],
                        "prov": record[1],
                        "country": record[2]
                    }
                    res_data.append(result_dict)
    except:
        return prepare_response("ERROR")
    return prepare_response("OK", data=res_data)

# search for last n flight that takeoff from given airport
def list_airport(params):
    try:
        with conn:
            with conn.cursor() as curs:
                curs.execute("""SELECT f.flight_id
                                FROM Flight_segment f
                                WHERE f.takeoff_airport = %s
                                ORDER BY f.takeoff_time DESC, f.flight_id ASC
                                LIMIT %s;""",
                            (params["iatacode"], params["n"]))
                res_data = []
                for record in curs:
                    result_dict = {
                        "id": str(record[0])
                    }
                    res_data.append(result_dict)
    except:
        return prepare_response("ERROR")
    return prepare_response("OK", data=res_data)

# search for last n flights near given city
def list_city(params):
    try:
        with conn:
            with conn.cursor() as curs:
                print(params)
                curs.execute("""WITH Given_city AS
                                (SELECT *
                                    FROM City c
                                    WHERE c.name = %s AND c.province = %s AND c.country = %s),
                                Flight_segment_close AS
                                (SELECT f.*, round(ST_Distance(f.route, (ST_MakePoint(c.longitude, c.latitude))::geography) / 1000) AS mdist
                                    FROM Flight_segment f
                                    JOIN Given_city c ON ((ST_Distance(f.route, (ST_MakePoint(c.longitude, c.latitude))::geography) / 1000) < %s)),
                                Flight_mindist AS
                                (SELECT f.flight_id, MIN(f.mdist) AS mdist
                                        FROM Flight_segment_close f
                                        GROUP BY f.flight_id)
                                SELECT f.flight_id, f.mdist
                                FROM Flight_segment_close f
                                    JOIN Flight_mindist fmin ON (fmin.flight_id = f.flight_id)
                                WHERE f.mdist = fmin.mdist
                                ORDER BY f.takeoff_time DESC, f.flight_id ASC
                                LIMIT %s;""",
                            (params["name"], params["prov"], params["country"], params["dist"], params["n"]))
                res_data = []
                for record in curs:
                    result_dict = {
                        "rid": str(record[0]),
                        "mdist": str(record[1])
                    }
                    res_data.append(result_dict)
    except:
        return prepare_response("ERROR")
    return prepare_response("OK", data=res_data)

if check_if_init():
    response = init()
    print(json.dumps(response))
else:
    while True:
        try:
            json_string = input()
            if json_string == "":
                break
            json_request = json.loads(json_string)
            if json_request["function"] == "flight":
                response = flight(json_request["params"])
            elif json_request["function"] == "list_flights":
                response = list_flights(json_request["params"])
            elif json_request["function"] == "list_cities":
                response = list_cities(json_request["params"])
            elif json_request["function"] == "list_airport":
                response = list_airport(json_request["params"])
            elif json_request["function"] == "list_city":
                response = list_city(json_request["params"])
            else:
                response = prepare_response("ERROR")
            print(json.dumps(response, indent=4, ensure_ascii=False))
        except EOFError:
            break

conn.close()