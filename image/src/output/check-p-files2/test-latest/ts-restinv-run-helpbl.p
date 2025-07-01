DEF TEMP-TABLE t-h-bill LIKE h-bill
    FIELD rec-id AS INT.

DEF TEMP-TABLE t-h-artikel1 LIKE h-artikel
    FIELD rec-id AS INT.

DEF INPUT-OUTPUT PARAMETER kpr-time AS INT.
DEF INPUT-OUTPUT PARAMETER kpr-recid AS INT.
DEF INPUT PARAMETER bill-date AS DATE.
DEF INPUT PARAMETER tischnr AS INT.
DEF INPUT PARAMETER curr-dept AS INT.
DEF INPUT PARAMETER amount LIKE bill-line.betrag.

DEF OUTPUT PARAMETER fl-code AS INT INIT 0.
DEF OUTPUT PARAMETER TABLE FOR t-h-artikel1.
DEF OUTPUT PARAMETER TABLE FOR t-h-bill.

IF (kpr-time - TIME) GE 300 THEN kpr-time = TIME.
IF kpr-recid = 0 THEN
DO:
    FIND FIRST vhp.queasy WHERE vhp.queasy.key = 3 
      AND vhp.queasy.number1 NE 0 
      AND (vhp.queasy.char1 NE "" OR vhp.queasy.char3 NE "") 
      AND (queasy.date1 EQ bill-date) NO-LOCK NO-ERROR.
    IF AVAILABLE vhp.queasy THEN 
    ASSIGN kpr-recid = INTEGER(RECID(vhp.queasy)).
    kpr-time = TIME.
END.
ELSE IF kpr-recid NE 0 AND (TIME GT (kpr-time + 30)) THEN
DO:
    FIND FIRST vhp.queasy WHERE RECID(vhp.queasy) = kpr-recid
        NO-LOCK NO-ERROR.
    IF AVAILABLE vhp.queasy AND vhp.queasy.number1 NE 0 THEN
    DO:
        fl-code = 1.
    END.
    ASSIGN
      kpr-recid = 0
      kpr-time  = TIME
    .
END.

FIND FIRST vhp.h-bill WHERE vhp.h-bill.tischnr = tischnr
    AND vhp.h-bill.departement = curr-dept
    AND vhp.h-bill.flag = 0 NO-LOCK NO-ERROR.
IF AVAILABLE h-bill THEN
DO:
    CREATE t-h-bill.
    BUFFER-COPY h-bill TO t-h-bill.
    ASSIGN t-h-bill.rec-id = RECID(h-bill).
END.

FOR EACH h-artikel WHERE h-artikel.departement = curr-dept
    AND h-artikel.activeflag NO-LOCK:
    CREATE t-h-artikel1.
    BUFFER-COPY h-artikel TO t-h-artikel1.
    ASSIGN t-h-artikel1.rec-id = RECID(h-artikel).
END.
