-- \c justus;
-- select message, sender_id, receiver_id
-- from messages
-- where sender_id = '3afc9e6e-99ed-4a70-9c6f-b1a1a4e7b725'
-- group by sender_id, receiver_id, message;

-- SELECT * from messages;


WITH recents as (SELECT sender_id, receiver_id, max(timestamp) as timestamp
                 from messages
                 where sender_id = '3afc9e6e-99ed-4a70-9c6f-b1a1a4e7b725'
                 group by receiver_id, sender_id)
SELECT  m.message, m.sender_id, m.receiver_id, m.timestamp FROM recents r
INNER JOIN messages m ON m.timestamp = r.timestamp And m.receiver_id = r.receiver_id;
