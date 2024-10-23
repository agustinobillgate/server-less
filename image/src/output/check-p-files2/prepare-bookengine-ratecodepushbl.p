DEF TEMP-TABLE t-push-list
    FIELD rcodeVHP      AS CHAR
    FIELD rcodeBE       AS CHAR
    FIELD rmtypeVHP     AS CHAR
    FIELD rmtypeBE      AS CHAR
    FIELD argtVHP       AS CHAR
    FIELD flag          AS INT INIT 0.

DEFINE TEMP-TABLE q-list
    FIELD rcode AS CHAR
    FIELD rcodeBE AS CHAR
    FIELD zikatnr AS INT
    FIELD rmtype  AS CHAR
    FIELD rmtypeBE  AS CHAR
    FIELD arrangement AS CHAR
.

DEFINE TEMP-TABLE rmcat-list 
    FIELD zikatnr  AS INTEGER 
    FIELD anzahl   AS INTEGER 
    FIELD typ      AS INTEGER
    FIELD sleeping AS LOGICAL INITIAL YES
    FIELD bezeich  AS CHAR
. 

DEFINE TEMP-TABLE dynarate-list
    FIELD scode AS CHAR.

DEFINE INPUT  PARAMETER bookengID      AS INT.
DEFINE OUTPUT PARAMETER bookeng-name   AS CHAR.
DEFINE OUTPUT PARAMETER TABLE FOR t-push-list.

/*DEFINE VAR bookengID      AS INT INIT 1.
DEFINE VAR bookeng-name   AS CHAR.*/

DEFINE VARIABLE cat-flag AS LOGICAL INIT NO.
DEFINE VARIABLE gastnrBE AS INT INIT 0.

DEFINE VARIABLE tokcounter  AS INTEGER NO-UNDO.
DEFINE VARIABLE ifTask      AS CHAR    NO-UNDO.
DEFINE VARIABLE mesToken    AS CHAR    NO-UNDO.
DEFINE VARIABLE mesValue    AS CHAR    NO-UNDO.
DEFINE VARIABLE scode       AS CHAR    NO-UNDO.

DEFINE BUFFER bratecode FOR ratecode.

FIND FIRST queasy WHERE queasy.KEY = 159 AND 
    queasy.number1 = bookengID NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO:
    bookeng-name = queasy.char1.
    gastnrBE = queasy.number2.
END.
ELSE RETURN.

FIND FIRST queasy WHERE queasy.KEY = 152 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN cat-flag = YES.


/*FOR EACH zimkateg WHERE zimkateg.verfuegbarkeit NO-LOCK:*/
/*FDL Feb 22, 2023 => Ticket F2306A*/
FOR EACH zimkateg WHERE zimkateg.verfuegbarkeit
    AND NOT zimkateg.bezeich MATCHES "*NOT USED*" NO-LOCK:
    IF cat-flag AND zimkateg.typ NE 0 THEN
        FIND FIRST rmcat-list WHERE rmcat-list.typ = zimkateg.typ NO-LOCK NO-ERROR.
    ELSE 
        FIND FIRST rmcat-list WHERE rmcat-list.zikatnr = zimkateg.zikatnr NO-LOCK NO-ERROR.
    IF NOT AVAILABLE rmcat-list THEN
    DO: 
        CREATE rmcat-list.
        IF cat-flag AND zimkateg.typ NE 0 THEN
        DO:
            FIND FIRST queasy WHERE queasy.KEY = 152 AND queasy.number1 = zimkateg.typ NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
                rmcat-list.bezeich = queasy.char1.
            rmcat-list.typ = zimkateg.typ.
        END.
        ELSE
            ASSIGN
                rmcat-list.typ = zimkateg.zikatnr
                rmcat-list.bezeich = zimkateg.kurzbez.  
    END. 
END.

