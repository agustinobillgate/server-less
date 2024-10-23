
DEFINE TEMP-TABLE tmp-faartikel LIKE fa-artikel
    FIELD NAME      AS CHAR
    FIELD asset     AS CHAR  FORMAT "99.999.9999"
    FIELD datum     AS DATE
    FIELD price     AS DECIMAL
    FIELD bezeich   AS CHAR
    FIELD location  AS CHAR
    FIELD remark    AS CHAR
.

DEFINE TEMP-TABLE t-faartikel LIKE fa-artikel.

DEFINE OUTPUT PARAMETER TABLE FOR tmp-faartikel.

RUN create-artikel.

FOR EACH mathis NO-LOCK, 
    FIRST t-faartikel WHERE t-faartikel.nr = mathis.nr 
    AND NOT t-faartikel.posted AND t-faartikel.loeschflag = 0 
    AND t-faartikel.next-depn = ? ,
    FIRST fa-grup WHERE fa-grup.gnr = t-faartikel.subgrp AND fa-grup.flag = 1
    NO-LOCK BY mathis.NAME :
    CREATE tmp-faartikel.
    BUFFER-COPY t-faartikel TO tmp-faartikel.
    ASSIGN 
        tmp-faartikel.NAME    = mathis.NAME
        tmp-faartikel.asset   = mathis.asset
        tmp-faartikel.datum   = mathis.datum
        tmp-faartikel.price   = mathis.price
        tmp-faartikel.location = mathis.location
        tmp-faartikel.remark  = mathis.remark
        tmp-faartikel.bezeich = fa-grup.bezeich.
END.



PROCEDURE create-artikel :
    FOR EACH fa-artikel WHERE NOT fa-artikel.posted AND fa-artikel.loeschflag = 0 
        AND fa-artikel.next-depn = ? :
        
        FIND FIRST fa-order WHERE fa-order.activeflag = 0 AND fa-order.fa-nr = fa-artikel.nr NO-LOCK NO-ERROR.
        IF AVAILABLE fa-order THEN
        DO:

        END.
        ELSE
        DO:
            CREATE t-faartikel.
            BUFFER-COPY fa-artikel TO t-faartikel.
        END.
    END.
END.
