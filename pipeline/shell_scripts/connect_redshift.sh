source .env
export PGPASSWORD=$DB_PASSWORD
psql -h $DB_HOST -p $DB_PORT -d $DB_NAME -U $DB_USERNAME -f ../schema.sql


# psql -h c9-rs-truck-cluster.cdq12ms5gjyk.eu-west-2.redshift.amazonaws.com -p 5439 -d truck -U kevin 
# why does running this display not relations, until I import manually?
# why isn't truck_id resetting? It's been continuing thw whole time!


