/* Global Variables & Initial Values */
DEFINE VARIABLE lacm AS DATE. /* Last Accounting Closing Month */
FIND FIRST htparam WHERE htparam.paramnr = 558.
ASSIGN
    lacm = htparam.fdate.
DEFINE VARIABLE slacm AS CHARACTER.

DEFINE VARIABLE cacm AS DATE. /* Current Accounting Closing Month */
FIND FIRST htparam WHERE htparam.paramnr = 597.
ASSIGN
    cacm = htparam.fdate.

DEFINE VARIABLE lacy AS DATE. /* Last Accounting Closing Year */
FIND FIRST htparam WHERE htparam.paramnr = 795.
ASSIGN
    lacy = htparam.fdate.

DEFINE VARIABLE WorkSelect AS INTEGER
    VIEW-AS RADIO-SET VERTICAL
    RADIO-BUTTONS
        "Re-Open Closed &Month", 1,
        "Re-Open Closed &Year", 2,
        "Restore CoA &Budget", 3
    NO-UNDO.

DEFINE BUTTON BtnExecute    LABEL "  &Execute  ".
DEFINE BUTTON BtnCancel     LABEL "  &Cancel   ".

DEFINE FRAME mainFrame
    WorkSelect      AT ROW  2     COLUMN  3       NO-LABELS
    BtnExecute      AT ROW  5     COLUMN  10
    BtnCancel       SKIP(1)
    WITH SIDE-LABELS CENTERED OVERLAY WIDTH 38 THREE-D
    VIEW-AS DIALOG-BOX TITLE "e1-VHP - G/L TOOLS".
/* End of Global Variables & Initial Values */

/* Button Click */
ON CHOOSE OF BtnExecute
DO:
    ASSIGN WorkSelect.
    IF WorkSelect = 1 THEN DO: /* R-Button 1 : Re-Open Closed Month */
        RUN ReOpenMonth(cacm, lacm, lacy).
    END.
    IF WorkSelect = 2 THEN DO: /* R-Button 2 : Re-Open Closed Year */
        RUN ReOpenYear(cacm, lacm, lacy).
    END.
    IF WorkSelect = 3 THEN DO: /* R-Button 3 : Restore CoA Budget */
        RUN RestoreCOABudget(lacy).
    END.
    RETURN.
END.

ON CHOOSE OF BtnCancel
DO:
    RETURN.
END.
/* End of Button Click */


/* Main PROCEDURE */
VIEW FRAME mainFrame.
ENABLE ALL WITH FRAME mainFrame.
WAIT-FOR CHOOSE OF BtnExecute, BtnCancel.
/* End of Main PROCEDURE */


