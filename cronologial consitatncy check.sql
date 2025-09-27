#cronologial consitatncy

SELECT message_id, status, status_timestamp
FROM nura.messages_with_statuses
WHERE status_timestamp < message_inserted_at;
