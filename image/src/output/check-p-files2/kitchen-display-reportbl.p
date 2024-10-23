DEFINE TEMP-TABLE kds
    FIELD nr            AS INT  FORMAT ">>>"        LABEL "No"
    FIELD kdsno         AS CHAR FORMAT "x(20)"        LABEL "KDS No"
    FIELD datum         AS DATE FORMAT "99/99/9999" LABEL "Date" 
    FIELD tableno       AS INT  FORMAT ">>>>>"      LABEL "Table"
    FIELD deptno        AS CHAR FORMAT "x(20)"      LABEL "Department"
    FIELD billno        AS INT  FORMAT ">>>>>>"     LABEL "Bill No"
    FIELD artno         AS INT  FORMAT ">>>>>>>>>"  LABEL "Art No"
    FIELD artqty        AS INT  FORMAT ">>>"        LABEL "Qty"
    FIELD artname       AS CHAR FORMAT "x(25)"      LABEL "Menu Description"
    FIELD sp-req        AS CHAR FORMAT "x(25)"      LABEL "Special Request"
    FIELD postby        AS CHAR FORMAT "x(20)"      LABEL "Posting By"
    FIELD postdate      AS DATE FORMAT "99/99/9999" LABEL "Posting Date" 
    FIELD post-time         AS CHAR FORMAT "x(15)"      LABEL "Posting Time"
    FIELD cooking-time      AS CHAR FORMAT "x(15)"   
    FIELD done-time         AS CHAR FORMAT "x(15)"  
    FIELD cooking-interval  AS CHAR FORMAT "x(15)" 
    FIELD served-time       AS CHAR FORMAT "x(15)" 
    FIELD serving-interval  AS CHAR FORMAT "x(15)" 
    FIELD inttime           AS CHAR FORMAT "x(15)"      LABEL "Interval".

DEFINE INPUT PARAMETER from-date   AS DATE.  
DEFINE INPUT PARAMETER to-date     AS DATE.  
DEFINE INPUT PARAMETER dept        AS INT.   
DEFINE INPUT PARAMETER kds-number  AS INT.
DEFINE OUTPUT PARAMETER TABLE FOR kds.

/*
DEFINE VARIABLE from-date   AS DATE.
DEFINE VARIABLE to-date     AS DATE.
DEFINE VARIABLE dept        AS INT.      
DEFINE VARIABLE kds-number  AS INT.

ASSIGN
from-date  = 01/01/23
to-date    = 04/03/23
dept       = 1
kds-number = 98.
*/

DEFINE VARIABLE count-i AS INTEGER.
DEFINE BUFFER q-kds-line FOR queasy.
DEFINE BUFFER qtime FOR queasy.
DEFINE BUFFER void-line FOR h-bill-line.

DEFINE VARIABLE nr        AS INT.
DEFINE VARIABLE spreq     AS CHAR.
DEFINE VARIABLE starttime AS INT.
DEFINE VARIABLE endtime   AS INT.
DEFINE VARIABLE inttime   AS INT.
DEFINE VARIABLE deptname  AS CHAR.
DEFINE VARIABLE currdate  AS DATE.
DEFINE VARIABLE orig-char  AS CHAR.

DO currdate = from-date TO to-date:
    FOR EACH queasy WHERE queasy.KEY EQ 257
        AND queasy.char1 EQ "kds-header"
        AND queasy.date1 EQ currdate
        AND queasy.number1 EQ dept
        NO-LOCK BY queasy.date1 BY queasy.deci1:
    
        FOR EACH q-kds-line WHERE q-kds-line.KEY EQ 255
            AND q-kds-line.char1 EQ "kds-line"
            AND q-kds-line.deci2 EQ DEC(RECID(queasy))
            /*AND NOT q-kds-line.logi1*/ EXCLUSIVE-LOCK,
            FIRST h-bill-line WHERE RECID(h-bill-line) EQ q-kds-line.number3 NO-LOCK,
            FIRST h-artikel WHERE  h-artikel.departement EQ h-bill-line.departement
            AND h-artikel.artnr EQ h-bill-line.artnr
            AND h-artikel.bondruckernr[1] EQ kds-number NO-LOCK BY q-kds-line.date1 BY q-kds-line.deci1:
            FIND FIRST h-journal WHERE h-journal.schankbuch EQ q-kds-line.number3 NO-LOCK NO-ERROR.
            IF AVAILABLE h-journal THEN spreq = h-journal.aendertext.
            ELSE spreq = "".
    
            FIND FIRST hoteldpt WHERE hoteldpt.num EQ h-artikel.departement NO-LOCK NO-ERROR.
            IF AVAILABLE hoteldpt THEN deptname = hoteldpt.depart.
            ELSE deptname = "".
    
            starttime  = INT(q-kds-line.deci1).
            endtime    = INT(q-kds-line.deci3).
            IF q-kds-line.char3 EQ "2" THEN inttime = endtime - starttime.
            ELSE inttime = 0.
            
            FIND FIRST printer WHERE printer.nr EQ h-artikel.bondruckernr[1] NO-LOCK NO-ERROR.
            FIND FIRST qtime WHERE qtime.KEY EQ 302 AND qtime.betriebsnr EQ INT(RECID(q-kds-line)) NO-LOCK NO-ERROR.
            IF AVAILABLE qtime THEN orig-char = qtime.char1.
            ELSE orig-char = "-|-|-".

            nr = nr + 1.
            CREATE kds.
            ASSIGN 
                kds.nr               = nr
                kds.kdsno            = STRING(printer.nr) + " - " + printer.make
                kds.datum            = queasy.date1
                kds.tableno          = queasy.number3
                kds.deptno           = deptname
                kds.billno           = q-kds-line.number2 
                kds.artno            = h-artikel.artnr
                kds.artqty           = h-bill-line.anzahl
                kds.artname          = h-artikel.bezeich 
                kds.sp-req           = spreq
                kds.postby           = queasy.char2
                kds.postdate         = queasy.date1
                kds.post-time        = STRING(starttime,"HH:MM:SS")
                kds.done-time        = STRING(endtime,"HH:MM:SS")
                kds.inttime          = STRING(inttime,"HH:MM:SS")
                kds.cooking-time     = ENTRY(1,orig-char,"|")
                kds.done-time        = ENTRY(2,orig-char,"|")
                kds.cooking-interval = STRING(DATETIME(kds.done-time) - DATETIME(kds.cooking-time),"HH:MM:SS")
                kds.served-time      = ENTRY(3,orig-char,"|")
                kds.serving-interval = STRING(DATETIME(kds.served-time) - DATETIME(kds.done-time),"HH:MM:SS")
                .
        END.
    END.
END.

/*
CURRENT-WINDOW:WIDTH = 250.
FOR EACH kds:
    DISP kds WITH WIDTH 240.
END.*/