/* Re-Open Closed Month PROCEDURES */
PROCEDURE ReOpenMonth:
    DEFINE INPUT PARAMETER cacm         AS DATE.
    DEFINE INPUT PARAMETER lacm         AS DATE.
    DEFINE INPUT PARAMETER lacy         AS DATE.

    DEFINE VARIABLE fDate               AS DATE.
    DEFINE VARIABLE tDate               AS DATE.
    DEFINE VARIABLE cMonth              AS INTEGER.
    DEFINE VARIABLE questAns            AS LOGICAL.

    DEFINE BUFFER gl-acctBUFF           FOR gl-acct.
    DEFINE BUFFER gl-jouhdrBUFF         FOR gl-jouhdr.
    DEFINE BUFFER gl-journalBUFF        FOR gl-journal.

    /* Re-Ask for Re-Open Closed Month */
    MESSAGE "Are you sure to Re-Open Closed Month "
        + STRING(lacm) + "?"
        VIEW-AS ALERT-BOX QUESTION BUTTONS YES-NO UPDATE questAns.

    IF questAns = NO THEN DO:
        RETURN.
    END.
    /* End of Re-Ask for Re-Open Closed Month */

    /* Parameters checking before Re-Open Closed Month */
    IF lacm <= lacy
        OR cacm <= lacm THEN DO:

        IF lacm = lacy THEN DO:
            MESSAGE "Incorrect Parameters! Please Re-Open Closed Year "
                + STRING(YEAR(lacy))
                + " before Re-Open Closed Month "
                + STRING(lacm)
                VIEW-AS ALERT-BOX INFORMATION.
            RETURN.
        END.
        MESSAGE "Incorrect Parameters!"
            SKIP "Current Closing Month : " + STRING(cacm)
            SKIP "Last Closing Month : " + STRING(lacm)
            SKIP "Last Closing Year : " + STRING(lacy)
            SKIP " "
            SKIP "Can't Re-Open Closed Month!"
            VIEW-AS ALERT-BOX INFORMATION.
        RETURN.
    END.
    /* End of Parameters checking before Re-Open Closed Month */
    /* Re-Open Closed Month */
    ASSIGN
        fDate  = DATE(MONTH(lacm),1,YEAR(lacm))
        tDate  = lacm
        cMonth = INTEGER(MONTH(lacm)).

    FIND FIRST gl-jouhdr WHERE gl-jouhdr.datum >= fDate
        AND gl-jouhdr.datum <= tDate
        NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE gl-jouhdr.
        FIND FIRST gl-jouhdrBUFF WHERE RECID(gl-jouhdrBUFF) = RECID(gl-jouhdr)
            EXCLUSIVE-LOCK.
        ASSIGN
            gl-jouhdrBUFF.BATCH      = YES
            gl-jouhdrBUFF.activeflag = 0.
        
        FIND FIRST gl-journal WHERE gl-journal.jnr = gl-jouhdr.jnr
            NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE gl-journal.
            FIND FIRST gl-journalBUFF WHERE RECID(gl-journalBUFF) = RECID(gl-journal)
                EXCLUSIVE-LOCK.
            ASSIGN
                gl-journalBUFF.activeflag = 0.

            RELEASE gl-journalBUFF.
            FIND NEXT gl-journal WHERE gl-journal.jnr = gl-jouhdr.jnr
                NO-LOCK NO-ERROR.
        END.
        IF gl-jouhdrBUFF.jtype = 0 THEN DO:
            ASSIGN
                gl-jouhdrBUFF.BATCH      = NO.
        END.

        RELEASE gl-jouhdrBUFF.
        FIND NEXT gl-jouhdr WHERE gl-jouhdr.datum >= fDate
            AND gl-jouhdr.datum <= tDate
            NO-LOCK NO-ERROR.
    END.

    FIND FIRST gl-acct NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE gl-acct.
        FIND FIRST gl-acctBUFF WHERE RECID(gl-acctBUFF) = RECID(gl-acct)
            EXCLUSIVE-LOCK.
        ASSIGN
            gl-acctBUFF.actual[cMonth] = 0.

        RELEASE gl-acctBUFF.
        FIND NEXT gl-acct NO-LOCK NO-ERROR.
    END.

    FIND FIRST htparam WHERE paramnr = 597. /* Current Closing Period */
    ASSIGN
        htparam.fdate = tDate.
    FIND FIRST htparam WHERE paramnr = 558. /* Last Closing Period */
    ASSIGN
        htparam.fdate = fDate - 1.

    MESSAGE "Re-Open Closed Month are Done"
        SKIP "Current Closing Date : " + STRING(tDate)
        VIEW-AS ALERT-BOX INFORMATION.
    /* End of Re-Open Closed Month */
    
    RETURN.
END.
/* End of Re-Open Closed Month PROCEDURES */



