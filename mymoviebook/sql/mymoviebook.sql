--
-- PostgreSQL database dump
--

-- Dumped from database version 11.1
-- Dumped by pg_dump version 11.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: lo_readall(oid); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.lo_readall(oid) RETURNS bytea
    LANGUAGE sql STRICT
    AS $_$

SELECT loread(q3.fd, q3.filesize + q3.must_exec) FROM
	(SELECT q2.fd, q2.filesize, lo_lseek(q2.fd, 0, 0) AS must_exec FROM
		(SELECT q1.fd, lo_lseek(q1.fd, 0, 2) AS filesize FROM
			(SELECT lo_open($1, 262144) AS fd)
		AS q1)
	AS q2)
AS q3

$_$;


ALTER FUNCTION public.lo_readall(oid) OWNER TO postgres;

--
-- Name: covers_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.covers_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.covers_seq OWNER TO postgres;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: covers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.covers (
    id integer DEFAULT nextval('public.covers_seq'::regclass) NOT NULL,
    films_id integer,
    cover bytea
);


ALTER TABLE public.covers OWNER TO postgres;

--
-- Name: films; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.films (
    id_films integer DEFAULT nextval(('"films_seq"'::text)::regclass) NOT NULL,
    savedate date,
    name text,
    id_dvd integer
);


ALTER TABLE public.films OWNER TO postgres;

--
-- Name: films_duplicated; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.films_duplicated AS
 SELECT upper(films.name) AS upper,
    count(*) AS count
   FROM public.films
  GROUP BY (upper(films.name))
 HAVING (count(*) > 1);


ALTER TABLE public.films_duplicated OWNER TO postgres;

--
-- Name: VIEW films_duplicated; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON VIEW public.films_duplicated IS 'Show films duplicated and count them';


--
-- Name: films_id_duplicated; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.films_id_duplicated AS
 SELECT films.id_dvd,
    upper(films.name) AS upper
   FROM public.films,
    ( SELECT upper(films_1.name) AS name,
            count(*) AS count
           FROM public.films films_1
          GROUP BY (upper(films_1.name))
         HAVING (count(*) > 1)) k
  WHERE (upper(films.name) = upper(k.name));


ALTER TABLE public.films_id_duplicated OWNER TO postgres;

--
-- Name: VIEW films_id_duplicated; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON VIEW public.films_id_duplicated IS 'Shows films duplicated with id_dvd';


--
-- Name: films_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.films_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.films_seq OWNER TO postgres;

--
-- Name: globals; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.globals (
    id integer NOT NULL,
    global text,
    value text
);


ALTER TABLE public.globals OWNER TO postgres;

--
-- Name: covers covers_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.covers
    ADD CONSTRAINT covers_pk PRIMARY KEY (id);


--
-- Name: films films_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.films
    ADD CONSTRAINT films_pk PRIMARY KEY (id_films);


--
-- Name: globals pk_globals; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.globals
    ADD CONSTRAINT pk_globals PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 11.1
-- Dumped by pg_dump version 11.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: globals; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.globals VALUES (1, 'Version', '201901030929');


--
-- PostgreSQL database dump complete
--

ALTER SEQUENCE public.covers_seq START WITH 1 RESTART;
ALTER SEQUENCE public.films_seq START WITH 1 RESTART;
