CREATE OR REPLACE FUNCTION qcserverless3.notify_interface()
RETURNS trigger
LANGUAGE plpgsql
AS $function$
DECLARE
    payload jsonb;
BEGIN
    -- Bangun payload JSON (tanpa logika key)
    payload := jsonb_build_object(
        'type', 'interface',
        'schema', TG_TABLE_SCHEMA,                  -- schema aktif tempat trigger berjalan
        'table', TG_TABLE_NAME,
        'action', TG_OP,                            -- 'INSERT' / 'UPDATE'
        'time', to_char(NOW(), 'YYYY-MM-DD HH24:MI:SS'),
        'key', NEW.key,                             -- tetap kirimkan nilainya ke payload
        'endpoint', COALESCE(NEW.zinr, ''),
        'parameter', COALESCE(NEW.parameters, ''),  -- tambahkan field singular "parameter"
        'action', NEW.action, -- tetap sertakan plural jika masih dibutuhkan
        'recid', NEW._recid
    );

    -- Kirim notifikasi ke channel utama
    PERFORM pg_notify('notify_channel', payload::text);

    RETURN NEW;
END;
$function$;


DROP TRIGGER IF EXISTS trg_notify_interface ON qcserverless3.interface;

CREATE TRIGGER trg_notify_interface
AFTER INSERT OR UPDATE ON qcserverless3.interface
FOR EACH ROW
WHEN (NEW.key = 76)
EXECUTE FUNCTION qcserverless3.notify_interface();
