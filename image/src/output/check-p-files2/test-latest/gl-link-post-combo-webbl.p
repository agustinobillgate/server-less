/*FDL August 21, 2023 - for web combbo transfer to GL*/

DEFINE TEMP-TABLE g-list 
    FIELD  flag             AS INTEGER 
    FIELD  datum            AS DATE 
    FIELD  artnr            AS INTEGER 
    FIELD  dept             AS INTEGER 
    FIELD  jnr              LIKE gl-journal.jnr 
    FIELD  fibukonto        LIKE gl-journal.fibukonto 
    FIELD  debit            LIKE gl-journal.debit   FORMAT ">,>>>,>>>,>>9.99"
    FIELD  credit           LIKE gl-journal.credit FORMAT ">,>>>,>>>,>>9.99"
    FIELD  bemerk           AS CHAR FORMAT "x(32)" 
    FIELD  userinit         LIKE gl-journal.userinit 
    FIELD  sysdate          LIKE gl-journal.sysdate INITIAL today 
    FIELD  zeit             LIKE gl-journal.zeit 
    FIELD  chginit          LIKE gl-journal.chginit 
    FIELD  chgdate          LIKE gl-journal.chgdate INITIAL ? 
    FIELD  duplicate        AS LOGICAL INITIAL YES
    FIELD  acct-fibukonto   LIKE gl-acct.fibukonto
    FIELD  bezeich          LIKE gl-acct.bezeich. 

DEFINE TEMP-TABLE g2-list 
    FIELD  flag             AS INTEGER 
    FIELD  datum            AS DATE 
    FIELD  artnr            AS INTEGER 
    FIELD  dept             AS INTEGER 
    FIELD  jnr              LIKE gl-journal.jnr 
    FIELD  fibukonto        LIKE gl-journal.fibukonto 
    FIELD  debit            LIKE gl-journal.debit   FORMAT ">,>>>,>>>,>>9.99"
    FIELD  credit           LIKE gl-journal.credit FORMAT ">,>>>,>>>,>>9.99"
    FIELD  bemerk           AS CHAR FORMAT "x(32)" 
    FIELD  userinit         LIKE gl-journal.userinit 
    FIELD  sysdate          LIKE gl-journal.sysdate INITIAL today 
    FIELD  zeit             LIKE gl-journal.zeit 
    FIELD  chginit          LIKE gl-journal.chginit 
    FIELD  chgdate          LIKE gl-journal.chgdate INITIAL ? 
    FIELD  duplicate        AS LOGICAL INITIAL YES
    FIELD  acct-fibukonto   LIKE gl-acct.fibukonto
    FIELD  bezeich          LIKE gl-acct.bezeich. 

DEFINE TEMP-TABLE combo-glist 
    FIELD  flag             AS INTEGER 
    FIELD  datum            AS DATE 
    FIELD  artnr            AS INTEGER 
    FIELD  dept             AS INTEGER 
    FIELD  jnr              LIKE gl-journal.jnr 
    FIELD  fibukonto        LIKE gl-journal.fibukonto 
    FIELD  debit            LIKE gl-journal.debit   FORMAT ">,>>>,>>>,>>9.99"
    FIELD  credit           LIKE gl-journal.credit FORMAT ">,>>>,>>>,>>9.99"
    FIELD  bemerk           AS CHAR FORMAT "x(32)" 
    FIELD  userinit         LIKE gl-journal.userinit 
    FIELD  sysdate          LIKE gl-journal.sysdate INITIAL today 
    FIELD  zeit             LIKE gl-journal.zeit 
    FIELD  chginit          LIKE gl-journal.chginit 
    FIELD  chgdate          LIKE gl-journal.chgdate INITIAL ? 
    FIELD  duplicate        AS LOGICAL INITIAL YES
    FIELD  acct-fibukonto   LIKE gl-acct.fibukonto
    FIELD  bezeich          LIKE gl-acct.bezeich. 

