
DEFINE TEMP-TABLE disc-list LIKE mc-disc
    FIELD depart  AS CHAR
    FIELD rec-id  AS INTEGER
    FIELD counter AS INTEGER.

DEFINE TEMP-TABLE tdept LIKE hoteldpt.

DEFINE INPUT PARAMETER curr-nr        AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER types-bezeich AS CHAR    NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR disc-list.
DEFINE OUTPUT PARAMETER TABLE FOR tdept.

DEF VAR counter AS INTEGER.

DEFINE BUFFER hbuff FOR hoteldpt.


FIND FIRST mc-types WHERE mc-types.nr = curr-nr NO-LOCK.
IF AVAILABLE mc-types THEN
    ASSIGN types-bezeich = mc-types.bezeich.

FOR EACH mc-disc WHERE mc-disc.nr = curr-nr NO-LOCK,
  FIRST hbuff WHERE hbuff.num = mc-disc.departement NO-LOCK 
  BY mc-disc.artnrfront:
    counter = counter + 1.
    CREATE disc-list.
    BUFFER-COPY mc-disc TO disc-list.
    ASSIGN disc-list.depart  = hbuff.depart
           disc-list.rec-id  = RECID(mc-disc)
           disc-list.counter = counter.
END.

FOR EACH hoteldpt NO-LOCK:
    CREATE tdept.
    BUFFER-COPY hoteldpt TO tdept.
END.
