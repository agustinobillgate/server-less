DEF TEMP-TABLE t-pull-list
    FIELD rcodeVHP      AS CHAR
    FIELD rcodeBE       AS CHAR
    FIELD rmtypeVHP     AS CHAR
    FIELD rmtypeBE      AS CHAR
    FIELD argtVHP       AS CHAR
    FIELD flag          AS INT INIT 0.

DEFINE TEMP-TABLE temp-rate-list
    FIELD room-type         AS CHARACTER
    FIELD room-categ        AS CHARACTER
    FIELD dCode             AS CHARACTER
    FIELD sCode             AS CHARACTER
    FIELD currency          AS CHARACTER
    FIELD DYdatum-str       AS CHARACTER
    FIELD DMdatum-str       AS CHARACTER
    FIELD DTdatum-str       AS CHARACTER
    FIELD argt-str          AS CHARACTER
    .

DEFINE TEMP-TABLE sum-list 
  FIELD allot-flag  AS LOGICAL INITIAL NO
  FIELD bezeich     AS CHAR FORMAT "x(19)" 
  FIELD summe       AS INTEGER EXTENT 30 FORMAT "       ->>>9"
. 

DEFINE TEMP-TABLE room-list 
  FIELD avail-flag  AS LOGICAL INITIAL NO
  FIELD allot-flag  AS LOGICAL INITIAL NO
  FIELD zikatnr     AS INTEGER 
  FIELD i-typ       AS INTEGER
  FIELD sleeping    AS LOGICAL INITIAL YES 
  FIELD allotment   AS INTEGER EXTENT 30 
  FIELD bezeich     AS CHAR FORMAT "x(19)"
  FIELD room        AS INTEGER EXTENT 30 
  FIELD coom        AS CHAR EXTENT 30 FORMAT "x(15)"

  FIELD rmrate      AS DECIMAL EXTENT 30
  FIELD currency    AS INTEGER
  FIELD wabkurz     AS CHAR

  FIELD i-counter   AS INTEGER
  FIELD rateflag    AS LOGICAL INIT NO
  FIELD adult       AS INTEGER
  FIELD child       AS INTEGER
  FIELD prcode      AS CHAR EXTENT 30
  FIELD rmcat       AS CHAR
  FIELD argt        AS CHAR
  FIELD rcode       AS CHAR
  FIELD segmentcode AS CHAR
  FIELD dynarate    AS LOGICAL INIT NO
  FIELD expired     AS LOGICAL INIT NO
  FIELD argt-remark AS CHAR
  FIELD minstay     AS INTEGER INIT 0
  FIELD maxstay     AS INTEGER INIT 0
  FIELD minadvance  AS INTEGER INIT 0
  FIELD maxadvance  AS INTEGER INIT 0    
  FIELD frdate      AS DATE INIT ?
  FIELD todate      AS DATE INIT ?
  FIELD marknr      AS INTEGER INIT 0
  FIELD datum       AS DATE EXTENT 30
. 

DEF TEMP-TABLE t-pull-ratecode
    FIELD rcodeVHP      AS CHAR
    FIELD rcodeBE       AS CHAR
    FIELD rmtypeVHP     AS CHAR
    FIELD rmtypeBE      AS CHAR
    FIELD argtVHP       AS CHAR.

DEF TEMP-TABLE t-ratecode-list LIKE queasy
    FIELD SELECTED AS LOGICAL INIT YES.

DEF INPUT  PARAMETER bookengID AS INT.
DEF OUTPUT PARAMETER bookeng-name AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-pull-list.
DEF OUTPUT PARAMETER TABLE FOR t-ratecode-list.

DEFINE BUFFER quecateg FOR queasy.
FOR EACH queasy WHERE queasy.KEY = 163 AND queasy.number1 = bookengID NO-LOCK:

    CREATE t-pull-list.
    ASSIGN
        t-pull-list.rcodeVHP    = ENTRY(1, queasy.char1, ";")
        t-pull-list.rcodeBE     = ENTRY(2, queasy.char1, ";")
        t-pull-list.rmtypeVHP   = ENTRY(3, queasy.char1, ";")
        t-pull-list.rmtypeBE    = ENTRY(4, queasy.char1, ";")
        t-pull-list.argtVHP     = ENTRY(5, queasy.char1, ";").
END.

FOR EACH queasy WHERE queasy.KEY = 2 NO-LOCK:
    CREATE t-ratecode-list.
    BUFFER-COPY queasy TO t-ratecode-list.
END.
/*MT
DEF VAR gastnrBE AS INT.
FIND FIRST queasy WHERE queasy.KEY = 159 AND 
    queasy.number1 = bookengID NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO:
    bookeng-name = queasy.char1.
    gastnrBE = queasy.number2.
END.


DEF VAR allotFlag       AS INTEGER INIT 1.    /* 1 -> before allotment, 2 -> after allotment */
DEF VAR adult-child-str AS CHAR NO-UNDO.
DEF VAR co-date         AS DATE NO-UNDO.
DEF VAR curr-date       AS DATE NO-UNDO.
DEF VAR indGastnr       AS INTEGER NO-UNDO.
DEF VAR qci-zinr        AS CHAR NO-UNDO. 
DEF VAR room-categ      AS CHAR NO-UNDO. 
DEF VAR i               AS INTEGER NO-UNDO.
DEF VAR frDate          AS DATE INIT TODAY.
DEF VAR toDate          AS DATE INIT TODAY.
DEF VAR maxAdult        AS INT INIT 2.
DEF VAR maxChild        AS INT INIT 0.
ASSIGN
    curr-date   = frDate
    toDate      = frDate
.

