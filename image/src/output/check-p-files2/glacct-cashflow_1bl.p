DEF TEMP-TABLE coa-list
    FIELD fibu LIKE gl-acct.fibukonto
.
DEFINE TEMP-TABLE t-list
    FIELD cf                    AS INTEGER INIT 0
    FIELD fibukonto             AS CHARACTER
    FIELD debit                 AS DECIMAL INIT 0
    FIELD credit                AS DECIMAL INIT 0
    FIELD debit-lsyear          AS DECIMAL INIT 0
    FIELD credit-lsyear         AS DECIMAL INIT 0
    FIELD debit-lsmonth         AS DECIMAL INIT 0
    FIELD credit-lsmonth        AS DECIMAL INIT 0
    FIELD balance		        AS DECIMAL INIT 0
    FIELD ly-balance            AS DECIMAL INIT 0
    FIELD pm-balance            AS DECIMAL INIT 0
    /*geral D5D0FB debit - credit MTD & YTD*/
    FIELD debit-today           AS DECIMAL
    FIELD credit-today          AS DECIMAL
    FIELD debit-MTD             AS DECIMAL
    FIELD credit-MTD            AS DECIMAL
    FIELD debit-YTD             AS DECIMAL
    FIELD credit-YTD            AS DECIMAL
    FIELD today-balance         AS DECIMAL
    FIELD MTD-balance           AS DECIMAL
    FIELD YTD-balance           AS DECIMAL
.
DEFINE BUFFER tbuff FOR t-list.

DEF INPUT PARAMETER from-date    AS DATE NO-UNDO.
DEF INPUT PARAMETER to-date      AS DATE NO-UNDO.
DEF INPUT PARAMETER from-lsyr    AS DATE NO-UNDO.
DEF INPUT PARAMETER to-lsyr      AS DATE NO-UNDO.
DEF INPUT PARAMETER Pfrom-date   AS DATE NO-UNDO.
DEF INPUT PARAMETER Pto-date     AS DATE NO-UNDO.
DEF INPUT PARAMETER from-month   AS DATE NO-UNDO.
DEF INPUT PARAMETER from-year    AS DATE NO-UNDO.
DEF INPUT PARAMETER TABLE FOR coa-list.
DEF OUTPUT PARAMETER TABLE FOR t-list.

DEF VARIABLE close-month    AS DATE    NO-UNDO.
DEF VARIABLE close-year     AS DATE    NO-UNDO.
DEF VARIABLE last-close-yr  AS DATE    NO-UNDO.
DEF VARIABLE prev-month     AS INTEGER NO-UNDO.

RUN htpdate.p(597, OUTPUT close-month).
RUN htpdate.p(795, OUTPUT last-close-yr).
ASSIGN close-year = DATE(12, 31, YEAR(last-close-yr) + 1).

ASSIGN prev-month = MONTH(from-date) - 1.
IF prev-month = 0 THEN prev-month = 12.

FOR EACH coa-list:
    CREATE tbuff.
    ASSIGN tbuff.fibukonto = coa-list.fibu.
    RUN calc-balance(1, coa-list.fibu, from-date, to-date).
    RUN calc-balance(2, coa-list.fibu, from-lsyr, to-lsyr).
    RUN calc-balance(3, coa-list.fibu, Pfrom-date, Pto-date).
    /*geral D5D0FB debit - credit MTD & YTD*/
    RUN calc-balance(4, coa-list.fibu, to-date, to-date).
    RUN calc-balance(5, coa-list.fibu, from-month, to-date).
    RUN calc-balance(6, coa-list.fibu, from-year, to-date).
END.

PROCEDURE calc-balance:
DEF INPUT PARAMETER i-case      AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER fibu        AS CHAR     NO-UNDO.
DEF INPUT PARAMETER from-date   AS DATE     NO-UNDO.
DEF INPUT PARAMETER to-date     AS DATE     NO-UNDO.

DEF VARIABLE p-bal  AS DECIMAL INITIAL 0    NO-UNDO.
DEF VARIABLE debit  AS DECIMAL INITIAL 0    NO-UNDO.
DEF VARIABLE credit AS DECIMAL INITIAL 0    NO-UNDO.