DEFINE TEMP-TABLE ar-glist 
    FIELD  rechnr           AS INTEGER 
    FIELD  dept             AS INTEGER 
    FIELD  jnr              LIKE gl-journal.jnr 
    FIELD  fibukonto        LIKE gl-journal.fibukonto 
    FIELD  debit            LIKE gl-journal.debit 
    FIELD  credit           LIKE gl-journal.credit 
    FIELD  bemerk           AS CHAR FORMAT "x(50)" 
    FIELD  userinit         LIKE gl-journal.userinit 
    FIELD  sysdate          LIKE gl-journal.sysdate INITIAL today 
    FIELD  zeit             LIKE gl-journal.zeit 
    FIELD  chginit          LIKE gl-journal.chginit 
    FIELD  chgdate          LIKE gl-journal.chgdate INITIAL ? 
    FIELD  duplicate        AS LOGICAL INITIAL YES 
    FIELD  add-info         AS CHAR 
    FIELD  counter          AS INTEGER
    FIELD  acct-fibukonto   LIKE gl-acct.fibukonto
    FIELD  bezeich          LIKE gl-acct.bezeich.

DEFINE TEMP-TABLE ar-g2list 
    FIELD  rechnr           AS INTEGER 
    FIELD  dept             AS INTEGER 
    FIELD  jnr              LIKE gl-journal.jnr 
    FIELD  fibukonto        LIKE gl-journal.fibukonto 
    FIELD  debit            LIKE gl-journal.debit 
    FIELD  credit           LIKE gl-journal.credit 
    FIELD  bemerk           AS CHAR FORMAT "x(50)" 
    FIELD  userinit         LIKE gl-journal.userinit 
    FIELD  sysdate          LIKE gl-journal.sysdate INITIAL today 
    FIELD  zeit             LIKE gl-journal.zeit 
    FIELD  chginit          LIKE gl-journal.chginit 
    FIELD  chgdate          LIKE gl-journal.chgdate INITIAL ? 
    FIELD  duplicate        AS LOGICAL INITIAL YES 
    FIELD  add-info         AS CHAR 
    FIELD  counter          AS INTEGER
    FIELD  acct-fibukonto   LIKE gl-acct.fibukonto
    FIELD  bezeich          LIKE gl-acct.bezeich. 

DEFINE TEMP-TABLE combo-ar-glist 
    FIELD  rechnr           AS INTEGER 
    FIELD  dept             AS INTEGER 
    FIELD  jnr              LIKE gl-journal.jnr 
    FIELD  fibukonto        LIKE gl-journal.fibukonto 
    FIELD  debit            LIKE gl-journal.debit 
    FIELD  credit           LIKE gl-journal.credit 
    FIELD  bemerk           AS CHAR FORMAT "x(50)" 
    FIELD  userinit         LIKE gl-journal.userinit 
    FIELD  sysdate          LIKE gl-journal.sysdate INITIAL today 
    FIELD  zeit             LIKE gl-journal.zeit 
    FIELD  chginit          LIKE gl-journal.chginit 
    FIELD  chgdate          LIKE gl-journal.chgdate INITIAL ? 
    FIELD  duplicate        AS LOGICAL INITIAL YES 
    FIELD  add-info         AS CHAR 
    FIELD  counter          AS INTEGER
    FIELD  acct-fibukonto   LIKE gl-acct.fibukonto
    FIELD  bezeich          LIKE gl-acct.bezeich.

DEFINE TEMP-TABLE trans-dept
    FIELD nr AS INTEGER.

DEFINE TEMP-TABLE t-htparam LIKE htparam.

DEFINE TEMP-TABLE s2-list 
    FIELD fibukonto   LIKE gl-acct.fibukonto 
    FIELD bezeich     AS CHAR FORMAT "x(28)" 
    FIELD credit      AS DECIMAL FORMAT ">>>,>>>,>>>,>>9.99" 
    FIELD debit       AS DECIMAL FORMAT ">>>,>>>,>>>,>>9.99". 

