DEFINE TEMP-TABLE op-list LIKE l-op 
    FIELD bezeich  AS CHAR FORMAT "x(36)"             COLUMN-LABEL "Description" 
    FIELD username AS CHAR FORMAT "x(16)"             COLUMN-LABEL "Created by" 
    FIELD onhand   AS DECIMAL FORMAT "->,>>>,>>9.99"  COLUMN-LABEL "On-Hand"
    FIELD anzahl0  AS DECIMAL
    FIELD fibu     AS CHAR
    FIELD fibu10   AS CHAR
    FIELD s-recid  AS INTEGER
    FIELD einheit  AS CHAR FORMAT "x(3)".

/* Oscar (14/03/25) - 3E510E - change payload format*/
DEFINE TEMP-TABLE payload-list 
    FIELD t-lschein AS CHARACTER
    FIELD t-datum   AS CHARACTER
    FIELD t-amount  AS DECIMAL
    FIELD lscheinnr AS CHARACTER
.

/* Oscar (14/03/25) - 3E510E - change response format and add new field sr-remark */
DEFINE TEMP-TABLE response-list
    FIELD t-amount      AS DECIMAL
    FIELD lscheinnr     AS CHARACTER
    FIELD curr-lager    AS INTEGER
    FIELD deptNo        AS INTEGER
    FIELD transfered    AS LOGICAL
    FIELD out-type      AS INTEGER
    FIELD to-stock      AS INTEGER
    FIELD deptname      AS CHARACTER
    FIELD lager-bezeich AS CHARACTER
    FIELD lager-bez1    AS CHARACTER
    FIELD curr-pos      AS INTEGER
    FIELD sr-remark     AS CHARACTER
.

DEF VAR t-lschein    AS CHAR.
DEF VAR t-datum      AS DATE.
DEF VAR t-amount     AS DECIMAL.
DEF VAR lscheinnr    AS CHAR.

DEF VAR curr-lager    AS INT.
DEF VAR deptNo        AS INT.
DEF VAR transfered    AS LOGICAL.
DEF VAR out-type      AS INT.
DEF VAR to-stock      AS INT.
DEF VAR deptname      AS CHAR.
DEF VAR lager-bezeich AS CHAR.
DEF VAR lager-bez1    AS CHAR.
DEF VAR curr-pos      AS INT.
DEF VAR sr-remark     AS CHAR.

DEF INPUT PARAMETER TABLE FOR payload-list.
DEF OUTPUT PARAMETER TABLE FOR op-list.
DEF OUTPUT PARAMETER TABLE FOR response-list.

DEFINE BUFFER sys-user FOR bediener. 

FIND FIRST payload-list NO-LOCK NO-ERROR.
IF AVAILABLE payload-list THEN
DO:
    ASSIGN
        t-lschein = payload-list.t-lschein
        t-amount  = payload-list.t-amount 
        lscheinnr = payload-list.lscheinnr
    .

    t-datum   = DATE(INTEGER(SUBSTRING(payload-list.t-datum, 1, 2)), 
                     INTEGER(SUBSTRING(payload-list.t-datum, 4, 2)), 
                     2000 + INTEGER(SUBSTRING(payload-list.t-datum, 7, 2))).


    RUN read-data.

    CREATE response-list.
    ASSIGN
        response-list.t-amount      = t-amount 
        response-list.lscheinnr     = lscheinnr
        response-list.curr-lager    = curr-lager   
        response-list.deptNo        = deptNo       
        response-list.transfered    = transfered   
        response-list.out-type      = out-type     
        response-list.to-stock      = to-stock     
        response-list.deptname      = deptname     
        response-list.lager-bezeich = lager-bezeich
        response-list.lager-bez1    = lager-bez1   
        response-list.curr-pos      = curr-pos     
        response-list.sr-remark     = sr-remark    
    .
END.

PROCEDURE read-data:
    ASSIGN lscheinnr = t-lschein.
    FIND FIRST l-op WHERE l-op.datum = t-datum 
        AND l-op.lscheinnr = t-lschein AND l-op.pos GT 0 NO-LOCK NO-ERROR.
    /* Rulita 060225 | Fixing IF AVAILABLE serverless issue git 542*/
    IF AVAILABLE l-op THEN
    DO: 
        ASSIGN 
            curr-lager = l-op.lager-nr            /* Rulita 060225 | Fixing serverless from lager to lager-nr issue git 542*/
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
        IF AVAILABLE l-lager THEN lager-bezeich = l-lager.bezeich.              /* Rulita 070225 | Fixing serverless issue git 542*/

        IF to-stock NE 0 THEN
        DO:
            FIND FIRST l-lager WHERE l-lager.lager-nr = to-stock NO-LOCK NO-ERROR.
            IF AVAILABLE l-lager THEN lager-bez1 = l-lager.bezeich.              /* Rulita 070225 | Fixing serverless issue git 542*/
        END.

        FOR EACH l-op WHERE l-op.datum = t-datum 
            AND l-op.lscheinnr = t-lschein AND l-op.pos GT 0 
            AND l-op.loeschflag = 0 /*IT*/
            NO-LOCK BY l-op.pos:

            CREATE op-list.
            BUFFER-COPY l-op TO op-list.
      
            FIND FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK NO-ERROR.
            IF AVAILABLE l-artikel THEN 
            DO:
                op-list.bezeich  = l-artikel.bezeich.
                op-list.einheit  = l-artikel.masseinheit.              /* Rulita 070225 | Fixing serverless issue git 542*/
            END.

            FIND FIRST sys-user WHERE sys-user.nr = l-op.fuellflag NO-LOCK NO-ERROR.
            IF AVAILABLE sys-user THEN op-list.username = sys-user.username. /*NA*/            /* Rulita 070225 | Fixing serverless issue git 542*/

            FIND FIRST l-bestand WHERE l-bestand.artnr = l-op.artnr
                AND l-bestand.lager-nr = curr-lager NO-LOCK NO-ERROR.

            ASSIGN
                op-list.s-recid  = INTEGER(RECID(l-op))
                op-list.anzahl0  = l-op.anzahl
                op-list.fibu     = l-op.stornogrund
                op-list.fibu10   = l-op.stornogrund
                curr-pos         = l-op.pos
                t-amount         = t-amount + l-op.warenwert
            .

            IF AVAILABLE l-bestand THEN op-list.onhand = l-bestand.anz-anf-best
                                                       + l-bestand.anz-eingang - l-bestand.anz-ausgang.

            FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-op.stornogrund
                NO-LOCK NO-ERROR.
            IF NOT AVAILABLE gl-acct THEN
                FIND FIRST gl-acct WHERE gl-acct.bezeich = l-op.stornogrund
                NO-LOCK NO-ERROR.
            IF AVAILABLE gl-acct THEN
                ASSIGN
                    op-list.fibu = gl-acct.fibukonto
                    op-list.fibu10 = gl-acct.fibukonto
                    op-list.stornogrund = gl-acct.bezeich.
        END.

        /* Oscar (14/03/25) - 3E510E - show field sr-remark */
        FIND FIRST queasy WHERE queasy.KEY EQ 343 
            AND queasy.char1 EQ t-lschein NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            sr-remark = queasy.char2.
        END.
    END.
    /* End Rulita */
END.
