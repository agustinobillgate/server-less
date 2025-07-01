
DEF TEMP-TABLE t-add-last
    FIELD wabkurz LIKE waehrung.wabkurz.

DEF TEMP-TABLE t-mathis
    FIELD artnr AS INTEGER
    FIELD asset-name AS CHARACTER
    FIELD asset-number AS CHARACTER.
    
DEF TEMP-TABLE t-lief-list
    FIELD firma AS CHARACTER
    FIELD lief-nr AS INTEGER.

DEF TEMP-TABLE t-dept-list
    FIELD NAME AS CHARACTER
    FIELD nr   AS INTEGER.

DEF INPUT-OUTPUT PARAMETER Order-Nr AS CHAR.
DEF OUTPUT PARAMETER err-no AS INT INIT 0.
DEF OUTPUT PARAMETER local-nr AS INTEGER.
DEF OUTPUT PARAMETER billdate AS DATE.
DEF OUTPUT PARAMETER add-first-waehrung-wabkurz AS CHAR INIT "".
DEF OUTPUT PARAMETER TABLE FOR t-add-last.
DEF OUTPUT PARAMETER TABLE FOR t-mathis.
DEF OUTPUT PARAMETER TABLE FOR t-lief-list.
DEF OUTPUT PARAMETER TABLE FOR t-dept-list.


FOR EACH l-lieferant NO-LOCK:
    CREATE t-lief-list.
    ASSIGN
        t-lief-list.firma = l-lieferant.firma
        t-lief-list.lief-nr = l-lieferant.lief-nr
    .
END.

FOR EACH mathis NO-LOCK:
    CREATE t-mathis.
    ASSIGN
        t-mathis.artnr = mathis.nr
        t-mathis.asset-name = mathis.NAME
        t-mathis.asset-number = mathis.asset
    .
END.

FOR EACH parameters WHERE progname = "CostCenter" AND SECTION = "Name" NO-LOCK:
    CREATE t-dept-list.
    ASSIGN
        t-dept-list.NAME = parameters.vstring
        t-dept-list.nr = INT(parameters.varname)
    .
END.

FIND FIRST htparam WHERE htparam.paramnr = 152 NO-LOCK. 
FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
IF NOT AVAILABLE waehrung THEN 
DO: 
    err-no = 1.
    RETURN. 
END. 

local-nr = waehrung.waehrungsnr. 

FIND FIRST htparam WHERE paramnr = 975 NO-LOCK. 
IF htparam.finteger NE 1 AND htparam.finteger NE 2 THEN 
DO: 
  FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
  billdate = htparam.fdate. 
END. 
ELSE billdate = TODAY. 

IF order-nr = "" THEN 
DO: 
  RUN new-fapo-number. 
END. 

RUN currency-list. 


PROCEDURE new-fapo-number :
    DEFINE BUFFER fa-orderhdr1 FOR fa-ordheader. 
    DEFINE VARIABLE s AS CHAR. 
    DEFINE VARIABLE i AS INTEGER INITIAL 1. 
    DEFINE VARIABLE mm AS INTEGER. 
    DEFINE VARIABLE yy AS INTEGER. 
    DEFINE VARIABLE dd AS INTEGER.
    DEFINE VARIABLE docu-nr AS CHAR.
    DEF VAR a AS LOGICAL.

    FIND FIRST htparam WHERE paramnr = 973 NO-LOCK. 
    IF htparam.paramgr = 21 THEN 
    DO:
        mm = month(billdate). 
        yy = year(billdate). 
        dd = DAY(billdate).

        s = "F" + SUBSTR(STRING(year(billdate)),3,2) 
          + STRING(MONTH(billdate), "99").   

        IF htparam.flogical THEN
        DO:
            FIND FIRST fa-counter WHERE fa-counter.count-type = 0 AND fa-counter.yy = yy AND fa-counter.mm = mm AND
                fa-counter.dd = dd AND fa-counter.docu-type = 0 EXCLUSIVE-LOCK NO-ERROR.
            IF NOT AVAILABLE fa-counter THEN
            DO:
                CREATE fa-counter.
                ASSIGN fa-counter.count-type = 0
                       fa-counter.yy         = yy
                       fa-counter.mm         = mm
                       fa-counter.dd         = dd
                       fa-counter.counters   = 0
                       fa-counter.docu-type   = 0 .

            END.
            FIND CURRENT fa-counter NO-LOCK.
            i = fa-counter.counters + 1 .
            docu-nr = s + string(dd,"99") + STRING(i, "999").
        END.
        ELSE
        DO:
            FIND FIRST fa-counter WHERE fa-counter.count-type = 1 AND fa-counter.yy = yy 
                AND fa-counter.mm = mm AND fa-counter.docu-type = 0 EXCLUSIVE-LOCK NO-ERROR.
            IF NOT AVAILABLE fa-counter THEN
            DO:
                CREATE fa-counter.
                ASSIGN fa-counter.count-type = 1
                       fa-counter.yy         = yy
                       fa-counter.mm         = mm
                       fa-counter.dd         = 0
                       fa-counter.counters   = 0
                       fa-counter.docu-type   = 0 .

            END.
            FIND CURRENT fa-counter NO-LOCK.
            i = fa-counter.counters + 1.
            docu-nr = s + STRING(i, "99999"). 
        END.
    END.

    ASSIGN order-nr = docu-nr.
    /*MTDISP order-nr WITH FRAME frame1.*/

END PROCEDURE.


PROCEDURE currency-list :
    FIND FIRST waehrung WHERE waehrung.waehrungsnr = local-nr NO-LOCK. 
    add-first-waehrung-wabkurz = waehrung.wabkurz.

    FOR EACH waehrung WHERE waehrung.waehrungsnr NE local-nr 
        AND waehrung.ankauf GT 0 AND waehrung.betriebsnr NE 0 
        NO-LOCK BY waehrung.wabkurz: 
        CREATE t-add-last.
        t-add-last.wabkurz = waehrung.wabkurz.
    END. 

END PROCEDURE.

