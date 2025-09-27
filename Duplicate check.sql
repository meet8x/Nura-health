SELECT 
    ANY_VALUE(mws.message_id) AS message_id,  -- pick any message_id from the group
    mws.content,
    DATE_FORMAT(mws.message_inserted_at, '%Y-%m-%d %H:%i') AS minute_bucket,
    COUNT(*) AS duplicate_count
FROM nura.messages_with_statuses mws
GROUP BY mws.content, minute_bucket
HAVING COUNT(*) > 1;
