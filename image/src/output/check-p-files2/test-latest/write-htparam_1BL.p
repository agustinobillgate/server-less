
DEF TEMP-TABLE t-htparam   LIKE htparam.

DEF INPUT PARAMETER case-type   AS INTEGER.
DEF INPUT PARAMETER TABLE FOR t-htparam.
DEF OUTPUT PARAMETER success-flag AS LOGICAL INITIAL NO.

DEF BUFFER htbuff FOR htparam.

FIND FIRST t-htparam NO-ERROR.
IF NOT AVAILABLE t-htparam THEN
    RETURN NO-APPLY.

CASE case-type :
    WHEN 1 THEN
    DO: 
        FIND FIRST htparam WHERE
            htparam.paramnr EQ t-htparam.paramnr
            NO-LOCK NO-ERROR.
        IF AVAILABLE htparam THEN
        DO TRANSACTION:
            FIND FIRST htbuff WHERE RECID(htbuff) = RECID(htparam)
                EXCLUSIVE-LOCK.
            BUFFER-COPY t-htparam TO htbuff.
            FIND CURRENT htbuff NO-LOCK.
            RELEASE htbuff.
            success-flag = YES.
        END.
    END.
    WHEN 2 THEN
    DO: 
        FIND FIRST htparam WHERE
            htparam.paramnr EQ t-htparam.paramnr
            NO-LOCK NO-ERROR.
        IF AVAILABLE htparam THEN
        DO TRANSACTION:

            FIND FIRST htbuff WHERE RECID(htbuff) = RECID(htparam)
                EXCLUSIVE-LOCK.
            ASSIGN htbuff.fdate = t-htparam.fdate.
            FIND CURRENT htbuff NO-LOCK.
            RELEASE htbuff.
            success-flag = YES.
        END.
    END.
    /* SY 25 JUL 2017 */
    WHEN 3 THEN
    DO:
    DEF VARIABLE prev-natcode AS INTEGER NO-UNDO INIT 0.
    DEF VARIABLE new-natcode  AS INTEGER NO-UNDO.
    DEF BUFFER natbuff FOR nation.
        FIND FIRST htparam WHERE htparam.paramnr EQ t-htparam.paramnr
            NO-LOCK NO-ERROR.
        IF AVAILABLE htparam THEN
        DO:
            IF t-htparam.paramnr = 153 AND t-htparam.fchar NE ? THEN
            DO: /* update nation.natcode of local region */ 
              IF htparam.fchar NE t-htparam.fchar THEN
              DO:
                FIND FIRST nation WHERE nation.kurzbez = htparam.fchar
                    NO-LOCK NO-ERROR.
                IF AVAILABLE nation THEN 
                    ASSIGN prev-natcode = nation.nationnr.
                FIND FIRST nation WHERE nation.kurzbez = t-htparam.fchar
                    NO-LOCK.
                ASSIGN new-natcode = nation.nationnr.
                IF prev-natcode NE 0 THEN
                DO:
                  FIND FIRST nation WHERE nation.natcode = prev-natcode
                    NO-LOCK NO-ERROR.
                  DO WHILE AVAILABLE nation:
                    DO TRANSACTION:
                        FIND FIRST natbuff WHERE RECID(natbuff)
                            = RECID(nation) EXCLUSIVE-LOCK.
                        ASSIGN natbuff.natcode = new-natcode.
                        FIND CURRENT natbuff.
                        RELEASE natbuff.
                    END.
                    FIND NEXT nation WHERE nation.natcode = prev-natcode
                        NO-LOCK NO-ERROR.
                  END.
                END.
              END.
            END.
            DO TRANSACTION:
              FIND FIRST htbuff WHERE RECID(htbuff) = RECID(htparam)
                  EXCLUSIVE-LOCK.
            IF t-htparam.finteger NE ? THEN
            ASSIGN htbuff.finteger = t-htparam.finteger.
            IF t-htparam.fdecimal NE ? THEN
            ASSIGN htbuff.fdecimal = t-htparam.fdecimal.
            IF t-htparam.fdate NE ? THEN
            ASSIGN htbuff.fdate = t-htparam.fdate.
            IF t-htparam.flogical NE ? THEN
            ASSIGN htbuff.flogical = t-htparam.flogical.
            IF t-htparam.fchar NE ? THEN
            ASSIGN htbuff.fchar = t-htparam.fchar.
            FIND CURRENT htbuff NO-LOCK.
            RELEASE htbuff.
            success-flag = YES.
            END.
        END.
    END.
    /* SY 05 AUG 2017 */
    WHEN 4 THEN
    DO:
        FOR EACH t-htparam:
            FIND FIRST htparam WHERE htparam.paramnr = 
                t-htparam.paramnr EXCLUSIVE-LOCK.
            BUFFER-COPY t-htparam TO htparam.
            FIND CURRENT htparam NO-LOCK.
        END.
        success-flag = YES.
    END.
    /* Add by Michael @ 04/09/2019 for VHP Web customization */
    WHEN 5 THEN
    DO:
        FIND FIRST htparam WHERE htparam.paramnr EQ t-htparam.paramnr NO-LOCK NO-ERROR.
        DO TRANSACTION:
            BUFFER-COPY t-htparam TO htparam.
            FIND CURRENT htparam NO-LOCK.
            RELEASE htparam.
            ASSIGN success-flag = YES.
        END.
    END.
    /* End of add */

END CASE.


