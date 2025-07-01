DEF TEMP-TABLE t-artikel LIKE artikel.

DEF INPUT  PARAMETER case-type  AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER artNo      AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER dept       AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER aName      AS CHAR     NO-UNDO.
DEF INPUT  PARAMETER artart     AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER betriebsNo AS INTEGER  NO-UNDO.
DEF INPUT  PARAMETER actFlag    AS LOGICAL  NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR t-artikel.

CASE case-type :
    WHEN 1 THEN
    DO:
        IF artNo NE 0 THEN
            FIND FIRST artikel WHERE artikel.artnr = artNo 
            AND artikel.departement = dept NO-LOCK NO-ERROR.
        ELSE IF aName NE "" THEN
            FIND FIRST artikel WHERE artikel.bezeich = aName 
            AND artikel.departement = dept NO-LOCK NO-ERROR.
        IF AVAILABLE artikel THEN RUN cr-artikel.
    END.
    WHEN 2 THEN
    DO:
        FIND FIRST artikel WHERE artikel.artnr = artNo 
            AND artikel.departement = dept 
            AND artikel.artart = artart NO-LOCK NO-ERROR.
        IF AVAILABLE artikel THEN RUN cr-artikel.
    END.
    WHEN 3 THEN
    DO:
        FIND FIRST artikel WHERE artikel.artnr = artNo 
            AND artikel.departement = dept 
            AND artikel.activeFlag = actFlag NO-LOCK NO-ERROR.
        IF NOT AVAILABLE artikel THEN
        FIND FIRST artikel WHERE artikel.artnr = artNo 
            AND artikel.departement = 0 
            AND (artikel.artart = 2 OR artikel.artart = 6
              OR artikel.artart = 7)
            AND artikel.activeFlag NO-LOCK NO-ERROR.
        IF AVAILABLE artikel THEN RUN cr-artikel.
    END.
    WHEN 4 THEN
    DO:
        FIND FIRST artikel WHERE artikel.artnr = artNo 
            AND artikel.departement = dept 
            AND artikel.betriebsnr = betriebsNo NO-LOCK NO-ERROR.
        IF AVAILABLE artikel THEN RUN cr-artikel.
    END.
    WHEN 5 THEN
    DO:
        FOR EACH artikel WHERE artikel.departement = dept 
            AND (artikel.artart = 0 OR artikel.artart = 8 OR artikel.artart = 9) 
            AND artikel.activeflag = actFlag NO-LOCK :
            RUN cr-artikel.
        END.
    END.
    WHEN 6 THEN
    DO:
         FOR EACH artikel WHERE artikel.departement = 0 
             AND (artikel.artart = 2 OR artikel.artart = 5 
                  OR artikel.artart = 6 OR artikel.artart = 7) 
             AND artikel.activeflag = actFlag NO-LOCK:
             RUN cr-artikel.
         END.
    END.
    WHEN 7 THEN
    DO:
        FIND FIRST artikel WHERE artikel.betriebsnr = betriebsNo 
            NO-LOCK NO-ERROR.
        IF AVAILABLE artikel THEN RUN cr-artikel.
    END.
    WHEN 8 THEN
    DO:
        FOR EACH artikel WHERE artikel.departement = dept 
            AND (artikel.artart = 0 OR artikel.artart = 8 
                 OR (artikel.artart = 9 AND artikel.artgrp NE 0))
            AND artikel.activeflag = actFlag NO-LOCK :
            RUN cr-artikel.
        END.
    END.
    WHEN 9 THEN
    DO:
        FOR EACH artikel WHERE artikel.departement = dept 
            AND (artikel.artart = 0 OR artikel.artart = 8 
                 OR (artikel.artart = 9 AND artikel.artgrp NE 0))
            AND artikel.activeflag = actFlag
            AND artikel.bezeich GE aName NO-LOCK :
            RUN cr-artikel.
        END.
    END.
    WHEN 10 THEN
    DO:
        FIND FIRST artikel WHERE artikel.departement = 0
            AND (artikel.artart = 6 OR artikel.artart = 7) AND artikel.artnr = artNo
            NO-LOCK NO-ERROR.
        IF AVAILABLE artikel THEN RUN cr-artikel.
    END.
    WHEN 11 THEN
    DO:
        FOR EACH artikel WHERE artikel.artnr = artNo
            AND artikel.departement = dept 
            AND (artikel.artart = 0 OR artikel.artart = 1 
                 OR artikel.artart = 8 OR artikel.artart = 9) NO-LOCK :
            RUN cr-artikel.
        END.
    END.
    WHEN 12 THEN
    DO:
        IF dept = ? THEN dept = 0.
         FOR EACH artikel WHERE artikel.departement = dept 
             AND (artikel.artart = 2 OR artikel.artart = 5 
                  OR artikel.artart = 6 OR artikel.artart = 7) 
             AND artikel.activeflag = actFlag NO-LOCK:
             RUN cr-artikel.
         END.
    END.
    WHEN 13 THEN
    DO:
         FOR EACH artikel WHERE artikel.departement = dept
             AND (artikel.artart = 2 OR artikel.artart = 7)
             AND artikel.activeflag = actFlag NO-LOCK:
             RUN cr-artikel.
         END.
    END.
    WHEN 14 THEN
    DO:
        FIND FIRST artikel WHERE artikel.artart = 2 OR artikel.artart = 7
            NO-LOCK NO-ERROR.
        IF AVAILABLE artikel THEN RUN cr-artikel.
    END.
    WHEN 15 THEN
    DO:
        FIND FIRST artikel WHERE artikel.departement = dept
            AND (artikel.artart = 2 OR artikel.artart = 7) 
            AND artikel.artnr = artNo
            NO-LOCK NO-ERROR.
        IF AVAILABLE artikel THEN RUN cr-artikel.
    END.
    WHEN 16 THEN
    DO:
         FOR EACH artikel WHERE artikel.departement = dept
             AND artikel.artart = artart 
             AND artikel.activeflag = actFlag NO-LOCK:
             RUN cr-artikel.
         END.
    END.
    WHEN 17 THEN
    DO:
        FIND FIRST artikel WHERE artikel.artnr = artNo
            AND artikel.departement = dept AND artikel.artart = artart
            AND artikel.pricetab = actFlag NO-LOCK NO-ERROR. 
        IF AVAILABLE artikel THEN RUN cr-artikel.
    END.
    WHEN 18 THEN
    DO:
        FOR EACH artikel WHERE artikel.departement = dept 
            AND artikel.artart = artart AND artikel.pricetab = actFlag NO-LOCK :
            RUN cr-artikel.
        END.
    END.
    WHEN 19 THEN
    DO:
        FOR EACH t-artikel WHERE artikel.departement = dept 
            AND artikel.artart = artart AND artikel.artnr GE artNo
            AND artikel.pricetab = actFlag NO-LOCK :
            RUN cr-artikel.
        END.
    END.
    WHEN 20 THEN
    DO:
        FOR EACH artikel WHERE artikel.departement = dept 
            AND artikel.artnr = artNo NO-LOCK :
            RUN cr-artikel.
        END.
    END.
    WHEN 21 THEN
    DO:
        FIND FIRST artikel WHERE artikel.artnr = artNo AND
            artikel.departement = dept AND 
            (artikel.artart = 4 OR artikel.artart = 6) NO-LOCK NO-ERROR.
        IF AVAILABLE artikel THEN RUN cr-artikel.
    END.
    WHEN 22 THEN
    DO:
        IF  betriebsNo = 7 THEN
        FIND FIRST artikel WHERE artikel.departement = 0
            AND artikel.artnr = artNo 
            AND (artikel.artart = 4 OR artikel.artart = 7) NO-LOCK NO-ERROR.
        ELSE
        FIND FIRST artikel WHERE artikel.departement = 0 
            AND artikel.artnr = artNo 
            AND (artikel.artart = 4 OR artikel.artart = 2 OR artikel.artart = 7) NO-LOCK NO-ERROR.

        IF AVAILABLE artikel THEN RUN cr-artikel.
    END.
    WHEN 23 THEN
    DO:
        IF  betriebsNo = 7 THEN
        DO:
            IF artNo = 1 THEN
            FOR EACH artikel WHERE artikel.departement = 0
                AND (artikel.artart = 4 OR artikel.artart = 7)
                AND artikel.activeflag = YES NO-LOCK BY artikel.artnr:
                RUN cr-artikel.
            END.
            ELSE
            FOR EACH artikel WHERE artikel.departement = 0
                AND (artikel.artart = 4 OR artikel.artart = 7)
                AND artikel.activeflag = YES NO-LOCK BY artikel.bezeich:
                RUN cr-artikel.
            END.
        END.
        ELSE
        DO:
            IF artNo = 1 THEN
            FOR EACH artikel WHERE artikel.departement = 0 
                AND (artikel.artart = 4 OR artikel.artart = 2
                     OR artikel.artart = 7)
                AND artikel.activeflag = YES NO-LOCK BY artikel.artnr:
                RUN cr-artikel.
            END.
            ELSE
            FOR EACH artikel WHERE artikel.departement = 0 
                AND (artikel.artart = 4 OR artikel.artart = 2 
                     OR artikel.artart = 7)
                AND artikel.activeflag = YES NO-LOCK BY artikel.bezeich:
                RUN cr-artikel.
            END.
        END.
    END.
    WHEN 24 THEN
    DO:
      FOR EACH artikel WHERE artikel.departement = dept 
        AND (artikel.artart = 0 OR artikel.artart = 8 OR artikel.artart = 9) 
        AND artikel.activeflag = actFlag NO-LOCK:
        RUN cr-artikel.
      END.
      FOR EACH artikel WHERE artikel.departement = 0 
        AND (artikel.artart = 2 OR artikel.artart = 5
        OR artikel.artart = 6 OR artikel.artart = 7) 
        AND artikel.activeflag = actFlag NO-LOCK:
        RUN cr-artikel.
      END.
    END.
    WHEN 25 THEN
    DO:
      FOR EACH artikel WHERE artikel.departement = dept 
        AND (artikel.artart = 0 OR artikel.artart = 8 
        OR (artikel.artart = 9 AND artikel.artgrp NE 0)) 
        AND artikel.activeflag = actFlag NO-LOCK:
        RUN cr-artikel.
      END.
      FOR EACH artikel WHERE artikel.departement = 0 
        AND (artikel.artart = 2 OR artikel.artart = 5
        OR artikel.artart = 6 OR artikel.artart = 7) 
        AND artikel.activeflag = actFlag NO-LOCK:
        RUN cr-artikel.
      END.
    END.
    WHEN 26 THEN
    DO:
        FIND FIRST artikel WHERE artikel.bezeich = aName
            AND artikel.departement = dept
            AND artikel.artnr NE artNo NO-LOCK NO-ERROR.
        IF AVAILABLE artikel THEN RUN cr-artikel.
    END.
    WHEN 27 THEN
    DO:
        FIND FIRST artikel WHERE artikel.departement = dept
            AND artikel.zwkum = artNo NO-LOCK NO-ERROR.
        IF AVAILABLE artikel THEN RUN cr-artikel.
    END.
    WHEN 28 THEN
    DO:
        FIND FIRST artikel WHERE artikel.endkum = artNo
            NO-LOCK NO-ERROR.
        IF AVAILABLE artikel THEN RUN cr-artikel.
    END.
    WHEN 29 THEN
    DO:
        FIND FIRST artikel WHERE artikel.departement = dept
            NO-LOCK NO-ERROR.
        IF AVAILABLE artikel THEN RUN cr-artikel.
    END.
    WHEN 30 THEN
    DO:
        FIND FIRST artikel WHERE artikel.departement = dept
            AND (artikel.artart = 0 OR artikel.artart = 8) AND artikel.artnr = artNo
            NO-LOCK NO-ERROR.
        IF AVAILABLE artikel THEN RUN cr-artikel.
    END.
    WHEN 31 THEN
    DO:
        FIND FIRST artikel WHERE artikel.artart = 0 
            AND artikel.artgrp = artNo NO-LOCK NO-ERROR. 
        IF AVAILABLE artikel THEN RUN cr-artikel.
    END.
    WHEN 32 THEN
    DO:
        FOR EACH artikel WHERE artikel.artart = artart
            AND artikel.departement = dept NO-LOCK:
            RUN cr-artikel.
        END.
    END.
    WHEN 33 THEN
    DO:
        FOR EACH artikel WHERE artikel.departement = dept
            AND (artikel.artart = 0 OR artikel.artart = 8) NO-LOCK :
            RUN cr-artikel.
        END.
    END.   
    WHEN 34 THEN /*FD August 26, 2020*/
    DO:
        FIND FIRST artikel WHERE artikel.artnr = artno
            AND artikel.departement = dept
            AND artikel.artart = artart
            AND artikel.activeflag = actFlag NO-LOCK NO-ERROR.
        IF AVAILABLE artikel THEN RUN cr-artikel.
    END.
END CASE.

PROCEDURE cr-artikel :
    CREATE t-artikel.
    BUFFER-COPY artikel TO t-artikel.
END.
