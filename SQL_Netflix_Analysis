
select count(*)
from [master].[dbo].[tNetflix_rawdata];
-- 8807 rows
select *
from [master].[dbo].[tNetflix_rawdata]
where show_id='s5023';
-- Movie title in foreign characters so set title to nvarchar type

-- Removing Duplicates
select show_id, count(*)
from [master].[dbo].[tNetflix_rawdata]
group by show_id
having count(*) > 1

-- As there are no duplicates- lets keep this column as primary key 
-- Drop the table and create table with approriate datatype and load the data

-- Create new table for director as it as multiple directors for a movie
select show_id, trim(value) as director
into [master].[dbo].tNetflix_Directors
from [master].[dbo].[tNetflix_rawdata]
cross apply string_split(director,',');

select *
from [master].[dbo].tNetflix_Directors;

-- New table for Country
select show_id, trim(value) as Country
into tNetflix_country
from tNetflix_rawdata
cross apply string_split(country,',');

select *
from tNetflix_country;

-- New table for cast
select show_id, trim(value) as cast
into tNetflix_cast
from tNetflix_rawdata
cross apply string_split(cast,',');

select *
from tNetflix_cast;

-- New table for listed_in - Genre
select show_id, trim(value) as listed_in
into tNetflix_genre
from tNetflix_rawdata
cross apply string_split(listed_in,',');

select *
from tNetflix_genre;


-- Checking duplicates on title
select *
from [master].[dbo].[tNetflix_rawdata]
where concat(title,type) in (
                select concat(title,type)
from [master].[dbo].[tNetflix_rawdata]
group by title,type
having count(*) > 1)
order by title;

-- Remove duplicate title
with
    cte
    as
    (
        select *, row_number() over(partition by title,type order by show_id) as rn
        from [master].[dbo].[tNetflix_rawdata]
    )

-- select * from cte where rn = 1;   -- 8804 rows

-- select only needed columns, remove columns those are in seperate tables(director,listed_in(genre),country,cast)

select show_id, type, title, cast(date_added as date) as date_added, release_year, rating,
    case when duration is null then rating else duration end as duration,
    description
into tNetflix
from cte
where rn=1;

-- New final cleaned data in a staging table - tNetflix
select *
from tNetflix;

-- Populate missing values in Country table whose value is NULL
insert into tNetflix_country
select show_id, mp.Country
from tNetflix_rawdata nr
    INNER JOIN
    (select director, country
    from tNetflix_country nc inner join tNetflix_Directors nd
        on nc.show_id = nd.show_id
    group by director,country) mp
    on nr.director = mp.director
where nr.country is NULL;

-- Populate missing values for duration

select *
from tNetflix_rawdata
where duration is NULL;

-- Update the cte to replace null duration with rating as duration is misplaced in rating field instead of duration field

/** Data Analysis **/
/** 1. For each director count the number of movies and tv shows created by them in seperate columns and who created both tv shows and movies **/
select nd.director,
    sum(case when n.type = 'Movie' then 1 else 0 end) as Movie,
    sum(case when n.type = 'TV Show' then 1 else 0 end) as TV_Shows,
    sum(case when n.type IN ('Movie','TV Show') then 1 else 0 end) as Both
from tNetflix n
    INNER JOIN tNetflix_Directors nd
    on n.show_id = nd.show_id
group by nd.director
order by nd.director;
-- 4988


/** Show count of movies and tv shows in seperate columns. 
Show only directors who done both movies and TV shows **/

select nd.director,
    count(case when n.type = 'Movie' then n.show_id end) as Movie,
    count(case when n.type = 'TV Show' then n.show_id end) as TV_Shows
from tNetflix n
    INNER JOIN tNetflix_Directors nd
    on n.show_id = nd.show_id
group by nd.director
having count(distinct n.type) > 1

/** Country with highest number of comedy movies **/
-- select * from tNetflix_genre;

select top 1
    nc.Country, count(distinct n.show_id) as no_of_movies
from tNetflix n
    INNER JOIN tNetflix_country nc
    on n.show_id = nc.show_id
    inner join tNetflix_genre ng
    on n.show_id = ng.show_id
where ng.listed_in = 'Comedies' and n.type = 'Movie'
group by nc.Country
order by count(n.show_id) desc;

/** For each year which director has max no of movies released (based on date added to netflix **/

-- select * from tNetflix;

with
    topDirEachYr
    as
    (
        select nd.director, year(n.date_added) as MovieYear, count(distinct n.show_id) as NoOfMovies,
            ROW_NUMBER() over(partition by year(n.date_added) order by count(distinct n.show_id) desc,nd.director) as rn,
            DENSE_RANK() over(partition by year(n.date_added) order by count(distinct n.show_id) desc ) as dr
        from tNetflix_Directors nd
            INNER JOIN tNetflix n
            on nd.show_id = n.show_id
        where n.type = 'Movie'
        group by director,year(n.date_added)
    )

-- Results of directors with tie in same year based on no of movies
-- select MovieYear,director,NoOfMovies from topDirEachYr where dr=1;

-- Results of directors with tie in same year but picking only one director based on lexi order of director name
select MovieYear, director, NoOfMovies
from topDirEachYr
where rn=1;


/** Average duration of movies in each genre **/

select listed_in as genre, avg(cast(substring(duration,1,len(duration)-3) as int)) as avg_duration
from tNetflix n
    inner join tNetflix_genre ng
    on n.show_id = ng.show_id
where type = 'movie'
group by listed_in;

-- you can also use replace()
select listed_in as genre, avg(cast(replace(duration,' min','') as int)) as avg_duration
from tNetflix n
    inner join tNetflix_genre ng
    on n.show_id = ng.show_id
where type = 'movie'
group by listed_in;

/** Find list of directors who have created both Horror and Comedy movies **/
/** Display Director name and no.of.Comedy and Horror movies directed by them **/
with
    cte1
    as
    (
        select distinct director,
            count(case when listed_in='Comedies' then 1 end ) as NoOfComedyMovies,
            count(case when listed_in='Horror movies' then 1 end ) as NoOfHorrorMovies
        from tNetflix n
            inner join tNetflix_genre ng
            on n.show_id = ng.show_id
                and n.type = 'movie'
                and ng.listed_in IN ('Comedies','Horror movies')
            inner join tNetflix_Directors nd
            on ng.show_id = nd.show_id
        group by director
    )
-- using having clause without cte also works with condition having count(distinct ng.listed_in) = 2

select *
from cte1
where NoOfComedyMovies >0 and NoOfHorrorMovies > 0;

/********************************************************************************************************************************************/