DEFINE TEMP-TABLE t-artikel LIKE artikel.
DEFINE TEMP-TABLE artikel-list
    FIELD artnr       LIKE artikel.artnr
    FIELD departement LIKE artikel.departement
    FIELD bezeich     LIKE artikel.bezeich
    FIELD artart      LIKE artikel.artart.
DEFINE TEMP-TABLE hart-list
    FIELD artnr       LIKE artikel.artnr
    FIELD departement LIKE artikel.departement
    FIELD bezeich     LIKE artikel.bezeich
    FIELD artart      LIKE artikel.artart.
DEFINE TEMP-TABLE gart-list
    FIELD artnr       LIKE artikel.artnr
    FIELD departement LIKE artikel.departement
    FIELD bezeich     LIKE artikel.bezeich
    FIELD artart      LIKE artikel.artart.

DEFINE INPUT PARAMETER curr-dept    AS INTEGER INITIAL 0.
DEFINE OUTPUT PARAMETER TABLE FOR hart-list.

RUN create-list.

PROCEDURE create-list: 
  FOR EACH hart-list: 
    DELETE hart-list. 
  END.
  RUN load-artikelbl.p(1, curr-dept, OUTPUT TABLE artikel-list,
      OUTPUT TABLE t-artikel).
  FIND FIRST artikel-list WHERE (artikel-list.artart = 0
    OR artikel-list.artart = 5) NO-ERROR.
  DO WHILE AVAILABLE artikel-list:
    FIND FIRST gart-list WHERE gart-list.artnr = artikel-list.artnr 
      AND gart-list.departement = artikel-list.departement NO-ERROR. 
    IF NOT AVAILABLE gart-list THEN 
    DO: 
      CREATE hart-list. 
      BUFFER-COPY artikel-list TO hart-list.
    END. 
    FIND NEXT artikel-list WHERE (artikel-list.artart = 0
      OR artikel-list.artart = 5) NO-ERROR.
  END. 
END.
