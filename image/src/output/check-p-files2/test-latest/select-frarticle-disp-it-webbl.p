
DEFINE TEMP-TABLE t-artikel
    FIELD artnr         AS INTEGER
    FIELD departement   AS INTEGER
    FIELD bezeich       AS CHARACTER
    FIELD activeflag    AS LOGICAL.

DEF INPUT  PARAMETER sorttype AS INT.
DEF INPUT  PARAMETER artart   AS INT.
DEF INPUT  PARAMETER f-dept   AS INT.
DEF OUTPUT PARAMETER artnr    AS INT INIT 0.
DEF OUTPUT PARAMETER TABLE FOR t-artikel.

RUN disp-it.

PROCEDURE disp-it: 
  IF artart = 0 THEN 
  DO: 
    IF sorttype = 1 THEN 
    FOR EACH artikel WHERE artikel.departement = f-dept 
        AND (artikel.artart = artart 
             OR (artikel.artart = 9 AND artikel.artgrp NE 0)) 
        NO-LOCK BY artikel.artnr:
        RUN create-it.
    END.
    ELSE 
    FOR EACH artikel WHERE artikel.departement = f-dept 
        AND (artikel.artart = artart 
             OR (artikel.artart = 9 AND artikel.artgrp NE 0)) 
        NO-LOCK BY artikel.bezeich:
        RUN create-it.
    END.
  END. 
  ELSE 
  DO: 
    IF sorttype = 1 THEN 
    FOR EACH artikel WHERE artikel.departement = f-dept 
        AND artikel.artart = artart
        NO-LOCK BY artikel.artnr:
        RUN create-it.
    END.
    ELSE 
    FOR EACH artikel WHERE artikel.departement = f-dept 
        AND artikel.artart = artart
        NO-LOCK BY artikel.bezeich:
        RUN create-it.
    END.
  END. 
  IF AVAILABLE artikel THEN artnr = artikel.artnr. 
END. 

PROCEDURE create-it:
    CREATE t-artikel.
    ASSIGN
    t-artikel.artnr         = artikel.artnr
    t-artikel.departement   = artikel.departement
    t-artikel.bezeich       = artikel.bezeich
    t-artikel.activeflag    = artikel.activeflag.
END.
