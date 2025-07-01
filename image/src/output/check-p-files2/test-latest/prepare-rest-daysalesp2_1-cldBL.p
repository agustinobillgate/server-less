DEFINE TEMP-TABLE htl-dept
    FIELD dptnr     AS INTEGER COLUMN-LABEL "Number"
    FIELD bezeich   AS CHAR    COLUMN-LABEL "Description" FORMAT "x(24)".

DEF TEMP-TABLE t-hoteldpt LIKE hoteldpt.
DEF TEMP-TABLE buf-art
    FIELD artnr LIKE artikel.artnr
    FIELD bezeich LIKE artikel.bezeich
    FIELD departement LIKE artikel.departement
    FIELD art-type AS INTEGER.

DEF TEMP-TABLE usr1 LIKE kellner
    FIELD rec-id AS INT.

DEFINE OUTPUT PARAMETER disc-art1       AS INTEGER INITIAL -1   NO-UNDO. 
DEFINE OUTPUT PARAMETER disc-art2       AS INTEGER INITIAL -1   NO-UNDO. 
DEFINE OUTPUT PARAMETER disc-art3       AS INTEGER INITIAL -1   NO-UNDO.
DEFINE OUTPUT PARAMETER exchg-rate      as decimal format ">>,>>9.99". 
DEFINE OUTPUT PARAMETER str             as char. 
DEFINE OUTPUT PARAMETER curr-foreign    as char.  
DEFINE OUTPUT PARAMETER serv-taxable    as logical initial NO. 
DEFINE OUTPUT PARAMETER dpt-str         AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER art-str         AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER oth-str         AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER anzahl          as integer initial 0. 
DEFINE OUTPUT PARAMETER curr-dept       as integer.
DEFINE OUTPUT PARAMETER dept-name       as char.
DEFINE OUTPUT PARAMETER voucher-art     AS INTEGER INITIAL 0.
DEFINE OUTPUT PARAMETER use-voucher     AS LOGICAL INITIAL YES.
DEFINE OUTPUT PARAMETER from-date       as date.
DEFINE OUTPUT PARAMETER to-date         as date. 
DEFINE OUTPUT PARAMETER htl-dept-dptnr  AS INT.
DEFINE OUTPUT PARAMETER err-flag        AS INT INIT 0.
DEFINE OUTPUT PARAMETER p-110           AS DATE.
DEFINE OUTPUT PARAMETER p-240           AS LOGICAL.
DEFINE OUTPUT PARAMETER active-deposit  AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR buf-art.
DEFINE OUTPUT PARAMETER TABLE FOR htl-dept.
DEFINE OUTPUT PARAMETER TABLE FOR usr1.

DEFINE VARIABLE f-cash          AS LOGICAL INITIAL NO.
define variable i               AS INTEGER.
DEFINE VARIABLE str-tmp         AS CHAR NO-UNDO.
DEFINE VARIABLE curr-local      AS CHAR NO-UNDO.
DEFINE VARIABLE price-decimal   AS INTEGER NO-UNDO.
define variable artnr-list      as integer extent 20.           /*extent 10 gerald 4A7817*/
DEFINE VARIABLE show-option     AS LOGICAL INITIAL NO NO-UNDO.

FIND FIRST vhp.htparam WHERE paramnr = 556 NO-LOCK. 
IF vhp.htparam.finteger > 0 THEN disc-art3 = vhp.htparam.finteger. 
FIND FIRST vhp.htparam WHERE paramnr = 557 NO-LOCK. 
IF vhp.htparam.finteger > 0 THEN disc-art1 = vhp.htparam.finteger. 
FIND FIRST vhp.htparam WHERE paramnr = 596 NO-LOCK. 
IF vhp.htparam.finteger > 0 THEN disc-art2 = vhp.htparam.finteger.

find first htparam where htparam.paramnr = 144 no-lock. 
find first waehrung where waehrung.wabkurz = htparam.fchar no-lock no-error. 
if available waehrung then exchg-rate = waehrung.ankauf / waehrung.einheit. 
else exchg-rate = 1. 
 
find first htparam where paramnr = 152 no-lock. 
curr-local = fchar. 
find first htparam where paramnr = 144 no-lock. 
curr-foreign = fchar. 

FIND FIRST htparam WHERE htparam.paramnr = 491. 
price-decimal =  htparam.finteger.

FIND FIRST vhp.htparam WHERE htpara.paramnr = 588 NO-LOCK. 
active-deposit = htparam.flogical.

str = curr-local + ";" + STRING(price-decimal).
 
find first htparam where htparam.paramnr = 479 no-lock. 
if htparam.flogical  /* service taxable */ then serv-taxable = YES.

