DEFINE TEMP-TABLE t-article
    FIELD nr            AS INT 
    FIELD artnr         AS INTEGER   FORMAT ">>>>>>>9" LABEL "ArtNo"
    FIELD dept          AS INTEGER   FORMAT ">>9"
    FIELD bezeich       AS CHARACTER FORMAT "x(30)"  LABEL "Article Name"
    FIELD img           AS CHARACTER FORMAT "x(50)"
    FIELD remark        AS CHARACTER FORMAT "x(78)" LABEL "Description"
    FIELD activ-art     AS LOGICAL
    FIELD sold-out      AS LOGICAL
    FIELD selected-art  AS LOGICAL INITIAL NO
    .

DEFINE TEMP-TABLE t-dept
    FIELD nr    AS INTEGER FORMAT   ">9"
    FIELD dept  AS CHARACTER FORMAT "x(30)".


DEFINE INPUT PARAMETER dept AS CHAR.
DEFINE INPUT PARAMETER case-type AS INT.
DEFINE OUTPUT PARAMETER licenseNr AS INT.
DEFINE OUTPUT PARAMETER TABLE FOR t-article.
DEFINE OUTPUT PARAMETER TABLE FOR t-dept.

DEF VAR nr AS INT.

FIND FIRST paramtext WHERE txtnr = 243 NO-LOCK NO-ERROR. 
IF AVAILABLE paramtext AND paramtext.ptexte NE "" THEN 
RUN decode-string(ptexte, OUTPUT licenseNr). 

FOR EACH hoteldpt WHERE hoteldpt.num GT 0 NO-LOCK:
    CREATE t-dept.
    ASSIGN
        t-dept.nr   = hoteldpt.num
        t-dept.dept = CAPS(hoteldpt.depart).

END.
IF dept EQ "" THEN
DO:
    FIND FIRST hoteldpt WHERE hoteldpt.num EQ 1 NO-LOCK NO-ERROR.
    dept = hoteldpt.depart.
END.

FIND FIRST hoteldpt WHERE hoteldpt.depart EQ dept NO-LOCK NO-ERROR.
FOR EACH h-artikel WHERE h-artikel.departement EQ hoteldpt.num
    AND h-artikel.activeflag EQ YES 
    AND h-artikel.artart EQ 0 
    AND h-artikel.epreis1 NE 0 NO-LOCK:
    FIND FIRST queasy WHERE queasy.KEY EQ 222 
        AND queasy.number1 EQ 2 
        AND queasy.number2 EQ h-artikel.artnr 
        AND queasy.number3 EQ h-artikel.departement NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        CREATE t-article.
        ASSIGN
            t-article.artnr     = queasy.number2
            t-article.dept      = queasy.number3
            t-article.bezeich   = h-artikel.bezeich
            t-article.img       = queasy.char2
            t-article.remark    = queasy.char3
            t-article.activ-art = queasy.logi1
            t-article.sold-out  = queasy.logi2. 
    END.
    ELSE
    DO:
        CREATE t-article.
        ASSIGN                   
            t-article.artnr     = h-artikel.artnr
            t-article.dept      = h-artikel.departement
            t-article.bezeich   = h-artikel.bezeich.
    END.
END.
nr = 0.
FOR EACH t-article BY t-article.activ-art DESC BY t-article.bezeich.
    nr = nr + 1.
    t-article.nr = nr.
END.
nr = 0.
FOR EACH t-article BY t-article.activ-art DESC BY t-article.bezeich.
    nr = nr + 1.
    t-article.nr = nr.
