
DEF TEMP-TABLE t-bediener LIKE bediener.

DEF OUTPUT PARAMETER TABLE FOR t-bediener.

FOR EACH bediener WHERE bediener.flag = 0 NO-LOCK BY bediener.username:
    CREATE t-bediener.
    BUFFER-COPY bediener TO t-bediener.
END.