DEF VARIABLE date1      AS DATE             NO-UNDO.
DEF VARIABLE date2      AS DATE             NO-UNDO.
DEF VARIABLE p-sign     AS INTEGER INIT 1   NO-UNDO.
DEF VARIABLE i-cf       AS INTEGER INIT ?   NO-UNDO.
DEF BUFFER gbuff FOR gl-acct.
   
    FIND FIRST gbuff WHERE gbuff.fibukonto = fibu NO-LOCK NO-ERROR.
    IF NOT AVAILABLE gbuff THEN RETURN.
    IF from-date GT close-month THEN RETURN.

    FIND CURRENT tbuff.

    IF gbuff.acc-type = 1 OR gbuff.acc-type = 4 THEN p-sign = -1.
    IF gbuff.acc-type = 3 OR gbuff.acc-type = 4 THEN
    DO:
      IF YEAR(close-year) = YEAR(close-month) THEN /* already doing close year */
      DO:
        IF YEAR(from-date) EQ YEAR(close-month) THEN
        DO:
            /*DISP from-date.
            MESSAGE "in3"
                VIEW-AS ALERT-BOX INFO BUTTONS OK.*/
            IF MONTH(from-date) EQ 1 THEN ASSIGN p-bal = gbuff.last-yr[12].
            ELSE ASSIGN p-bal = gbuff.actual[prev-month].
        END.
        ELSE /* it means YEAR(from-date) LT YEAR(close-month) */
        DO:
            FIND FIRST gl-accthis WHERE gl-accthis.fibukonto = fibu
              AND gl-accthis.YEAR = YEAR(from-date) NO-LOCK NO-ERROR.
            IF NOT AVAILABLE gl-accthis THEN RETURN.
            IF MONTH(from-date) EQ 1 THEN ASSIGN p-bal = gl-accthis.last-yr[12].
            ELSE ASSIGN p-bal = gl-accthis.actual[prev-month].
        END.
      END.
      ELSE IF YEAR(close-year) LT YEAR(close-month) THEN /* not yet doing close year */
      DO:
        /*DISP YEAR(from-date) YEAR(close-month).
        MESSAGE "in1"
            VIEW-AS ALERT-BOX INFO BUTTONS OK.*/
        IF YEAR(from-date) EQ YEAR(close-month) THEN /* this year */
        DO:
            IF MONTH(from-date) EQ 1 THEN ASSIGN p-bal = gbuff.last-yr[12].
            ELSE ASSIGN p-bal = gbuff.actual[prev-month].
        END.
        ELSE IF YEAR(from-date) EQ (YEAR(close-month) - 1) THEN /* = last year */
        DO:
            IF MONTH(from-date) GE 2 THEN ASSIGN p-bal = gbuff.last-yr[prev-month].
            ELSE /* it means MONTH(from-date) = 1 */ 
            DO:
                FIND FIRST gl-accthis WHERE gl-accthis.fibukonto = fibu
                  AND gl-accthis.YEAR = YEAR(from-date) - 1 NO-LOCK NO-ERROR.
                IF NOT AVAILABLE gl-accthis THEN RETURN.
                ASSIGN p-bal = gl-accthis.actual[12].
            END.
        END.
        ELSE /* = YEAR(from-date) is older than last year */
        DO:
            FIND FIRST gl-accthis WHERE gl-accthis.fibukonto = fibu
              AND gl-accthis.YEAR = YEAR(from-date) NO-LOCK NO-ERROR.
            IF NOT AVAILABLE gl-accthis THEN RETURN.
            IF MONTH(from-date) EQ 1 THEN ASSIGN p-bal = gl-accthis.last-yr[12].
            ELSE ASSIGN p-bal = gl-accthis.actual[prev-month].
        END.
      END.
    END.

    IF DAY(from-date) GE 2 AND (gbuff.acc-type = 3 OR gbuff.acc-type = 4) THEN
    DO:
        ASSIGN
            date1 = DATE(MONTH(from-date), 1, YEAR(from-date))
            date2 = DATE(MONTH(from-date), DAY(from-date) - 1, YEAR(from-date))
        .
        FOR EACH gl-jouhdr WHERE gl-jouhdr.datum GE date1
            AND gl-jouhdr.datum LE date2 NO-LOCK,
            EACH gl-journal WHERE gl-journal.jnr = gl-jouhdr.jnr
                AND gl-journal.fibukonto = fibu NO-LOCK:
            ASSIGN p-bal = p-bal + gl-journal.debit - gl-journal.credit.
        END.
    END.
    CASE i-case:
        WHEN 1 THEN tbuff.balance       = p-bal.
        WHEN 2 THEN tbuff.ly-balance    = p-bal.
        WHEN 3 THEN tbuff.pm-balance    = p-bal.
        WHEN 3 THEN tbuff.today-balance = p-bal.
        WHEN 5 THEN tbuff.MTD-balance   = p-bal.
        WHEN 6 THEN tbuff.YTD-balance   = p-bal.
    END CASE.

    /*DISP p-bal FORMAT "->>>,>>>,>>9.99".
    MESSAGE "in"
        VIEW-AS ALERT-BOX INFO BUTTONS OK.*/
    
    ASSIGN
        date1 = DATE(MONTH(from-date), DAY(from-date), YEAR(from-date))
        date2 = DATE(MONTH(to-date), DAY(to-date), YEAR(to-date)).


    FOR EACH gl-jouhdr WHERE gl-jouhdr.datum GE date1
        AND gl-jouhdr.datum LE date2 NO-LOCK,
        EACH gl-journal WHERE gl-journal.jnr = gl-jouhdr.jnr
        AND gl-journal.fibukonto = fibu NO-LOCK:
        ASSIGN
            credit = gl-journal.credit
            debit  = gl-journal.debit
            i-cf  = ?
            i-cf  = INTEGER(ENTRY(2,gl-journal.bemerk,CHR(2))) NO-ERROR
        .
        RELEASE t-list.
        IF i-case GT 0 THEN
        DO:
            FIND FIRST t-list WHERE t-list.fibukonto = fibu
                AND t-list.cf = i-cf NO-ERROR.
            IF NOT AVAILABLE t-list THEN
            DO:
                CREATE t-list.
                ASSIGN 
                    t-list.fibukonto = fibu
                    t-list.cf        = i-cf
                .
            END.
            CASE i-case:
                WHEN 1 THEN
                ASSIGN
                    t-list.credit  = t-list.credit + credit
                    t-list.debit   = t-list.debit + debit
                .
                WHEN 2 THEN
                ASSIGN
                    t-list.credit-lsyear  = t-list.credit-lsyear + credit
                    t-list.debit-lsyear   = t-list.credit-lsyear + debit
                .
                WHEN 3 THEN
                ASSIGN
                    t-list.credit-lsmonth = t-list.credit-lsmonth + credit
                    t-list.debit-lsmonth  = t-list.debit-lsmonth + debit
                .
                WHEN 4 THEN
                ASSIGN
                    t-list.credit-today   = t-list.credit-today + credit
                    t-list.debit-today    = t-list.debit-today + debit
                .
                WHEN 5 THEN
                ASSIGN
                    t-list.credit-MTD     = t-list.credit-MTD + credit
                    t-list.debit-MTD      = t-list.debit-MTD + debit
                .
                WHEN 6 THEN
                ASSIGN
                    t-list.credit-YTD     = t-list.credit-YTD + credit
                    t-list.debit-YTD      = t-list.debit-YTD + debit
                .
            END CASE.
        END.
        CASE i-case:
            WHEN 1 THEN
            ASSIGN
                tbuff.credit  = tbuff.credit + credit
                tbuff.debit   = tbuff.debit + debit
                tbuff.balance = tbuff.balance + debit - credit
            .
            WHEN 2 THEN
            ASSIGN
                tbuff.credit-lsyear  = tbuff.credit-lsyear + credit
                tbuff.debit-lsyear   = tbuff.credit-lsyear + debit
                tbuff.ly-balance     = tbuff.ly-balance + debit - credit
            .
            WHEN 3 THEN
            ASSIGN
                tbuff.credit-lsmonth = tbuff.credit-lsmonth + credit
                tbuff.debit-lsmonth  = tbuff.debit-lsmonth + debit
                tbuff.pm-balance     = tbuff.pm-balance + debit - credit
            .
            WHEN 4 THEN
            ASSIGN
                tbuff.credit-today    = tbuff.credit-today + credit
                tbuff.debit-today     = tbuff.debit-today + debit
                tbuff.today-balance   = tbuff.today-balance + debit - credit
            .
            WHEN 5 THEN
            ASSIGN
                tbuff.credit-mtd      = tbuff.credit-mtd + credit
                tbuff.debit-mtd       = tbuff.debit-mtd + debit
                tbuff.mtd-balance     = tbuff.mtd-balance + debit - credit
            .
            WHEN 6 THEN
            ASSIGN
                tbuff.credit-ytd      = tbuff.credit-ytd + credit
                tbuff.debit-ytd       = tbuff.debit-ytd + debit
                tbuff.ytd-balance     = tbuff.ytd-balance + debit - credit
            .
        END CASE.
    END.
    CASE i-case:
        WHEN 1 THEN tbuff.balance        = p-sign * tbuff.balance.
        WHEN 2 THEN tbuff.ly-balance     = p-sign * tbuff.ly-balance.
        WHEN 3 THEN tbuff.pm-balance     = p-sign * tbuff.pm-balance.
        WHEN 4 THEN tbuff.today-balance  = p-sign * tbuff.today-balance.
        WHEN 5 THEN tbuff.mtd-balance    = p-sign * tbuff.mtd-balance.
        WHEN 6 THEN tbuff.ytd-balance    = p-sign * tbuff.ytd-balance.
    END CASE.

END.
