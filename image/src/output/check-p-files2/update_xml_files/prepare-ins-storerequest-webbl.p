DEFINE TEMP-TABLE op-list LIKE l-op 
  FIELD bezeich  AS CHAR FORMAT "x(36)"             COLUMN-LABEL "Description" 
  FIELD username AS CHAR FORMAT "x(16)"             COLUMN-LABEL "Created by" 
  FIELD onhand   AS DECIMAL FORMAT "->,>>>,>>9.99"  COLUMN-LABEL "On-Hand"
  FIELD new-flag AS LOGICAL INIT YES
.

DEF TEMP-TABLE t-l-lager LIKE l-lager.

DEFINE BUFFER sys-user FOR bediener. 

/* Oscar (14/03/25) - 3E510E - change payload format */
DEFINE TEMP-TABLE payload-list
    FIELD user-init AS CHAR
    FIELD t-datum   AS CHARACTER
    FIELD t-lschein AS CHAR
.

/* Oscar (14/03/25) - 3E510E - change response format and add new field sr-remark */
DEFINE TEMP-TABLE response-list
    FIELD deptname      AS CHAR
    FIELD curr-lager    AS INT
    FIELD deptNo        AS INTEGER
    FIELD show-price    AS LOGICAL
    FIELD req-flag      AS LOGICAL
    FIELD p-220         AS INT
    FIELD out-type      AS INTEGER INIT 1
    FIELD transfered    AS LOGICAL INITIAL NO
    FIELD to-stock      AS INTEGER
    FIELD lager-bezeich AS CHAR
    FIELD lager-bez1    AS CHAR
    FIELD curr-pos      AS INTEGER
    FIELD t-amount      AS DECIMAL
    FIELD lscheinnr     LIKE l-op.lscheinnr
    FIELD sr-remark     AS CHARACTER
. 

DEFINE VARIABLE user-init      AS CHAR.
DEFINE VARIABLE t-datum        AS DATE.
DEFINE VARIABLE t-lschein      AS CHAR.

DEFINE VARIABLE deptname       AS CHAR.
DEFINE VARIABLE curr-lager     AS INT.
DEFINE VARIABLE deptNo         AS INTEGER.
DEFINE VARIABLE show-price     AS LOGICAL.
DEFINE VARIABLE req-flag       AS LOGICAL.
DEFINE VARIABLE p-220          AS INT.
DEFINE VARIABLE out-type       AS INTEGER INIT 1.
DEFINE VARIABLE transfered     AS LOGICAL INITIAL NO.
DEFINE VARIABLE to-stock       AS INTEGER.
DEFINE VARIABLE lager-bezeich  AS CHAR.
DEFINE VARIABLE lager-bez1     AS CHAR.
DEFINE VARIABLE curr-pos       AS INTEGER.
DEFINE VARIABLE t-amount       AS DECIMAL.
DEFINE VARIABLE lscheinnr      LIKE l-op.lscheinnr.
DEFINE VARIABLE sr-remark      AS CHARACTER.

DEF INPUT PARAMETER TABLE FOR payload-list.
DEF OUTPUT PARAMETER TABLE FOR op-list.
DEF OUTPUT PARAMETER TABLE FOR response-list.
/*DEF OUTPUT PARAMETER TABLE FOR t-l-lager.*/

/* Rulita 060225 | Fixing IF AVAILABLE serverless issue git 544*/
FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR. 
IF AVAILABLE bediener THEN
DO:
    IF SUBSTR(bediener.permissions, 22, 1) NE "0" THEN show-price = YES. 
END.

FIND FIRST htparam WHERE htparam.paramnr = 43 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN
DO:
    show-price = htparam.flogical.
END.

FIND FIRST htparam WHERE paramnr = 475 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN
DO:
    req-flag = NOT htparam.flogical. 
END.
 
FIND FIRST htparam WHERE paramnr = 220 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN
DO:
    p-220 = htparam.finteger.
END.
/* End Rulita */

/*
FOR EACH l-lager NO-LOCK:
    CREATE t-l-lager.
    BUFFER-COPY l-lager TO t-l-lager.
END.
*/

