
DEFINE TEMP-TABLE t-dept
    FIELD nr    AS INTEGER FORMAT   ">9"
    FIELD dept  AS CHARACTER FORMAT "x(30)".

DEFINE TEMP-TABLE t-queasy270 LIKE queasy.

DEFINE TEMP-TABLE vhp-art 
    FIELD art-dept AS INT
    FIELD art-nr   AS INT  FORMAT ">>>>>>>>>" LABEL "Art No"
    FIELD art-name AS CHAR FORMAT "x(30)" LABEL "Art Name".

DEFINE TEMP-TABLE t-article
    FIELD vhpdept     AS INTEGER   FORMAT ">>>>>9" LABEL "VHP Dept"
    FIELD vhpartnr    AS INTEGER   FORMAT ">>>>>9" LABEL "VHP ArtNo"
    FIELD vhpbezeich  AS CHARACTER FORMAT "x(33)"  LABEL "VHP Article Name"
    FIELD vhpflag     AS LOGICAL LABEL "Active"
    FIELD tadadept    AS INTEGER   FORMAT ">>>>>9" LABEL "TADA Dept"
    FIELD tadaartnr   AS INTEGER   FORMAT ">>>>>9" LABEL "TADA ArtNo"
    FIELD tadabezeich AS CHARACTER FORMAT "x(33)"  LABEL "TADA Article Name"
    FIELD tadaflag    AS LOGICAL LABEL "Active"
    FIELD tadasku     AS CHAR
    .

DEFINE TEMP-TABLE crd-list
    FIELD deptno AS INT
    FIELD uname  AS CHAR
    FIELD pass   AS CHAR.

DEFINE INPUT PARAMETER dept AS INT.
DEFINE OUTPUT PARAMETER TABLE FOR t-dept.
DEFINE OUTPUT PARAMETER TABLE FOR t-queasy270.
DEFINE OUTPUT PARAMETER TABLE FOR vhp-art.
DEFINE OUTPUT PARAMETER TABLE FOR t-article.
DEFINE OUTPUT PARAMETER TABLE FOR crd-list.

FOR EACH hoteldpt WHERE hoteldpt.num GT 0 NO-LOCK:
    CREATE t-dept.
    ASSIGN
        t-dept.nr   = hoteldpt.num
        t-dept.dept = CAPS(hoteldpt.depart).
END.

FOR EACH queasy WHERE queasy.KEY EQ 270 AND queasy.number1 EQ 1 
    NO-LOCK BY queasy.betriebsnr BY queasy.number2:
    CREATE t-queasy270.
    BUFFER-COPY queasy TO t-queasy270.

    IF (queasy.number2 EQ 27 OR queasy.number2 EQ 28 OR queasy.number2 EQ 29 OR queasy.number2 EQ 30) THEN
    DO:
        IF NUM-ENTRIES(queasy.char2,";") GE 2 THEN
        DO:
            CREATE crd-list.
            ASSIGN 
                crd-list.deptno = INT(ENTRY(1,queasy.char2,";"))
                crd-list.uname  = ENTRY(2,queasy.char2,";")
                crd-list.pass   = ENTRY(3,queasy.char2,";").
        END.
    END.
END.

FOR EACH h-artikel WHERE h-artikel.departement EQ dept
    AND h-artikel.artart EQ 0
    AND h-artikel.activeflag EQ YES NO-LOCK:
    CREATE vhp-art.
    ASSIGN 
    vhp-art.art-dept = h-artikel.departement
    vhp-art.art-nr   = h-artikel.artnr
    vhp-art.art-name = h-artikel.bezeich.
END.

FOR EACH queasy WHERE queasy.KEY EQ 270
    AND queasy.number1 EQ 2
    AND queasy.betriebsnr EQ dept NO-LOCK:
    CREATE t-article.
    ASSIGN 
        t-article.vhpdept     = queasy.betriebsnr  
        t-article.tadadept    = queasy.deci1  
        t-article.tadaartnr   = queasy.number2 
        t-article.vhpartnr    = queasy.number3 
        t-article.tadasku     = queasy.char1   
        t-article.tadabezeich = queasy.char2   
        t-article.vhpbezeich  = queasy.char3   
        t-article.tadaflag    = queasy.logi2   
        t-article.vhpflag     = queasy.logi3.    
END.