DEFINE INPUT PARAMETER TABLE FOR g-list. /*vhpIA*/
DEFINE INPUT PARAMETER TABLE FOR ar-glist. /*vhpAR*/
DEFINE INPUT PARAMETER TABLE FOR trans-dept.
DEFINE INPUT PARAMETER language-code    AS INTEGER.   
DEFINE INPUT PARAMETER vKey             AS CHARACTER.
DEFINE INPUT PARAMETER vModule          AS CHARACTER. /*vhpIA|vhpAR*/
DEFINE INPUT PARAMETER combo-gastnr     AS INTEGER.   /*Param 155*/
DEFINE INPUT PARAMETER user-init        AS CHARACTER.
DEFINE INPUT PARAMETER pf-file1         AS CHARACTER. /*Param 339*/
DEFINE INPUT PARAMETER pf-file2         AS CHARACTER. /*Param 340*/
DEFINE INPUT PARAMETER from-date        AS DATE.
DEFINE INPUT PARAMETER to-date          AS DATE.
DEFINE INPUT PARAMETER refno            AS CHARACTER.
DEFINE INPUT PARAMETER bezeich          AS CHARACTER.
DEFINE INPUT PARAMETER curr-anz1        AS INTEGER.
DEFINE INPUT PARAMETER debit1           AS DECIMAL.
DEFINE INPUT PARAMETER credit1          AS DECIMAL.
DEFINE INPUT PARAMETER merge-flag       AS LOGICAL. /*vhpAR*/
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR g2-list.    /*vhpIA*/
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR ar-g2list.  /*vhpAR*/
DEFINE INPUT-OUTPUT PARAMETER debits    AS DECIMAL.
DEFINE INPUT-OUTPUT PARAMETER credits   AS DECIMAL.
DEFINE INPUT-OUTPUT PARAMETER remains   AS DECIMAL.
DEFINE OUTPUT PARAMETER frame-title2    AS CHARACTER.
DEFINE OUTPUT PARAMETER last-acctdate   AS DATE.
DEFINE OUTPUT PARAMETER curr-anz        AS INTEGER.
DEFINE OUTPUT PARAMETER created         AS LOGICAL.
DEFINE OUTPUT PARAMETER message-result  AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE FOR s2-list.

DEFINE VARIABLE connect-param       AS CHAR    NO-UNDO.
DEFINE VARIABLE connect-paramSSL    AS CHAR   NO-UNDO.
DEFINE VARIABLE lreturn             AS LOGICAL NO-UNDO INIT NO.
DEFINE VARIABLE htl-name            AS CHARACTER.
DEFINE VARIABLE hServer             AS HANDLE NO-UNDO.
DEFINE VARIABLE debit2              AS DECIMAL.
DEFINE VARIABLE credit2             AS DECIMAL.
DEFINE VARIABLE curr-anz2           AS INTEGER INIT 0.
DEFINE VARIABLE remain2             AS DECIMAL.
DEFINE VARIABLE acct-error          AS INTEGER INIT 0.
DEFINE VARIABLE art-dpt             AS INTEGER.
DEFINE VARIABLE art-artnr           AS INTEGER.
DEFINE VARIABLE art-bezeich         AS CHARACTER.
DEFINE VARIABLE success-flag        AS LOGICAL NO-UNDO.
DEFINE VARIABLE err-flag            AS LOGICAL NO-UNDO.

/*********************************************************************************************/
CREATE SERVER hServer.

/*Validation First*/
IF pf-file1 EQ "" OR pf-file1 EQ ? THEN
DO:
    message-result = "01 - Param 339 is unfilled.".
END.
ELSE IF pf-file2 EQ "" OR pf-file2 EQ ? THEN
DO:
    message-result = "02 - Param 340 is unfilled.".
END.
ELSE IF combo-gastnr EQ 0 OR combo-gastnr EQ ? THEN
DO:
    message-result = "03 - Param 155 is unfilled.".
END.

IF refno EQ ? THEN refno = "".
IF bezeich EQ ? THEN bezeich = "".

