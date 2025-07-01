DEFINE TEMP-TABLE t-bill-line   LIKE bill-line.

DEFINE INPUT PARAMETER case-type    AS INTEGER.
DEFINE INPUT PARAMETER rechNo       AS INTEGER.
DEFINE INPUT PARAMETER artNo        AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR t-bill-line.

CASE case-type :
    WHEN 1 THEN
    DO:
        FIND FIRST bill-line WHERE bill-line.rechnr = rechNo NO-LOCK NO-ERROR.
        IF AVAILABLE bill-line THEN
        DO:
            CREATE t-bill-line.
            BUFFER-COPY bill-line TO t-bill-line.
        END.
    END.
    WHEN 2 THEN
    DO:
        FOR EACH bill-line WHERE bill-line.rechnr = rechNo NO-LOCK:
            CREATE t-bill-line.
            BUFFER-COPY bill-line TO t-bill-line.
        END.
    END.
    WHEN 3 THEN
    DO:
        FOR EACH bill-line WHERE bill-line.rechnr = rechNo ,
            FIRST artikel WHERE artikel.artnr = bill-line.artnr NO-LOCK :
            IF artikel.artart = 0 OR artikel.artart = 1 
                OR artikel.artart = 8 OR artikel.artart = 9 THEN
            DO:
                CREATE t-bill-line.
                BUFFER-COPY bill-line TO t-bill-line.
            END.
        END.
    END.
    WHEN 4 THEN
    DO:
        FOR EACH bill-line WHERE bill-line.rechnr = rechNo 
            AND bill-line.zinr NE "" NO-LOCK:
            CREATE t-bill-line.
            BUFFER-COPY bill-line TO t-bill-line.
        END.
    END.
    WHEN 5 THEN
    DO:
        FOR EACH bill-line WHERE bill-line.rechnr = rechNo NO-LOCK,
            FIRST artikel WHERE artikel.artnr = bill-line.artnr NO-LOCK :
            IF artikel.artart = 2 OR artikel.artart = 5 
                OR artikel.artart = 6 OR artikel.artart = 7 THEN
            DO:
                CREATE t-bill-line.
                BUFFER-COPY bill-line TO t-bill-line.
            END.
        END.
    END.
    WHEN 6 THEN
    DO:
        FOR EACH bill-line WHERE bill-line.rechnr = rechNo NO-LOCK, 
            FIRST artikel WHERE artikel.artnr = bill-line.artnr 
            AND artikel.departement = bill-line.departement NO-LOCK :
            CREATE t-bill-line.
            BUFFER-COPY bill-line TO t-bill-line.
        END.
            
    END.
    WHEN 7 THEN
    DO:
        FIND FIRST bill-line WHERE RECID(bill-line) = rechNo NO-LOCK.
        IF AVAILABLE bill-line THEN
        DO:
            CREATE t-bill-line.
            BUFFER-COPY bill-line TO t-bill-line.
        END.
            
    END.
END CASE.
