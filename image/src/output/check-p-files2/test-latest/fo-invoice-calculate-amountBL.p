
DEF TEMP-TABLE t-exrate LIKE exrate.
DEF TEMP-TABLE t-waehrung LIKE waehrung.

DEF INPUT PARAMETER transdate    AS DATE.
DEF INPUT PARAMETER a-betriebsnr AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-exrate.
DEF OUTPUT PARAMETER TABLE FOR t-waehrung.

FOR EACH exrate WHERE exrate.artnr = a-betriebsnr 
    AND exrate.datum = transdate NO-LOCK:
    CREATE t-exrate.
    BUFFER-COPY exrate TO t-exrate.
END.

FOR EACH waehrung WHERE waehrung.waehrungsnr = a-betriebsnr
    AND waehrung.ankauf NE 0 NO-LOCK:
    CREATE t-waehrung.
    BUFFER-COPY waehrung TO t-waehrung.
END.