/* Re-Open Closed Year PROCEDURES */
PROCEDURE ReOpenYear:
    DEFINE INPUT PARAMETER cacm         AS DATE.
    DEFINE INPUT PARAMETER lacm         AS DATE.
    DEFINE INPUT PARAMETER lacy         AS DATE.

    DEFINE VARIABLE fDate               AS DATE.
    DEFINE VARIABLE tDate               AS DATE.
    DEFINE VARIABLE questAns            AS LOGICAL.
    DEFINE VARIABLE changeRE            AS LOGICAL INITIAL NO.
    DEFINE VARIABLE i                   AS INTEGER.

    DEFINE BUFFER gl-acctBUFF           FOR gl-acct.
    DEFINE BUFFER gl-jouhdrBUFF         FOR gl-jouhdr.
    DEFINE BUFFER gl-journalBUFF        FOR gl-journal.
    DEFINE BUFFER gl-accthisBUFF        FOR gl-accthis.
    DEFINE BUFFER gl-jhdrhisBUFF        FOR gl-jhdrhis.
    DEFINE BUFFER gl-jourhisBUFF        FOR gl-jourhis.

    /* Re-Ask for Re-Open Closed Year */
    MESSAGE "Are you sure to Re-Open Closed Year "
        + STRING(YEAR(lacy)) + "?"
        VIEW-AS ALERT-BOX QUESTION BUTTONS YES-NO UPDATE questAns.

    IF questAns = NO THEN DO:
        RETURN.
    END.

    MESSAGE "Are you want to change Retained Earning Account? "
        + "This will Re-Open Closed Month up to January "
        + STRING(YEAR(lacy)) + "!"
        VIEW-AS ALERT-BOX QUESTION BUTTONS YES-NO UPDATE questAns.

    IF questAns = YES THEN DO:
        ASSIGN
            changeRE = YES.
        MESSAGE "Change Retained Earning (RE) selected! "
        + "This will Re-Open Closed Month up to January "
        + STRING(YEAR(lacy)) + "!"
        VIEW-AS ALERT-BOX INFORMATION.
    END.
    /* End of Re-Ask for Re-Open Closed Year */

    /* Parameters checking before Re-Open Closed Year */
    IF YEAR(cacm) <= YEAR (lacy)
        OR YEAR(cacm) > (YEAR(lacy) + 1) THEN DO:
        MESSAGE "Incorrect Parameters!"
            SKIP "Current Closing Month : " + STRING(cacm)
            SKIP "Last Closing Month : " + STRING(lacm)
            SKIP "Last Closing Year : " + STRING(lacy)
            VIEW-AS ALERT-BOX INFORMATION.
        RETURN.
    END.

    IF cacm > DATE(01, 31, YEAR(lacy) + 1)
        AND lacm <> lacy THEN DO:
        MESSAGE "Please Re-Open Closed Month to JAN "
            + STRING(YEAR(lacy) + 1)
            + " before Re-Open Closed Year "
            + STRING(YEAR(lacy)) + "!"
            SKIP "Current Closing Month : " + STRING(cacm)
            SKIP "Last Closing Month : " + STRING(lacm)
            SKIP "Last Closing Year : " + STRING(lacy)
            VIEW-AS ALERT-BOX INFORMATION.
        RETURN.
    END.
    /* End of Parameters checking before Re-Open Closed Year */

    /* Transfer gl-jhdrhis & gl-jourhis to gl-jouhdr & gl-journal */
    /* Need this to Re-Open Close Year more than 2 years from current year */
    FIND FIRST gl-jhdrhis WHERE gl-jhdrhis.datum >= DATE(1, 1, YEAR(lacy))
        AND gl-jhdrhis.datum <= DATE(12, 31, YEAR(lacy))
        NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE gl-jhdrhis.
        CREATE gl-jouhdr.
        ASSIGN
            gl-jouhdr.datum      = gl-jhdrhis.datum
            gl-jouhdr.refno      = gl-jhdrhis.refno
            gl-jouhdr.bezeich    = gl-jhdrhis.bezeich
            gl-jouhdr.debit      = gl-jhdrhis.debit
            gl-jouhdr.credit     = gl-jhdrhis.credit
            gl-jouhdr.remain     = gl-jhdrhis.remain
            gl-jouhdr.jnr        = gl-jhdrhis.jnr
            gl-jouhdr.jtype      = gl-jhdrhis.jtype
            gl-jouhdr.activeflag = gl-jhdrhis.activeflag
            gl-jouhdr.BATCH      = gl-jhdrhis.BATCH.

        FIND FIRST gl-jourhis WHERE gl-jourhis.jnr = gl-jhdrhis.jnr
            NO-LOCK NO-ERROR.

        DO WHILE AVAILABLE gl-jourhis.
            CREATE gl-journal.
            ASSIGN
                gl-journal.fibukonto  = gl-jourhis.fibukonto
                gl-journal.jnr        = gl-jourhis.jnr
                gl-journal.debit      = gl-jourhis.debit
                gl-journal.credit     = gl-jourhis.credit
                gl-journal.bemerk     = gl-jourhis.bemerk
                gl-journal.userinit   = gl-jourhis.userinit
                gl-journal.sysdate    = gl-jourhis.sysdate
                gl-journal.zeit       = gl-jourhis.zeit
                gl-journal.chginit    = gl-jourhis.chginit
                gl-journal.chgdate    = gl-jourhis.chgdate
                gl-journal.activeflag = gl-jourhis.activeflag.

            FIND FIRST gl-jourhisBUFF WHERE RECID(gl-jourhisBUFF) = RECID(gl-jourhis)
                EXCLUSIVE-LOCK.

            DELETE gl-jourhisBUFF.
            RELEASE gl-jourhisBUFF.

            FIND NEXT gl-jourhis WHERE gl-jourhis.jnr = gl-jhdrhis.jnr
                NO-LOCK NO-ERROR.
        END.

        FIND FIRST gl-jhdrhisBUFF WHERE RECID(gl-jhdrhisBUFF) = RECID(gl-jhdrhis)
            EXCLUSIVE-LOCK.

        DELETE gl-jhdrhisBUFF.
        RELEASE gl-jhdrhisBUFF.

        FIND NEXT gl-jhdrhis WHERE gl-jhdrhis.datum >= DATE(1, 1, YEAR(lacy))
            AND gl-jhdrhis.datum <= DATE(12, 31, YEAR(lacy))
            NO-LOCK NO-ERROR.
    END.
    /* End of Transfer gl-jhdrhis & gl-jourhis to gl-jouhdr & gl-journal */

    /* Make CoA Budget backup to gl-accthis on Current Year + 1000 */
    FIND FIRST gl-acct WHERE gl-acct.budget[1] <> 0
        OR gl-acct.budget[1] <> 0
        OR gl-acct.budget[1] <> 0
        OR gl-acct.budget[1] <> 0
        OR gl-acct.budget[1] <> 0
        OR gl-acct.budget[1] <> 0
        OR gl-acct.budget[1] <> 0
        OR gl-acct.budget[1] <> 0
        OR gl-acct.budget[1] <> 0
        OR gl-acct.budget[1] <> 0
        OR gl-acct.budget[1] <> 0
        OR gl-acct.budget[1] <> 0
        NO-LOCK NO-ERROR.

    IF AVAILABLE gl-acct THEN DO:
        FIND FIRST gl-accthis WHERE gl-accthis.YEAR = INTEGER(YEAR(lacy) + 1001)
            NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE gl-accthis.
            FIND FIRST gl-accthisBUFF WHERE RECID(gl-accthisBUFF) = RECID(gl-accthis)
                EXCLUSIVE-LOCK.

            DELETE gl-accthisBUFF.
            RELEASE gl-accthisBUFF.

            FIND NEXT gl-accthis WHERE gl-accthis.YEAR = INTEGER(YEAR(lacy) + 1001)
                NO-LOCK NO-ERROR.
        END.

        FIND FIRST gl-acct NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE gl-acct.
            CREATE gl-accthis.
            ASSIGN
                gl-accthis.fibukonto  = gl-acct.fibukonto
                gl-accthis.YEAR       = INTEGER(YEAR(lacy) + 1001)
                gl-accthis.budget[1]  = gl-acct.budget[1]
                gl-accthis.budget[2]  = gl-acct.budget[2]
                gl-accthis.budget[3]  = gl-acct.budget[3]
                gl-accthis.budget[4]  = gl-acct.budget[4]
                gl-accthis.budget[5]  = gl-acct.budget[5]
                gl-accthis.budget[6]  = gl-acct.budget[6]
                gl-accthis.budget[7]  = gl-acct.budget[7]
                gl-accthis.budget[8]  = gl-acct.budget[8]
                gl-accthis.budget[9]  = gl-acct.budget[9]
                gl-accthis.budget[10] = gl-acct.budget[10]
                gl-accthis.budget[11] = gl-acct.budget[11]
                gl-accthis.budget[12] = gl-acct.budget[12].

            FIND NEXT gl-acct NO-LOCK NO-ERROR.
        END.
    END.
    /* End of Make CoA Budget backup to gl-accthis on Current Year + 1000 */

    /* Reset gl-acct actual, last year, budget and last year budget value */
    FIND FIRST gl-acct NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE gl-acct.
        FIND FIRST gl-acctBUFF WHERE RECID(gl-acctBUFF) = RECID(gl-acct)
            EXCLUSIVE-LOCK.
        DO i = 1 TO 12:
            ASSIGN
                gl-acctBUFF.actual[i]    = 0
                gl-acctBUFF.budget[i]    = 0
                gl-acctBUFF.last-yr[i]   = 0
                gl-acctBUFF.ly-budget[i] = 0.
        END.

        RELEASE gl-acctBUFF.
        FIND NEXT gl-acct NO-LOCK NO-ERROR.
    END.
    /* End of Reset gl-acct actual, last year, budget and last year budget value */

    /* Copy gl-accthis last year to gl-acct */
    /* December will be generated by running Trial Close Month */
    FIND FIRST gl-accthis WHERE gl-accthis.YEAR = YEAR(lacy)
        NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE gl-accthis.
        FIND FIRST gl-acct WHERE gl-acct.fibukonto = gl-accthis.fibukonto
            NO-LOCK NO-ERROR.
        IF NOT AVAILABLE gl-acct THEN DO:
            MESSAGE "Please contact VHP Technical Support. "
                + "Account No. " + STRING(gl-accthis.fibukonto) + "not available."
                VIEW-AS ALERT-BOX INFORMATION.
        END.
        IF AVAILABLE gl-acct THEN DO:
            FIND FIRST gl-acctBUFF WHERE RECID(gl-acctBUFF) = RECID(gl-acct)
                EXCLUSIVE-LOCK.

            DO i = 1 TO 12:
                ASSIGN
                    gl-acctBUFF.actual[i]    = gl-accthis.actual[i]
                    gl-acctBUFF.budget[i]    = gl-accthis.budget[i]
                    gl-acctBUFF.debit[i]     = gl-accthis.debit[i]
                    gl-acctBUFF.credit[i]    = gl-accthis.credit[i].

            END.
            ASSIGN
                gl-acctBUFF.actual[12] = 0
                gl-acctBUFF.b-flag     = gl-accthis.b-flag
                gl-acctBUFF.modifiable = gl-accthis.modifiable
                gl-acctBUFF.activeflag = gl-accthis.activeflag.

            RELEASE gl-acctBUFF.
        END.

        FIND NEXT gl-accthis WHERE gl-accthis.YEAR = YEAR(lacy)
            NO-LOCK NO-ERROR.
    END.

    FIND FIRST gl-accthis WHERE gl-accthis.YEAR = YEAR(lacy) - 1
        NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE gl-accthis.
        FIND FIRST gl-acct WHERE gl-acct.fibukonto = gl-accthis.fibukonto
            NO-LOCK NO-ERROR.
        IF NOT AVAILABLE gl-acct THEN DO:
            MESSAGE "Please contact VHP Technical Support. "
                + "Account No. " + STRING(gl-accthis.fibukonto) + "not available."
                VIEW-AS ALERT-BOX INFORMATION.
        END.
        IF AVAILABLE gl-acct THEN DO:
            FIND FIRST gl-acctBUFF WHERE RECID(gl-acctBUFF) = RECID(gl-acct)
                EXCLUSIVE-LOCK.

            DO i = 1 TO 12:
                ASSIGN
                    gl-acctBUFF.last-yr[i]   = gl-accthis.actual[i]
                    gl-acctBUFF.ly-budget[i] = gl-accthis.budget[i].

            END.

            RELEASE gl-acctBUFF.
        END.

        FIND NEXT gl-accthis WHERE gl-accthis.YEAR = YEAR(lacy) - 1
            NO-LOCK NO-ERROR.
    END.
    /* End of Copy gl-accthis last year to gl-acct */

    /* Open Journal */
    ASSIGN
        fDate = DATE(12, 1, YEAR(lacm))
        tDate = DATE(12, 31, YEAR(lacm)).
    IF changeRE = YES THEN DO:
        ASSIGN
            fDate = DATE(1, 1, YEAR(lacm)).
    END.

    FIND FIRST gl-jouhdr WHERE gl-jouhdr.datum >= fDate
        AND gl-jouhdr.datum <= tDate
        NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE gl-jouhdr.
        FIND FIRST gl-jouhdrBUFF WHERE RECID(gl-jouhdrBUFF) = RECID(gl-jouhdr)
            EXCLUSIVE-LOCK.
        ASSIGN
            gl-jouhdrBUFF.BATCH      = YES
            gl-jouhdrBUFF.activeflag = 0.
        FIND FIRST gl-journal WHERE gl-journal.jnr = gl-jouhdr.jnr
            NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE gl-journal.
            FIND FIRST gl-journalBUFF WHERE RECID(gl-journalBUFF) = RECID(gl-journal)
                EXCLUSIVE-LOCK.
            ASSIGN
                gl-journalBUFF.activeflag = 0.

            RELEASE gl-journalBUFF.
            FIND NEXT gl-journal WHERE gl-journal.jnr = gl-jouhdr.jnr
                NO-LOCK NO-ERROR.
        END.
        IF gl-jouhdrBUFF.jtype = 0 THEN DO:
            ASSIGN
                gl-jouhdrBUFF.BATCH = NO.
        END.

        RELEASE gl-jouhdrBUFF.
        FIND NEXT gl-jouhdr WHERE gl-jouhdr.datum >= fDate
            AND gl-jouhdr.datum <= tDate
            NO-LOCK NO-ERROR.
    END.

    IF changeRE = YES THEN DO:
        FIND FIRST gl-acct NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE gl-acct.
            FIND FIRST gl-acctBUFF WHERE RECID(gl-acctBUFF) = RECID(gl-acct)
                EXCLUSIVE-LOCK.
            DO i = 1 TO 11:
                ASSIGN
                    gl-acctBUFF.actual[i] = 0.
            END.
            
            RELEASE gl-acctBUFF.
            FIND NEXT gl-acct NO-LOCK NO-ERROR.
        END.
    END.
    
    FIND FIRST htparam WHERE paramnr = 597. /* Current Closing Period */
    ASSIGN
        htparam.fdate = DATE(MONTH(fDate), 1, YEAR(fDate)) + 31 - DAY(DATE(MONTH(fDate), 1, YEAR(fDate)) + 31).

    FIND FIRST htparam WHERE paramnr = 558. /* Last Closing Period */
    ASSIGN
        htparam.fdate = fDate - 1.

    FIND FIRST htparam WHERE htparam.paramnr = 795. /* Last Closing Year Period */
        ASSIGN
            htparam.fdate = DATE(12, 31, YEAR(lacy) - 1).
    /* End of Open Journal */

    MESSAGE "Re-Oped Closed Year " + STRING(YEAR(lacy)) + " are DONE. "
        SKIP "Please do TRIAL CLOSE MONTH to refresh "
        + "journal data data!"
        SKIP "Current Closing Month : "
        + STRING(DATE(MONTH(fDate), 1, YEAR(fDate)) + 31 - DAY(DATE(MONTH(fDate), 1, YEAR(fDate)) + 31))
        SKIP "Last Closing Month : "
        + STRING(fDate - 1)
        SKIP "Last Closing Year : "
        + STRING(DATE(12, 31, YEAR(lacy) - 1))
    VIEW-AS ALERT-BOX INFORMATION.

    RETURN.