FIND FIRST htparam WHERE paramnr = 732 NO-LOCK.
IF fchar NE "" THEN
DO:
    DO i = 1 TO NUM-ENTRIES(fchar, ";"):
        str-tmp = ENTRY(i, fchar, ";").
        CASE SUBSTR(str-tmp, 1, 1) :
            WHEN "D" THEN
                dpt-str = SUBSTR(str-tmp, 2, (LENGTH(str-tmp) - 1)).
            WHEN "A" THEN
                art-str = SUBSTR(str-tmp, 2, (LENGTH(str-tmp) - 1)).
            WHEN "G" THEN
                oth-str = SUBSTR(str-tmp, 2, (LENGTH(str-tmp) - 1)).
        END CASE.
    END.  
    
END.
ELSE 
DO:
    err-flag = 1.
    RETURN.
END.

FOR EACH hoteldpt:
    CREATE t-hoteldpt.
    BUFFER-COPY hoteldpt TO t-hoteldpt.
END.

DO i = 1 TO NUM-ENTRIES(art-str, ","):
    IF i GT 21 THEN .
    ELSE
    DO:
        artnr-list[i] = INTEGER(ENTRY(i, art-str, ",")).
        IF /*artnr-list[i] = disc-art1 OR*/ artnr-list[i] = disc-art2
            OR artnr-list[i] = disc-art3 THEN show-option = YES.

        IF artnr-list[i] NE 0 THEN anzahl = anzahl + 1.
    END.
END.
DO i = 1 TO NUM-ENTRIES(dpt-str, ","):
    IF INTEGER(ENTRY(i, dpt-str, ",")) NE 0 THEN
    DO:
        FIND FIRST hoteldpt WHERE hoteldpt.num = INTEGER(ENTRY(i, dpt-str, ","))
            NO-LOCK NO-ERROR.
        IF AVAILABLE hoteldpt THEN
        DO:
            CREATE htl-dept.
            ASSIGN
                htl-dept.dptnr   = hoteldpt.num
                htl-dept.bezeich = hoteldpt.depart.
        END.
    END.
END.

FIND FIRST htl-dept NO-LOCK NO-ERROR.
IF NOT AVAILABLE htl-dept THEN
DO:
    err-flag = 2.
    RETURN.
END.

ASSIGN
    curr-dept = htl-dept.dptnr
    dept-name = htl-dept.bezeich
    .
htl-dept-dptnr = htl-dept.dptnr.

DO i = 1 TO anzahl:
    FOR EACH artikel WHERE artikel.artnr = artnr-list[i] 
        /*AND artikel.departement = curr-dept*/ NO-LOCK :
        CREATE buf-art.
        ASSIGN
            buf-art.artnr       = artikel.artnr
            buf-art.bezeich     = artikel.bezeich
            buf-art.departement = artikel.departement
            buf-art.art-type    = artikel.umsatzart
            .
    END.
END.

/*MT
IF oth-str NE "" THEN
DO:
    bezeich[11] = ENTRY(1, oth-str, ",").
    DO i = 2 TO NUM-ENTRIES(oth-str, ","):
        IF i GT 11 THEN .
        ELSE DO:
            CREATE other-art.
            ASSIGN 
                other-art.artnr = INTEGER(ENTRY(i, oth-str, ",")).
        END.
    END. 
    IF ENTRY(2, oth-str, ",") NE "" THEN
        oth-flag = YES.
END.
*/

FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 1001 NO-LOCK. 
IF vhp.htparam.finteger > 0 THEN 
DO: 
  FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr = vhp.htparam.finteger 
    AND vhp.h-artikel.artart = 6 NO-LOCK NO-ERROR. 
  IF AVAILABLE vhp.h-artikel THEN
  DO:
    voucher-art = vhp.h-artikel.artnr.
    FOR EACH h-artikel WHERE h-artikel.artart = 6 NO-LOCK,
      FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront
      AND artikel.departement = 0 AND artikel.pricetab NO-LOCK:
      ASSIGN
        f-cash      = YES
        use-voucher = NO.
      LEAVE.
    END.
  END.
END.
 
find first htparam where paramnr = 110 no-lock.  /*Invoicing Date */ 
ASSIGN
  from-date = htparam.fdate 
  to-date   = from-date
.

FOR EACH kellner /*MTWHERE kellner.departement = curr-dept*/:
    CREATE usr1.
    BUFFER-COPY kellner TO usr1.
    ASSIGN usr1.rec-id = RECID(kellner).
END.
FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK.
p-110 = htparam.fdate.
FIND FIRST htparam WHERE htparam.paramnr = 240 NO-LOCK.
p-240 = htparam.flogical.
