
DEFINE TEMP-TABLE b1-list
    FIELD nr       LIKE prtable.nr
    FIELD marknr   LIKE prtable.marknr
    FIELD bezeich  LIKE prmarket.bezeich
    FIELD char3    LIKE queasy.char3
    FIELD logi3    LIKE queasy.logi3
    FIELD rec-id   AS INT
    FIELD pr-recid AS INT.

DEF TEMP-TABLE t-prtable LIKE prtable.
DEF TEMP-TABLE t-prmarket LIKE prmarket.
DEF TEMP-TABLE t-queasy LIKE queasy.

DEF INPUT PARAMETER TABLE FOR t-prtable.
DEF INPUT PARAMETER TABLE FOR t-prmarket.
DEF INPUT PARAMETER TABLE FOR t-queasy.
DEF OUTPUT PARAMETER TABLE FOR b1-list.

FIND FIRST t-prtable NO-ERROR.
IF AVAILABLE t-prtable THEN
DO:
    CREATE prtable.
    BUFFER-COPY t-prtable TO prtable.
    RELEASE prtable.
END.

FIND FIRST t-prmarket NO-ERROR.
IF AVAILABLE t-prmarket THEN
DO:
    CREATE prmarket.
    BUFFER-COPY t-prmarket TO prmarket.
    RELEASE prmarket.
END.

FIND FIRST t-queasy NO-ERROR.
IF AVAILABLE t-queasy THEN
DO:
    CREATE queasy.
    BUFFER-COPY t-queasy TO queasy.
    RELEASE queasy.
END.


FOR EACH prtable WHERE prtable.prcode = "" NO-LOCK,
    FIRST prmarket WHERE prmarket.nr = prtable.marknr NO-LOCK,
    FIRST queasy WHERE queasy.key = 18 AND queasy.number1 = prmarket.nr 
    NO-LOCK BY prtable.nr:
    CREATE b1-list.
    ASSIGN
      b1-list.nr = prtable.nr
      b1-list.marknr = prtable.marknr
      b1-list.bezeich = prmarket.bezeich
      b1-list.char3 = queasy.char3
      b1-list.logi3 = queasy.logi3
      b1-list.rec-id = RECID(prtable)
      b1-list.pr-recid = RECID(prmarket).
END.
