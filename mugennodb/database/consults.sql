SELECT
  title_english,
  release_date
FROM mangas
WHERE
  active_status = 'ongoing'
ORDER BY
  release_date DESC;

SELECT
  m.title_english AS manga_title,
  t.tag_name AS genre
FROM mangas AS m
JOIN manga_genres AS mg
  ON m.id = mg.manga_id
JOIN tags AS t
  ON mg.tag_id = t.id
WHERE
  t.tag_type = 'genre'
ORDER BY
  manga_title,
  genre;

SELECT
  u.user_name,
  u.email
FROM users AS u
LEFT JOIN read AS r
  ON u.id = r.user_id
WHERE
  r.user_id IS NULL;

SELECT
  u.user_name,
  COUNT(r.users_id) AS number_of_reviews,
  AVG(r.score) AS average_score
FROM users AS u
JOIN review AS r
  ON u.id = r.users_id
GROUP BY
  u.user_name
HAVING
  COUNT(r.users_id) > 1;

SELECT DISTINCT
  m.title_english
FROM mangas m
JOIN manga_genres mg
  ON m.id = mg.manga_id
WHERE
  mg.tag_id IN (
    SELECT
      mg2.tag_id
    FROM mangas m2
    JOIN manga_genres mg2
      ON m2.id = mg2.manga_id
    WHERE
      m2.title_english = 'Attack on Titan'
  )
  AND m.title_english != 'Attack on Titan';

SELECT
  m.title_english,
  c.ch_number,
  c.title,
  ROW_NUMBER() OVER (PARTITION BY m.id ORDER BY c.ch_number) AS chapter_rank_in_manga
FROM mangas m
JOIN chapters c
  ON m.id = c.manga_id;

WITH BrazilianUsers AS (
  SELECT
    u.id
  FROM users u
  JOIN countries c
    ON u.country_id = c.id
  WHERE
    c.locale_code = 'pt-BR'
)
SELECT
  m.title_english,
  u.user_name
FROM read r
JOIN mangas m
  ON r.manga_id = m.id
JOIN users u
  ON r.user_id = u.id
WHERE
  r.user_id IN (
    SELECT
      id
    FROM BrazilianUsers
  ) AND r.status = 'completed';

SELECT
  title_english AS title,
  'Manga' AS type
FROM mangas
UNION ALL
SELECT
  title,
  'Chapter' AS type
FROM chapters
ORDER BY
  type,
  title;

SELECT
  title_english,
  release_date,
  CASE
    WHEN EXTRACT(YEAR FROM release_date) < 2000
    THEN 'Classic (pre-2000)'
    WHEN EXTRACT(YEAR FROM release_date) BETWEEN 2000 AND 2009
    THEN '2000s'
    WHEN EXTRACT(YEAR FROM release_date) BETWEEN 2010 AND 2019
    THEN '2010s'
    ELSE 'Modern (2020+)'
  END AS release_era
FROM mangas
ORDER BY
  release_date;

SELECT
  manga_title,
  avg_score
FROM (
  SELECT
    m.title_english AS manga_title,
    AVG(r.score) AS avg_score
  FROM mangas m
  JOIN manga_reviews mr
    ON m.id = mr.manga_id
  JOIN review r
    ON mr.review_id = r.review_id
  GROUP BY
    m.title_english
) AS MangaScores
ORDER BY
  avg_score DESC
LIMIT 1;

SELECT
  m1.title_english AS source_manga,
  m2.title_english AS related_manga,
  rm.relationship_type
FROM related_mangas rm
JOIN mangas m1
  ON rm.source_manga_id = m1.id
JOIN mangas m2
  ON rm.related_manga_id = m2.id
WHERE
  rm.relationship_type = 'similar_genre'
  AND m1.active_status = 'ongoing'
  AND m2.active_status = 'ongoing';