-- Insert an event, after databse and tables (schema.sql) were created
INSERT INTO events
(public_id, slug, name, type, created_at)
VALUES
(
    'insert-public-id',
    'insert-slug',
    'insert-name',
    'website-guestbook',
    NOW()
);