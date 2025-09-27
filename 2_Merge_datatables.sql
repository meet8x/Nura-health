CREATE TABLE nura.messages_with_statuses AS
SELECT 
    m.id                AS message_id,
    m.message_type,
    m.masked_addressees,
    m.masked_author,
    m.content,
    m.author_type,
    m.direction,
    m.external_id,
    m.external_timestamp,
    m.masked_from_addr,
    m.is_deleted,
    m.last_status,
    m.last_status_timestamp,
    m.rendered_content,
    m.source_type,
    m.uuid              AS message_uuid,
    m.inserted_at       AS message_inserted_at,
    m.updated_at        AS message_updated_at,

    s.id                AS status_id,
    s.status,
    s.timestamp         AS status_timestamp,
    s.uuid              AS status_uuid,
    s.message_uuid      AS status_message_uuid,
    s.message_id        AS status_message_id,
    s.number_id,
    s.inserted_at       AS status_inserted_at,
    s.updated_at        AS status_updated_at

FROM nura.messages m
LEFT JOIN nura.statuses s
    ON m.id = s.message_id;
