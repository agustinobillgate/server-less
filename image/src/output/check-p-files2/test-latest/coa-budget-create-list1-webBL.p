DEFINE TEMP-TABLE coa-list
  FIELD fibukonto  AS CHARACTER
  FIELD main-nr    AS INTEGER
  FIELD bezeich    AS CHARACTER
  FIELD b-flag     AS LOGICAL
  FIELD acct-type  AS INTEGER
  FIELD actual     AS DECIMAL EXTENT 12
  FIELD bemerk     AS CHARACTER
  FIELD fs-type    AS INTEGER
  FIELD last-yr    AS DECIMAL EXTENT 12
  FIELD budget     AS DECIMAL EXTENT 12
  FIELD deptnr     AS INTEGER
  FIELD userinit   AS CHARACTER
  FIELD chginit    AS CHARACTER
  FIELD c-date     AS DATE
  FIELD m-date     AS DATE
  FIELD modifiable AS LOGICAL
  FIELD activeflag AS LOGICAL
  FIELD ly-budget  AS DECIMAL EXTENT 12
  FIELD debit      AS DECIMAL EXTENT 12
  FIELD credit     AS DECIMAL EXTENT 12
  FIELD is-group   AS LOGICAL.

DEFINE TEMP-TABLE t-gl-fstype LIKE gl-fstype.

DEFINE INPUT PARAMETER disp-all       AS LOGICAL NO-UNDO. /* MG Untuk show COA Fix Asset Penambahan budget coa FA F9131B */
DEFINE INPUT PARAMETER case-type      AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER fstype-nr      AS INTEGER NO-UNDO. 
DEFINE OUTPUT PARAMETER max-row       AS INTEGER NO-UNDO INITIAL 2.
DEFINE OUTPUT PARAMETER month-closing AS INTEGER. /* FD June 20, 2022 => Ticket DCB0AD */
DEFINE OUTPUT PARAMETER year-closing  AS INTEGER. /* FD June 20, 2022 => Ticket DCB0AD */
DEFINE OUTPUT PARAMETER curr-year     AS INTEGER. /* FD June 20, 2022 => Ticket DCB0AD */
DEFINE OUTPUT PARAMETER TABLE         FOR coa-list.
DEFINE OUTPUT PARAMETER TABLE         FOR t-gl-fstype.

DEFINE VARIABLE fs-number-group       AS INTEGER INITIAL -99 NO-UNDO.
DEFINE VARIABLE is-first              AS LOGICAL INITIAL YES.

/* keep for upcoming enhancement */
FIND FIRST htparam WHERE paramnr = 558 NO-LOCK. 
month-closing = MONTH(htparam.fdate).
year-closing = YEAR(htparam.fdate).

FIND FIRST htparam WHERE paramnr = 87 NO-LOCK. 
curr-year = YEAR(htparam.fdate).
/* keep for upcoming enhancement */

FOR EACH coa-list:
  DELETE coa-list.
END.

FOR EACH t-gl-fstype:
  DELETE t-gl-fstype.
END.

/* enhance logic to enable sort gl-acct by financial statement by Oscar (23 September 2024) - 49A1C3 */


CASE case-type:
  WHEN 1 THEN
  DO:
    CREATE t-gl-fstype.
    ASSIGN 
      t-gl-fstype.nr = 0
      t-gl-fstype.kurzbez = "ALL"
      t-gl-fstype.bezeich = "Select All".

    FOR EACH gl-fstype NO-LOCK BY gl-fstype.nr:
      RUN assign-it.
    END.
    
  END.
  WHEN 2 THEN
  DO:
    IF fstype-nr EQ 0 THEN
    DO:
      IF disp-all THEN RUN create-list1a.
      ELSE RUN create-list1b.
    END.

    ELSE
    DO:
      IF disp-all THEN RUN create-list2a.
      ELSE RUN create-list2b.
    END.

    /*
    FOR EACH gl-acct NO-LOCK:
      ACCUMULATE gl-acct.fibukonto (COUNT).
    END.

    max-row = ACCUM COUNT gl-acct.fibukonto.
    */
    FOR EACH gl-acct NO-LOCK:
      max-row = max-row + 1.
    END.
  END.
END CASE.

PROCEDURE create-list1a:  
  FOR EACH gl-acct NO-LOCK,
  FIRST gl-fstype WHERE gl-fstype.nr EQ gl-acct.fs-type
  NO-LOCK BY gl-fstype.nr BY gl-acct.fibukonto:
    RUN create-coa-list.
  END.
END.

PROCEDURE create-list1b:
  FOR EACH gl-acct WHERE gl-acct.acc-type NE 3 
  AND gl-acct.acc-type NE 4 NO-LOCK,
  FIRST gl-fstype WHERE gl-fstype.nr EQ gl-acct.fs-type 
  NO-LOCK BY gl-fstype.nr BY gl-acct.fibukonto:
    RUN create-coa-list.
  END.
END.

PROCEDURE create-list2a:  
  FOR EACH gl-acct WHERE gl-acct.fs-type EQ fstype-nr NO-LOCK,
  FIRST gl-fstype WHERE gl-fstype.nr EQ gl-acct.fs-type 
  NO-LOCK BY gl-fstype.nr BY gl-acct.fibukonto:
    RUN create-coa-list.
  END.
END.

PROCEDURE create-list2b:
  FOR EACH gl-acct WHERE gl-acct.acc-type NE 3 
  AND gl-acct.acc-type NE 4 
  AND gl-acct.fs-type EQ fstype-nr NO-LOCK,
  FIRST gl-fstype WHERE gl-fstype.nr EQ gl-acct.fs-type 
  NO-LOCK BY gl-fstype.nr BY gl-acct.fibukonto:
    RUN create-coa-list.
  END.
END.

PROCEDURE assign-it:
  CREATE t-gl-fstype.
  BUFFER-COPY gl-fstype TO t-gl-fstype.
END.

PROCEDURE create-coa-list:
  IF fs-number-group NE gl-fstype.nr THEN
  DO:
    fs-number-group = gl-fstype.nr.

    IF is-first EQ NO THEN
    DO:
      CREATE coa-list.
      ASSIGN
        coa-list.fibukonto = ""
        coa-list.is-group  = YES.
    END.
    ELSE is-first = NO.

    CREATE coa-list.
    ASSIGN
      coa-list.fibukonto = ""
      coa-list.main-nr   = 0
      coa-list.bezeich   = STRING(gl-fstype.nr) + " - " + STRING(gl-fstype.bezeich)
      coa-list.is-group  = YES.
  END.

  CREATE coa-list.
  BUFFER-COPY gl-acct TO coa-list.
  coa-list.is-group = NO.
END.
