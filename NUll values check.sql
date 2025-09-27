#null values
SELECT *
FROM nura.messages_with_statuses
WHERE content IS NULL 
   OR masked_author IS NULL 
   OR status IS NULL;