FIND FIRST payload-list NO-LOCK NO-ERROR.
IF AVAILABLE payload-list THEN
DO:
    ASSIGN
        user-init = payload-list.user-init
        t-lschein = payload-list.t-lschein
    .

    t-datum   = DATE(INTEGER(SUBSTRING(payload-list.t-datum, 1, 2)), 
                     INTEGER(SUBSTRING(payload-list.t-datum, 4, 2)), 
                     2000 + INTEGER(SUBSTRING(payload-list.t-datum, 7, 2))).


    RUN read-data.

    CREATE response-list.
    ASSIGN
        response-list.deptname      = deptname     
        response-list.curr-lager    = curr-lager   
        response-list.deptNo        = deptNo       
        response-list.show-price    = show-price   
        response-list.req-flag      = req-flag     
        response-list.p-220         = p-220        
        response-list.out-type      = out-type     
        response-list.transfered    = transfered   
        response-list.to-stock      = to-stock     
        response-list.lager-bezeich = lager-bezeich
        response-list.lager-bez1    = lager-bez1   
        response-list.curr-pos      = curr-pos     
        response-list.t-amount      = t-amount     
        response-list.lscheinnr     = lscheinnr    
        response-list.sr-remark     = sr-remark      
    .
END.

PROCEDURE read-data:
    ASSIGN lscheinnr = t-lschein.
    FIND FIRST l-op WHERE l-op.datum = t-datum 
        AND l-op.lscheinnr = t-lschein AND l-op.pos GT 0 NO-LOCK NO-ERROR.
    /* Rulita 060225 | Fixing IF AVAILABLE serverless issue git 544*/
    IF AVAILABLE l-op THEN
    DO: 
        ASSIGN 
            curr-lager = l-op.lager-nr              /* Rulita 060225 | Fixing from l-op.lager to l-op.larger-nr serverless issue git 544*/
            deptNo     = l-op.reorgflag
        .
        FIND FIRST parameters WHERE parameters.progname = "CostCenter" 
            AND parameters.section = "Name" AND INTEGER(parameters.varname) = deptNo 
            NO-LOCK NO-ERROR. 
        IF AVAILABLE parameters THEN deptname = parameters.vstring. 
        IF l-op.op-art = 14 THEN 
            ASSIGN
                transfered = YES
                out-type   = 1
                to-stock   = l-op.pos
            .
        ELSE out-type = 2.
    
        FIND FIRST l-lager WHERE l-lager.lager-nr = curr-lager NO-LOCK NO-ERROR.
        IF AVAILABLE l-lager THEN
        DO:
            lager-bezeich = l-lager.bezeich.
            IF to-stock NE 0 THEN
            DO:
                FIND FIRST l-lager WHERE l-lager.lager-nr = to-stock NO-LOCK NO-ERROR.
                IF AVAILABLE l-lager THEN lager-bez1 = l-lager.bezeich.
            END.
        END.

        /* Oscar (14/03/25) - 3E510E - show field sr-remark */
        FIND FIRST queasy WHERE queasy.KEY EQ 343 
            AND queasy.char1 EQ t-lschein NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            sr-remark = queasy.char2.
        END.
    
        FOR EACH l-op WHERE l-op.datum = t-datum 
            AND l-op.lscheinnr = t-lschein AND l-op.pos GT 0 
            AND l-op.loeschflag LE 1 NO-LOCK BY l-op.pos:

            CREATE op-list.
            BUFFER-COPY l-op TO op-list.
            FIND FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK NO-ERROR.
            FIND FIRST sys-user WHERE sys-user.nr = l-op.fuellflag NO-LOCK NO-ERROR.
            FIND FIRST l-bestand WHERE l-bestand.artnr = l-op.artnr
                AND l-bestand.lager-nr = curr-lager NO-LOCK NO-ERROR.

            IF AVAILABLE sys-user THEN op-list.username = sys-user.username.
            IF AVAILABLE l-artikel THEN op-list.bezeich  = l-artikel.bezeich.

            ASSIGN
                op-list.new-flag = NO
                curr-pos         = l-op.pos
                t-amount         = t-amount + l-op.warenwert
            .

            IF AVAILABLE l-bestand THEN 
                op-list.onhand = l-bestand.anz-anf-best
                               + l-bestand.anz-eingang - l-bestand.anz-ausgang.
        END.
    END.
    /* End Rulita */
END.
