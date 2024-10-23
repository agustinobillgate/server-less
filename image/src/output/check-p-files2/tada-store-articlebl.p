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

DEFINE INPUT PARAMETER case-type AS INT.
DEFINE INPUT PARAMETER vhp-artnr AS INT.
DEFINE INPUT PARAMETER deptno    AS INT.
DEFINE INPUT PARAMETER article-flag AS LOGICAL.
DEFINE INPUT PARAMETER TABLE FOR t-article.

IF case-type EQ 1 THEN
DO:
    FOR EACH t-article NO-LOCK:
        FIND FIRST queasy WHERE queasy.KEY EQ 270
            AND queasy.number1 EQ 2
            AND queasy.betriebsnr EQ t-article.vhpdept
            AND queasy.number2 EQ t-article.tadaartnr NO-LOCK NO-ERROR.
        IF NOT AVAILABLE queasy THEN
        DO:
            CREATE queasy.
            ASSIGN 
                queasy.KEY = 270
                queasy.betriebsnr = t-article.vhpdept
                queasy.deci1      = DEC(t-article.tadadept)
                queasy.number1    = 2
                queasy.number2    = t-article.tadaartnr
                queasy.number3    = t-article.vhpartnr
                queasy.char1      = t-article.tadasku
                queasy.char2      = t-article.tadabezeich
                queasy.char3      = t-article.vhpbezeich
                queasy.logi2      = t-article.tadaflag
                queasy.logi3      = t-article.vhpflag.
        END.
    END.
END.
ELSE IF case-type EQ 2 THEN
DO:
    FOR EACH t-article NO-LOCK:
        FIND FIRST queasy WHERE queasy.KEY EQ 270
            AND queasy.number1 EQ 2
            AND queasy.betriebsnr EQ t-article.vhpdept
            AND queasy.number2 EQ t-article.tadaartnr NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            FIND CURRENT queasy EXCLUSIVE-LOCK.
            ASSIGN 
                queasy.number2 = t-article.tadaartnr
                queasy.number3 = t-article.vhpartnr
                queasy.char1   = t-article.tadasku
                queasy.char2   = t-article.tadabezeich
                queasy.char3   = t-article.vhpbezeich
                queasy.logi2   = t-article.tadaflag
                queasy.logi3   = t-article.vhpflag.

            FIND CURRENT queasy NO-LOCK.
        END.
        ELSE
        DO:
            CREATE queasy.
            ASSIGN 
                queasy.KEY = 270
                queasy.betriebsnr = t-article.vhpdept
                queasy.deci1      = DEC(t-article.tadadept)
                queasy.number1    = 2
                queasy.number2    = t-article.tadaartnr
                queasy.number3    = t-article.vhpartnr
                queasy.char1      = t-article.tadasku
                queasy.char2      = t-article.tadabezeich
                queasy.char3      = t-article.vhpbezeich
                queasy.logi2      = t-article.tadaflag
                queasy.logi3      = t-article.vhpflag.
        END.
    END.
END.
ELSE IF case-type EQ 3 THEN
DO:
    FOR EACH t-article NO-LOCK:
        FIND FIRST queasy WHERE queasy.KEY EQ 270
            AND queasy.number1 EQ 2
            AND queasy.betriebsnr EQ deptno
            AND queasy.number3 EQ vhp-artnr NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            FIND CURRENT queasy EXCLUSIVE-LOCK.
            ASSIGN 
                queasy.logi3   = article-flag.

            FIND FIRST h-artikel WHERE h-artikel.departement EQ deptno AND h-artikel.artnr EQ vhp-artnr EXCLUSIVE-LOCK NO-ERROR.
            IF AVAILABLE h-artikel THEN h-artikel.activeflag = article-flag.

            FIND CURRENT queasy NO-LOCK.
            RELEASE queasy.
        END.
    END.
END.