END.
/*
IF case-type EQ 1 THEN
DO:
    FOR EACH hoteldpt WHERE hoteldpt.num GT 0 NO-LOCK:
        CREATE t-dept.
        ASSIGN
            t-dept.nr   = hoteldpt.num
            t-dept.dept = CAPS(hoteldpt.depart).
    
    END.
    
    FOR EACH h-artikel WHERE h-artikel.departement EQ 1
        AND h-artikel.activeflag EQ YES 
        AND h-artikel.artart EQ 0 
        AND h-artikel.epreis1 NE 0 NO-LOCK:
        FIND FIRST queasy WHERE queasy.KEY EQ 222 
            AND queasy.number1 EQ 2 
            AND queasy.number2 EQ h-artikel.artnr 
            AND queasy.number3 EQ h-artikel.departement NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            CREATE t-article.
            ASSIGN
                t-article.artnr     = queasy.number2
                t-article.dept      = queasy.number3
                t-article.bezeich   = h-artikel.bezeich
                t-article.img       = queasy.char2
                t-article.remark    = queasy.char3
                t-article.activ-art = queasy.logi1
                .
        END.
        ELSE
        DO:
            CREATE t-article.
            ASSIGN                   
                t-article.artnr     = h-artikel.artnr
                t-article.dept      = h-artikel.departement
                t-article.bezeich   = h-artikel.bezeich.
        END.
    END.
    nr = 0.
    FOR EACH t-article BY t-article.activ-art DESC BY t-article.bezeich.
        nr = nr + 1.
        t-article.nr = nr.
    END.
END.
ELSE IF case-type EQ 2 THEN
DO:
    FOR EACH hoteldpt WHERE hoteldpt.num GT 0 NO-LOCK:
        CREATE t-dept.
        ASSIGN
            t-dept.nr   = hoteldpt.num
            t-dept.dept = CAPS(hoteldpt.depart).
    
    END.
    FIND FIRST hoteldpt WHERE hoteldpt.depart EQ dept NO-LOCK NO-ERROR.
    FOR EACH h-artikel WHERE h-artikel.departement EQ hoteldpt.num
        AND h-artikel.activeflag EQ YES 
        AND h-artikel.artart EQ 0 
        AND h-artikel.epreis1 NE 0 NO-LOCK:
        FIND FIRST queasy WHERE queasy.KEY EQ 222 
            AND queasy.number1 EQ 2 
            AND queasy.number2 EQ h-artikel.artnr 
            AND queasy.number3 EQ h-artikel.departement NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            CREATE t-article.
            ASSIGN
                t-article.artnr     = queasy.number2
                t-article.dept      = queasy.number3
                t-article.bezeich   = h-artikel.bezeich
                t-article.img       = queasy.char2
                t-article.remark    = queasy.char3
                t-article.activ-art = queasy.logi1.
        END.
        ELSE
        DO:
            CREATE t-article.
            ASSIGN                   
                t-article.artnr     = h-artikel.artnr
                t-article.dept      = h-artikel.departement
                t-article.bezeich   = h-artikel.bezeich.
        END.
    END.
    nr = 0.
    FOR EACH t-article BY t-article.activ-art DESC BY t-article.bezeich.
        nr = nr + 1.
        t-article.nr = nr.
    END.
END.
*/
PROCEDURE decode-string1: 
DEFINE INPUT PARAMETER in-str AS CHAR. 
DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "". 
DEFINE VARIABLE s AS CHAR. 
DEFINE VARIABLE j AS INTEGER. 
DEFINE VARIABLE len AS INTEGER. 
  s = in-str. 
  j = ASC(SUBSTR(s, 1, 1)) - 71. 
  len = LENGTH(in-str) - 1. 
  s = SUBSTR(in-str, 2, len). 
  DO len = 1 TO LENGTH(s): 
    out-str = out-str + chr(ASC(SUBSTR(s,len,1)) - j). 
  END. 
  out-str = SUBSTR(out-str, 5, (LENGTH(out-str) - 4)). 
END. 

PROCEDURE decode-string: 
DEFINE INPUT PARAMETER in-str   AS CHAR. 
DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "". 
DEFINE VARIABLE s   AS CHAR. 
DEFINE VARIABLE j   AS INTEGER. 
DEFINE VARIABLE len AS INTEGER. 
  s = in-str. 
  j = ASC(SUBSTR(s, 1, 1)) - 70. 
  len = LENGTH(in-str) - 1. 
  s = SUBSTR(in-str, 2, len). 
  DO len = 1 TO LENGTH(s): 
    out-str = out-str + chr(asc(SUBSTR(s,len,1)) - j). 
  END. 
END. 