END.
/* End of Re-Open Closed Year PROCEDURES */



/* Restore CoA Budget PROCEDURES */
PROCEDURE RestoreCOABudget:
    DEFINE INPUT PARAMETER lacy         AS DATE.

    DEFINE VARIABLE questAns            AS LOGICAL.
    DEFINE VARIABLE i                   AS INTEGER.

    DEFINE BUFFER gl-acctBUFF           FOR gl-acct.

    /* Re-Ask for Restore CoA Budget */
    MESSAGE "Are you sure want to Restore CoA Budget "
        + STRING(INT(YEAR(lacy)) + 1) + "?"
        SKIP "Note : Can't revert back after process!"
        VIEW-AS ALERT-BOX QUESTION BUTTONS YES-NO UPDATE questAns.

    IF questAns = NO THEN DO:
        RETURN.
    END.
    /* End of Re-Ask for Restore CoA Budget */

    /* Checking if CoA Budget is available */
    FIND FIRST gl-accthis WHERE gl-accthis.YEAR = (INT(YEAR(lacy)) + 1001)
        AND (gl-accthis.budget[1] <> 0
            OR gl-accthis.budget[2] <> 0
            OR gl-accthis.budget[3] <> 0
            OR gl-accthis.budget[4] <> 0
            OR gl-accthis.budget[5] <> 0
            OR gl-accthis.budget[6] <> 0
            OR gl-accthis.budget[7] <> 0
            OR gl-accthis.budget[8] <> 0
            OR gl-accthis.budget[9] <> 0
            OR gl-accthis.budget[10] <> 0
            OR gl-accthis.budget[11] <> 0
            OR gl-accthis.budget[12] <> 0)
        NO-LOCK NO-ERROR.

    IF NOT AVAILABLE gl-accthis THEN DO: /* If not available then exit */
        MESSAGE "Sorry, no data found for CoA Budget "
            + STRING(YEAR(lacy) + 1) + ". No data processed!"
            VIEW-AS ALERT-BOX INFORMATION.
        RETURN.
    END.

    IF AVAILABLE gl-accthis THEN DO: /* if available then clear budget on gl-acct */
        FIND FIRST gl-acct NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE gl-acct.
            FIND FIRST gl-acctBUFF WHERE RECID(gl-acctBUFF) = RECID(gl-acct)
                EXCLUSIVE-LOCK.

            DO i = 1 TO 12:
                ASSIGN gl-acctBUFF.budget[i] = 0.
            END.

            RELEASE gl-acctBUFF.
            FIND NEXT gl-acct NO-LOCK NO-ERROR.
        END.
    END.
    /* End of Checking if CoA Budget is available */

    /* Copy Budget from gl-accthis to gl-acct */
    FIND FIRST gl-accthis WHERE gl-accthis.YEAR = (INT(YEAR(lacy)) + 1001)
        AND (gl-accthis.budget[1] <> 0
            OR gl-accthis.budget[2] <> 0
            OR gl-accthis.budget[3] <> 0
            OR gl-accthis.budget[4] <> 0
            OR gl-accthis.budget[5] <> 0
            OR gl-accthis.budget[6] <> 0
            OR gl-accthis.budget[7] <> 0
            OR gl-accthis.budget[8] <> 0
            OR gl-accthis.budget[9] <> 0
            OR gl-accthis.budget[10] <> 0
            OR gl-accthis.budget[11] <> 0
            OR gl-accthis.budget[12] <> 0)
        NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE gl-accthis.
        FIND FIRST gl-acct WHERE gl-acct.fibukonto = gl-accthis.fibukonto NO-ERROR.
        IF NOT AVAILABLE gl-acct THEN DO:
            CREATE gl-acct.
            ASSIGN
                gl-acct.fibukonto  = gl-accthis.fibukonto
                gl-acct.budget[1]  = gl-accthis.budget[1]
                gl-acct.budget[2]  = gl-accthis.budget[2]
                gl-acct.budget[3]  = gl-accthis.budget[3]
                gl-acct.budget[4]  = gl-accthis.budget[4]
                gl-acct.budget[5]  = gl-accthis.budget[5]
                gl-acct.budget[6]  = gl-accthis.budget[6]
                gl-acct.budget[7]  = gl-accthis.budget[7]
                gl-acct.budget[8]  = gl-accthis.budget[8]
                gl-acct.budget[9]  = gl-accthis.budget[9]
                gl-acct.budget[10] = gl-accthis.budget[10]
                gl-acct.budget[11] = gl-accthis.budget[11]
                gl-acct.budget[12] = gl-accthis.budget[12].
        END.
        IF AVAILABLE gl-acct THEN DO:
            ASSIGN
                gl-acct.budget[1]  = gl-accthis.budget[1]
                gl-acct.budget[2]  = gl-accthis.budget[2]
                gl-acct.budget[3]  = gl-accthis.budget[3]
                gl-acct.budget[4]  = gl-accthis.budget[4]
                gl-acct.budget[5]  = gl-accthis.budget[5]
                gl-acct.budget[6]  = gl-accthis.budget[6]
                gl-acct.budget[7]  = gl-accthis.budget[7]
                gl-acct.budget[8]  = gl-accthis.budget[8]
                gl-acct.budget[9]  = gl-accthis.budget[9]
                gl-acct.budget[10] = gl-accthis.budget[10]
                gl-acct.budget[11] = gl-accthis.budget[11]
                gl-acct.budget[12] = gl-accthis.budget[12].
        END.
        FIND NEXT gl-accthis WHERE gl-accthis.YEAR = (INT(YEAR(lacy)) + 1001)
            AND (gl-accthis.budget[1] <> 0
                OR gl-accthis.budget[2] <> 0
                OR gl-accthis.budget[3] <> 0
                OR gl-accthis.budget[4] <> 0
                OR gl-accthis.budget[5] <> 0
                OR gl-accthis.budget[6] <> 0
                OR gl-accthis.budget[7] <> 0
                OR gl-accthis.budget[8] <> 0
                OR gl-accthis.budget[9] <> 0
                OR gl-accthis.budget[10] <> 0
                OR gl-accthis.budget[11] <> 0
                OR gl-accthis.budget[12] <> 0)
            NO-LOCK NO-ERROR.
    END.
    MESSAGE "Restore CoA Budget " + STRING(INT(YEAR(lacy)) + 1)
        + " are done!"
        VIEW-AS ALERT-BOX INFORMATION.
    /* End of Copy Budget from gl-accthis to gl-acct */

    RETURN.
END.
/* End of Restore CoA Budget PROCEDURES */
