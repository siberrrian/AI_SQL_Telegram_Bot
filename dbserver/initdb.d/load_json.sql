SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

CREATE TABLE public.video_snapshots (
    id uuid CONSTRAINT snapshots_id_not_null NOT NULL,
    video_id uuid,
    views_count integer,
    likes_count integer,
    reports_count integer,
    comments_count integer,
    delta_views_count integer,
    delta_likes_count integer,
    delta_reports_count integer,
    delta_comments_count integer,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

ALTER TABLE public.video_snapshots OWNER TO postgres;

CREATE TABLE public.videos (
    id uuid NOT NULL,
    video_created_at timestamp with time zone,
    views_count integer,
    likes_count integer,
    reports_count integer,
    comments_count integer,
    creator_id uuid,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

ALTER TABLE public.videos OWNER TO postgres;
ALTER TABLE ONLY public.video_snapshots ADD CONSTRAINT snapshots_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.videos ADD CONSTRAINT videos_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.video_snapshots ADD CONSTRAINT snapshots_video_id_fkey FOREIGN KEY (video_id) REFERENCES public.videos(id);

CREATE TABLE public.raw_json_data (doc jsonb);

COPY public.raw_json_data(doc) FROM '/dbserver/videos2.json' WITH (FORMAT text); 

INSERT INTO public.videos
SELECT jt.* FROM public.raw_json_data,
JSON_TABLE(doc, '$.videos[*]'
    COLUMNS (
        id UUID PATH '$.id',
        video_created_at TIMESTAMPTZ PATH '$.video_created_at',
        views_count INT PATH '$.views_count',
        likes_count INT PATH '$.likes_count',
        reports_count INT PATH '$.reports_count',
        comments_count INT PATH '$.comments_count',
        creator_id UUID PATH '$.creator_id',
        created_at TIMESTAMPTZ PATH '$.created_at',
        updated_at TIMESTAMPTZ PATH '$.updated_at'
    )
) AS jt;

INSERT INTO public.video_snapshots
SELECT jt.* FROM public.raw_json_data,
JSON_TABLE(doc, '$.videos[*].snapshots[*]'
    COLUMNS (
        id UUID PATH '$.id',
        video_id UUID PATH '$.video_id',
        views_count INT PATH '$.views_count',
        likes_count INT PATH '$.likes_count',
        reports_count INT PATH '$.reports_count',
        comments_count INT PATH '$.comments_count',
        delta_views_count INT PATH '$.delta_views_count',
        delta_likes_count INT PATH '$.delta_likes_count',
        delta_reports_count INT PATH '$.delta_reports_count',
        delta_comments_count INT PATH '$.delta_comments_count',
        created_at TIMESTAMPTZ PATH '$.created_at',
        updated_at TIMESTAMPTZ PATH '$.updated_at'
    )
) AS jt;