FOR EACH guest-pr WHERE guest-pr.gastnr = gastnrBE NO-LOCK:
    FOR EACH rmcat-list:
        CREATE q-list.
        ASSIGN
            q-list.rcode = guest-pr.CODE
            q-list.zikatnr = rmcat-list.typ
            q-list.rmtype = rmcat-list.bezeich
        .
    END.
END.

FOR EACH q-list NO-LOCK:
    IF cat-flag THEN
        FIND FIRST zimkateg WHERE zimkateg.typ = q-list.zikatnr NO-LOCK NO-ERROR.
    ELSE 
        FIND FIRST zimkateg WHERE zimkateg.zikatnr = q-list.zikatnr NO-LOCK NO-ERROR.

    FIND FIRST queasy WHERE queasy.KEY = 2 AND queasy.char1 = q-list.rcode NO-LOCK NO-ERROR.
    IF AVAILABLE queasy AND queasy.logi2 THEN
    DO:
        FIND FIRST ratecode WHERE ratecode.CODE = q-list.rcode NO-LOCK NO-ERROR.
        IF AVAILABLE ratecode THEN
        DO:
            EMPTY TEMP-TABLE dynarate-list.
            DO tokcounter = 1 TO NUM-ENTRIES(ratecode.char1[5], ";") - 1:
                mesToken = SUBSTRING(ENTRY(tokcounter, ratecode.char1[5], ";"), 1, 2).
                mesValue = SUBSTRING(ENTRY(tokcounter, ratecode.char1[5], ";"), 3).
                CASE mesToken:
                   WHEN "RC" THEN
                   DO:
                       IF mesvalue NE "" THEN
                       DO:
                           CREATE dynarate-list.
                           ASSIGN
                               dynarate-list.scode = mesValue.
                       END.
                   END.
                END CASE.
            END.

            FOR EACH dynarate-list NO-LOCK:
                FIND FIRST bratecode WHERE bratecode.CODE = dynarate-list.sCode AND bratecode.zikatnr = zimkateg.zikatnr 
                    NO-LOCK NO-ERROR.
                IF AVAILABLE bratecode THEN
                DO:
                    FIND FIRST arrangement WHERE arrangement.argtnr = bratecode.argtnr NO-LOCK NO-ERROR.
                    IF AVAILABLE arrangement THEN
                        q-list.arrangement = arrangement.arrangement.
                    LEAVE.
                END.
            END.          
        END.
    END.
    ELSE IF AVAILABLE queasy AND NOT queasy.logi2 THEN
    DO:
        FIND FIRST bratecode WHERE bratecode.CODE = q-list.rcode AND bratecode.zikatnr = zimkateg.zikatnr 
            NO-LOCK NO-ERROR.
        IF AVAILABLE bratecode THEN
        DO:
            FIND FIRST arrangement WHERE arrangement.argtnr = bratecode.argtnr NO-LOCK NO-ERROR.
            IF AVAILABLE arrangement THEN
                q-list.arrangement = arrangement.arrangement.
        END.
    END.
    ELSE IF NOT AVAILABLE queasy THEN
    DO:
        DELETE q-list.
        RELEASE q-list.
    END.
END.

FOR EACH q-list NO-LOCK:
    FIND FIRST queasy WHERE queasy.KEY = 161 AND queasy.number1 = bookengID 
        AND ENTRY(1, queasy.char1, ";") = q-list.rcode
        AND ENTRY(3, queasy.char1, ";") = q-list.rmtype
        NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
        ASSIGN
            q-list.rcodeBE = ENTRY(2, queasy.char1, ";")
            q-list.rmtypeBE = ENTRY(4, queasy.char1, ";").

    CREATE t-push-list.
    ASSIGN
        t-push-list.rcodeVHP    = q-list.rcode
        t-push-list.rcodeBE     = q-list.rcodeBE
        t-push-list.rmtypeVHP   = q-list.rmtype
        t-push-list.rmtypeBE    = q-list.rmtypeBE
        t-push-list.argtVHP     = q-list.arrangement
    .
END.
    
