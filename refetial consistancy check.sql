#refetial consistancy

SELECT s.status_id, s.status_message_id
FROM nura.messages_with_statuses s
WHERE s.status_message_id IS NOT NULL
  AND s.status_message_id NOT IN (
      SELECT message_id FROM nura.messages_with_statuses
  );
