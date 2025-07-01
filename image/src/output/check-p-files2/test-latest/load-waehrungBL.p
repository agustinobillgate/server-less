DEF TEMP-TABLE t-waehrung LIKE waehrung.
DEF OUTPUT PARAMETER TABLE FOR t-waehrung.
FOR EACH waehrung NO-LOCK:
    CREATE t-waehrung.
    BUFFER-COPY waehrung TO t-waehrung.
END.
