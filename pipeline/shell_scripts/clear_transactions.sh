source .env
export PGPASSWORD=$DB_PASSWORD
psql -h $DB_HOST -p $DB_PORT -d $DB_NAME -U $DB_USERNAME -c "DELETE FROM kevin_schema.FACT_transactions;"

echo "Transaction data cleared successfully."
