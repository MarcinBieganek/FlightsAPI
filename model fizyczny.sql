
-- create table for flight segment's information
CREATE TABLE IF NOT EXISTS Flight_segment (
    flight_id integer NOT NULL,
    segment_number integer NOT NULL,
    takeoff_time timestamp with time zone NOT NULL,
    landing_time timestamp with time zone NOT NULL,
    takeoff_airport varchar(3) REFERENCES Airport (iatacode) NOT NULL,
    landing_airport varchar(3) REFERENCES Airport (iatacode) NOT NULL,
    route geography(LINESTRING) NOT NULL,
    CONSTRAINT FlightSegmKey PRIMARY KEY (flight_id, segment_number)
);

-- create index for routes
CREATE INDEX ON Flight_segment USING Gist (route);