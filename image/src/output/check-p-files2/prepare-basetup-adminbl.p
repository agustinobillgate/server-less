DEFINE TEMP-TABLE t-bk-setup LIKE bk-setup
    FIELD rec-id AS INT.

DEF OUTPUT PARAMETER TABLE FOR t-bk-setup.

FOR EACH bk-setup NO-LOCK BY bk-setup.setup-id:
    CREATE t-bk-setup.
    BUFFER-COPY bk-setup TO t-bk-setup.
    ASSIGN t-bk-setup.rec-id = RECID(bk-setup).
END.
