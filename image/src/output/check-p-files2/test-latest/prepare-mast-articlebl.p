DEFINE TEMP-TABLE t-artikel  LIKE artikel.
DEFINE TEMP-TABLE t-res-line LIKE res-line.
DEFINE TEMP-TABLE t-fixleist LIKE fixleist.
DEFINE TEMP-TABLE t-mast-art LIKE mast-art.
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

DEFINE INPUT PARAMETER resnr        AS INTEGER.
DEFINE INPUT PARAMETER new-res      AS LOGICAL.
DEFINE INPUT PARAMETER curr-dept    AS INTEGER INITIAL 0.
DEFINE OUTPUT PARAMETER TABLE FOR gart-list.
DEFINE OUTPUT PARAMETER TABLE FOR hart-list.

RUN read-mast-artbl.p (1, resnr, ?,?,?,?, OUTPUT TABLE t-mast-art).
FOR EACH t-mast-art NO-LOCK:
    RUN read-artikelbl.p(t-mast-art.artnr, t-mast-art.departement, "", OUTPUT TABLE t-artikel).
    FIND FIRST t-artikel NO-ERROR.
    CREATE gart-list. 
    ASSIGN
    gart-list.artnr       = t-artikel.artnr
    gart-list.bezeich     = t-artikel.bezeich 
    gart-list.departement = t-artikel.departement. 
END.
/*
FIND FIRST t-mast-art NO-ERROR.
DO WHILE AVAILABLE t-mast-art:
  RUN read-artikelbl.p(t-mast-art.artnr, 
    t-mast-art.departement, "", OUTPUT TABLE t-artikel).
  FIND FIRST t-artikel NO-ERROR.
  CREATE gart-list. 
  ASSIGN
    gart-list.artnr       = t-artikel.artnr
    gart-list.bezeich     = t-artikel.bezeich 
    gart-list.departement = t-artikel.departement
   . 
  FIND NEXT t-mast-art NO-ERROR.
END. 
*/
IF new-res THEN 
DO: 
    RUN read-res-linebl.p(4, resnr, ?,?,?,?,?,?,?,?,?,OUTPUT TABLE t-res-line).
    FOR EACH t-res-line NO-LOCK:
        RUN read-fixleistbl.p(1, resnr, t-res-line.reslinnr, 1,OUTPUT TABLE t-fixleist).
        FOR EACH t-fixleist NO-LOCK:
            FIND FIRST gart-list WHERE gart-list.artnr = t-fixleist.artnr AND gart-list.departement = t-fixleist.departement NO-ERROR. 
            IF NOT AVAILABLE gart-list THEN 
            DO: 
                RUN read-artikelbl.p(t-fixleist.artnr, t-fixleist.departement, "", OUTPUT TABLE t-artikel).
                FIND FIRST t-artikel NO-ERROR.
                CREATE gart-list.
                ASSIGN
                    gart-list.artnr       = t-artikel.artnr
                    gart-list.bezeich     = t-artikel.bezeich 
                    gart-list.departement = t-artikel.departement
                    . 
            END. 
        END.
    END.
  /*
  FIND FIRST t-res-line NO-ERROR.
  DO WHILE AVAILABLE t-res-line:
    RUN read-fixleistbl.p(1, resnr, t-res-line.reslinnr, 1,
      OUTPUT TABLE t-fixleist).
    FIND FIRST t-fixleist NO-ERROR.
    DO WHILE AVAILABLE t-fixleist:
      FIND FIRST gart-list WHERE gart-list.artnr = t-fixleist.artnr 
        AND gart-list.departement = t-fixleist.departement NO-ERROR. 
      IF NOT AVAILABLE gart-list THEN 
      DO: 
        RUN read-artikelbl.p(t-fixleist.artnr, 
          t-fixleist.departement, "", OUTPUT TABLE t-artikel).
        FIND FIRST t-artikel NO-ERROR.
        CREATE gart-list.
        ASSIGN
          gart-list.artnr       = t-artikel.artnr
          gart-list.bezeich     = t-artikel.bezeich 
          gart-list.departement = t-artikel.departement
        . 
      END. 
      FIND NEXT t-fixleist NO-ERROR.
    END.
    FIND NEXT t-res-line NO-ERROR.
  END.*/
    RUN write-mast-artbl.p(1, resnr, TABLE gart-list).
END. 

RUN create-list.

PROCEDURE create-list: 
    EMPTY TEMP-TABLE hart-list.
    RUN load-artikelbl.p(1, curr-dept, OUTPUT TABLE artikel-list,OUTPUT TABLE t-artikel).
    FOR EACH artikel-list WHERE (artikel-list.artart = 0 OR artikel-list.artart = 5) NO-LOCK:
        FIND FIRST gart-list WHERE gart-list.artnr = artikel-list.artnr AND gart-list.departement = artikel-list.departement NO-ERROR. 
        IF NOT AVAILABLE gart-list THEN 
        DO: 
            CREATE hart-list. 
            BUFFER-COPY artikel-list TO hart-list.
        END. 
    END.
    /*
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
  END. */
END.
