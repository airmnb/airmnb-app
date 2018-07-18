--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.8
-- Dumped by pg_dump version 9.6.8

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
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: gcheng
--

COPY public.users (user_id, account_name, password, source, email, phone, family_name, given_name, full_name, gender, dob, last_access_at, created_at, salt, language) FROM stdin;
87a8ee78-583f-4f13-9f64-3022e10f9cea	provider_1	\N	1	\N	\N	\N	\N	\N	\N	\N	\N	2018-06-05 20:34:37.935351+10	\N	\N
4dcc4d87-9a11-46fd-a9ce-5d05f332f63d	provider_2	\N	1	\N	\N	\N	\N	\N	\N	\N	\N	2018-06-05 20:34:37.935351+10	\N	\N
a7ee4770-b31a-4a68-b185-5c82938daeb5	consumer_3	\N	1	\N	\N	\N	\N	\N	\N	\N	\N	2018-06-05 20:34:37.935351+10	\N	\N
25ed5e56-9760-4a07-963a-a6e4e5a5fefb	consumer_4	\N	1	\N	\N	\N	\N	\N	\N	\N	\N	2018-06-05 20:34:37.935351+10	\N	\N
\.


--
-- PostgreSQL database dump complete
--