/*Process*/
IF vModule EQ "vhpIA" THEN
DO:
    IF vKey EQ "createJournalListIA" THEN
    DO:
        /*Connect to Other DB*/
        connect-param = "-H " + ENTRY(1, pf-file2, ":") + " -S "
            + ENTRY(2, pf-file2, ":") 
            + " -DirectConnect -sessionModel Session-free".
        connect-paramSSL = connect-param + " -ssl -nohostverify".
    
        lreturn = hServer:CONNECT(connect-paramSSL, ?, ?, ?) NO-ERROR.
        IF NOT lreturn THEN lreturn = hServer:CONNECT(connect-param, ?, ?, ?) NO-ERROR.
    
        IF lreturn THEN RUN read-hotelnamebl.p ON hServer ("A120", OUTPUT htl-name).
    
        frame-title2 = htl-name + " - " + "F/O Journal Transfer to GL".
        RUN gl-linkfobl.p
            ON hServer(INPUT TABLE trans-dept, from-date, to-date, user-init, refno,
                        INPUT-OUTPUT curr-anz2, OUTPUT debit2, OUTPUT credit2,
                        OUTPUT acct-error, OUTPUT remain2, 
                        OUTPUT art-dpt, OUTPUT art-artnr, OUTPUT art-bezeich,
                        OUTPUT TABLE g2-list).
    
        /*Disconnect Other DB*/
        hServer:DISCONNECT() NO-ERROR. 
    
        IF acct-error EQ 1 THEN
        DO:
            message-result = "04 - COMBO DB: Reference number already exists.".
            RETURN.
        END.        
        ELSE IF acct-error EQ 2 THEN
        DO:
            message-result = "05 - COMBO DB: G/L AcctNo not found for the following article:"
                + CHR(10) 
                + STRING(art-dpt,"99 ") + STRING(art-artnr) + " - " + art-bezeich.
            RETURN.
        END.
            
        ASSIGN 
            debits   = debit1   + debit2
            credits  = credit1  + credit2
            curr-anz = curr-anz1 + curr-anz2
            .
    
        IF curr-anz EQ 0 THEN
        DO:
            message-result = "06 - No GL journals have been created.".
            RETURN.
        END.
        IF from-date EQ (last-acctdate + 1) THEN created = YES.
        ELSE created = NO.
    END.
    ELSE IF vKey EQ "postJournalListIA" THEN
    DO:
        FOR EACH combo-glist:
            DELETE combo-glist.
        END.

        FOR EACH g-list:
            CREATE combo-glist.
            BUFFER-COPY g-list TO combo-glist.
        END.

        FOR EACH g2-list:
            CREATE combo-glist.
            BUFFER-COPY g2-list TO combo-glist.
        END.

        /*Check COA*/
        FOR EACH combo-glist:
            FIND FIRST gl-acct WHERE gl-acct.fibukonto EQ combo-glist.fibukonto NO-LOCK NO-ERROR.
            IF NOT AVAILABLE gl-acct THEN
            DO:
                message-result = "COA " + combo-glist.fibukonto + " not found.".
                err-flag = YES.
                LEAVE.
            END.
        END.
        IF err-flag THEN RETURN.

        RUN gl-linkfo-updatebl.p(language-code, remains, credits, debits, 
            to-date, refno, bezeich, INPUT TABLE combo-glist).

        /*Connect to Other DB*/
        connect-param = "-H " + ENTRY(1, pf-file2, ":") + " -S "
            + ENTRY(2, pf-file2, ":") 
            + " -DirectConnect -sessionModel Session-free".
        connect-paramSSL = connect-param + " -ssl -nohostverify".
    
        lreturn = hServer:CONNECT(connect-paramSSL, ?, ?, ?) NO-ERROR.
        IF NOT lreturn THEN lreturn = hServer:CONNECT(connect-param, ?, ?, ?) NO-ERROR.
    
        IF lreturn THEN RUN read-hotelnamebl.p ON hServer ("A120", OUTPUT htl-name).

        FIND FIRST t-htparam NO-ERROR.
        IF NOT AVAILABLE t-htparam THEN CREATE t-htparam.
        ASSIGN
            t-htparam.paramnr = 1003
            t-htparam.fdate   = to-date
        .
        RUN write-htparambl.p ON hServer (2, TABLE t-htparam, OUTPUT success-flag).

        /*Disconnect Other DB*/
        hServer:DISCONNECT() NO-ERROR.

        message-result = "Transfer to GL Success.".
    END.
