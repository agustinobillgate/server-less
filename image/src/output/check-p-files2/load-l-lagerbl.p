DEF TEMP-TABLE t-l-lager LIKE l-lager.

DEF OUTPUT PARAMETER TABLE  FOR t-l-lager.
FOR EACH l-lager NO-LOCK:
    CREATE t-l-lager.
    BUFFER-COPY l-lager TO t-l-lager.
END.
