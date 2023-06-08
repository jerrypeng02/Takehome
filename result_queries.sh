docker exec -it takehome_db psql -U postgres
\c takehomedb;
SELECT * FROM average_experiments;
SELECT * FROM most_commonly_experimented_compound;
SELECT * FROM total_experiments;