END.
ELSE IF vModule EQ "vhpAR" THEN
DO:
    IF vKey EQ "createJournalListAR" THEN
    DO:
        /*Connect to Other DB*/
        connect-param = "-H " + ENTRY(1, pf-file2, ":") + " -S "
            + ENTRY(2, pf-file2, ":") 
            + " -DirectConnect -sessionModel Session-free".
        connect-paramSSL = connect-param + " -ssl -nohostverify".
    
        lreturn = hServer:CONNECT(connect-paramSSL, ?, ?, ?) NO-ERROR.
        IF NOT lreturn THEN lreturn = hServer:CONNECT(connect-param, ?, ?, ?) NO-ERROR.
    
        IF lreturn THEN RUN read-hotelnamebl.p ON hServer ("A120", OUTPUT htl-name).
    
        frame-title2 = htl-name + " - " + "A/R Journal Transfer to GL".
        RUN gl-linkarbl.p
            ON hServer(merge-flag, from-date, to-date, user-init, refno,
                        INPUT-OUTPUT curr-anz2, OUTPUT acct-error, OUTPUT debit2,
                        OUTPUT credit2, OUTPUT remain2, OUTPUT TABLE ar-g2list,
                        OUTPUT TABLE s2-list,
                        OUTPUT art-artnr, OUTPUT art-bezeich).
    
        /*Disconnect Other DB*/
        hServer:DISCONNECT() NO-ERROR. 
    
        IF acct-error EQ 1 THEN
        DO:
            message-result = "04 - COMBO DB: Reference number already exists.".
            RETURN.
        END.        
        ELSE IF acct-error EQ 2 THEN
        DO:
            message-result = "05 - COMBO DB: Chart of Account not defined."
                + CHR(10) 
                + "Article No " + STRING(art-artnr) + " - " + art-bezeich.
            RETURN.
        END.                    
    
        curr-anz = curr-anz1 + curr-anz2.
        IF (curr-anz1 + curr-anz2) EQ 0 THEN
        DO:
            message-result = "06 - A/R payment records missing." 
                + CHR(10) + "No GL journals have been created.".
            RETURN.
        END.
        created = YES.

        FOR EACH ar-glist:
            debits = debits + ar-glist.debit.
            credits = credits + ar-glist.credit.
        END.
        FOR EACH ar-g2list:
            debits = debits + ar-g2list.debit.
            credits = credits + ar-g2list.credit.
        END.
    END.
    ELSE IF vKey EQ "postJournalListAR" THEN
    DO:
        FOR EACH combo-ar-glist:
            DELETE combo-ar-glist.
        END.

        FOR EACH ar-glist:
            CREATE combo-ar-glist.
            BUFFER-COPY ar-glist TO combo-ar-glist.
        END.

        FOR EACH ar-g2list:
            CREATE combo-ar-glist.
            BUFFER-COPY ar-g2list TO combo-ar-glist.
        END.

        /*Check COA*/
        FOR EACH ar-g2list:
            FIND FIRST gl-acct WHERE gl-acct.fibukonto EQ ar-g2list.fibukonto NO-LOCK NO-ERROR.
            IF NOT AVAILABLE gl-acct THEN
            DO:
                message-result = "COA " + ar-g2list.fibukonto + " not found.".
                err-flag = YES.
                LEAVE.
            END.
        END.
        IF err-flag THEN RETURN.

        RUN gl-linkar-updatebl.p (language-code, remains, credits, debits, to-date,
            refno, bezeich, to-date, INPUT TABLE combo-ar-glist).

        /*Connect to Other DB*/
        connect-param = "-H " + ENTRY(1, pf-file2, ":") + " -S "
            + ENTRY(2, pf-file2, ":") 
            + " -DirectConnect -sessionModel Session-free".
        connect-paramSSL = connect-param + " -ssl -nohostverify".
    
        lreturn = hServer:CONNECT(connect-paramSSL, ?, ?, ?) NO-ERROR.
        IF NOT lreturn THEN lreturn = hServer:CONNECT(connect-param, ?, ?, ?) NO-ERROR.
    
        IF lreturn THEN RUN read-hotelnamebl.p ON hServer ("A120", OUTPUT htl-name).

        FIND FIRST t-htparam NO-ERROR.
        IF NOT AVAILABLE t-htparam THEN CREATE t-htparam.
        ASSIGN
            t-htparam.paramnr = 1014
            t-htparam.fdate   = to-date
        .
        RUN write-htparambl.p ON hServer (2, TABLE t-htparam, OUTPUT success-flag).

        /*Disconnect Other DB*/
        hServer:DISCONNECT() NO-ERROR.

        message-result = "Transfer to GL Success.".
    END.
END.