/*DO WHILE curr-date LE toDate:*/
    co-date         = curr-date + 1.
    adult-child-str = "$A" + STRING(maxAdult) + "," 
                    + STRING(maxChild) + ","
                    + STRING(MONTH(co-date),"99")
                    + STRING(DAY(co-date),"99")
                    + STRING(YEAR(co-date),"9999").

    RUN cr-availabilitybl.p
        (1, NO, 0, 0, 0, adult-child-str, 1, allotFlag, 
         curr-date, NO /*excl tentative*/, NO /* excl inactive rooms */, 
         YES /*show-rate*/, INPUT-OUTPUT gastnrBE, qci-zinr,
         OUTPUT TABLE room-list, OUTPUT TABLE sum-list).

    RUN filter-room-list.
    FOR EACH room-list NO-LOCK BY room-list.i-counter:
        DO i = 1 TO 1:
            /*MTIF room-list.rmrate[i] NE 0 THEN*/
            DO:
                room-categ = "".
                FIND FIRST zimkateg WHERE zimkateg.zikatnr = room-list.zikatnr.
                FIND FIRST quecateg WHERE quecateg.KEY = 152 AND quecateg.number1 = zimkateg.typ
                    NO-ERROR.
                IF AVAILABLE quecateg THEN room-categ = quecateg.char1.

                FIND FIRST queasy WHERE queasy.key = 18 AND queasy.number1 = room-list.currency NO-ERROR.
                IF NOT AVAILABLE queasy THEN
                    FIND FIRST queasy WHERE queasy.KEY = 2 AND queasy.char1 = room-list.rcode.
                
                CREATE temp-rate-list.
                ASSIGN
                    temp-rate-list.room-type         = zimkateg.kurzbez
                    temp-rate-list.room-categ        = room-categ
                    temp-rate-list.dCode             = room-list.rcode
                    temp-rate-list.sCode             = room-list.prcode[i]
                    temp-rate-list.currency          = queasy.char3
                    temp-rate-list.DYdatum-str       = STRING(YEAR(curr-date),"9999")
                    temp-rate-list.DMdatum-str       = STRING(MONTH(curr-date),"99")
                    temp-rate-list.DTdatum-str       = STRING(DAY(curr-date),"99")
                    temp-rate-list.argt-str          = STRING(room-list.argt)
                    .
            END.
        END.
    END.
    curr-date = curr-date + 1.
    /*curr-date = co-date + 1.*/
/*END.*/
DEFINE BUFFER buf FOR temp-rate-list.

FOR EACH temp-rate-list:
    FIND FIRST buf WHERE buf.room-type = temp-rate-list.room-type
        AND buf.DYdatum-str = temp-rate-list.DYdatum-str
        AND buf.DMdatum-str = temp-rate-list.DMdatum-str
        AND buf.DTdatum-str = temp-rate-list.DTdatum-str
        AND buf.sCode = temp-rate-list.sCode
        AND buf.dCode = temp-rate-list.dCode
        AND buf.currency = temp-rate-list.currency
        AND buf.argt-str = temp-rate-list.argt-str
        AND buf.room-categ = temp-rate-list.room-categ
        AND RECID(buf) NE RECID(temp-rate-list) NO-ERROR.
    IF AVAILABLE buf THEN DELETE buf.
END.

FOR EACH temp-rate-list:
    CREATE t-pull-ratecode.
    IF temp-rate-list.dCode NE "" THEN
        t-pull-ratecode.rcodeVHP      = temp-rate-list.dCode.
    ELSE t-pull-ratecode.rcodeVHP     = temp-rate-list.sCode.

    ASSIGN
        t-pull-ratecode.rcodeBE       = ""
        t-pull-ratecode.rmtypeVHP     = temp-rate-list.room-type
        t-pull-ratecode.rmtypeBE      = ""
        t-pull-ratecode.argtVHP       = temp-rate-list.argt-str.
END.

FOR EACH queasy WHERE queasy.KEY = 163 AND queasy.number1 = bookengID NO-LOCK:

    CREATE t-pull-list.
    ASSIGN
        t-pull-list.rcodeVHP    = ENTRY(1, queasy.char1, ";")
        t-pull-list.rcodeBE     = ENTRY(2, queasy.char1, ";")
        t-pull-list.rmtypeVHP   = ENTRY(3, queasy.char1, ";")
        t-pull-list.rmtypeBE    = ENTRY(4, queasy.char1, ";")
        t-pull-list.argtVHP     = ENTRY(5, queasy.char1, ";").
END.

FOR EACH t-pull-list:
    FIND FIRST t-pull-ratecode WHERE t-pull-ratecode.rcodeVHP = t-pull-list.rcodeVHP
        AND t-pull-ratecode.rmtypeVHP = t-pull-list.rmtypeVHP
        AND t-pull-ratecode.argtVHP = t-pull-list.argtVHP
        NO-LOCK NO-ERROR.
    IF NOT AVAILABLE t-pull-ratecode THEN t-pull-list.flag = 1.
END.

FOR EACH t-pull-ratecode:
    FIND FIRST t-pull-list WHERE t-pull-list.rcodeVHP = t-pull-ratecode.rcodeVHP 
        AND t-pull-list.rmtypeVHP = t-pull-ratecode.rmtypeVHP 
        AND t-pull-list.argtVHP = t-pull-ratecode.argtVHP NO-ERROR.
    IF NOT AVAILABLE t-pull-list THEN
    DO:
        CREATE t-pull-list.
        BUFFER-COPY t-pull-ratecode TO t-pull-list.
    END.
END.

PROCEDURE filter-room-list:
    FOR EACH room-list WHERE room-list.expired:
        DELETE room-list.
    END.
END.
*/
