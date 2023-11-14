CREATE SEQUENCE cities_id_seq
    AS bigint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE SEQUENCE forecast_id_seq
    AS bigint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


create table public.cities (
    id bigint primary key not NULL DEFAULT nextval('cities_id_seq'),
    name character varying(255)
);

create table public.forecast (
    id bigint primary key not null default nextval('forecast_id_seq'::regclass),
    "cityId" bigint,
    "dateTime" bigint,
    temperature integer,
    summary text,
    foreign key ("cityId") references public.cities (id)
     match simple on update no action on delete cascade
);