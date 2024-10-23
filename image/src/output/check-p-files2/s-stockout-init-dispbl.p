DEF TEMP-TABLE t-l-ophdr     LIKE l-ophdr
    FIELD rec-id AS INT.

DEF OUTPUT PARAMETER TABLE FOR t-l-ophdr.

DO TRANSACTION: 
   CREATE l-ophdr.
   FIND CURRENT l-ophdr NO-LOCK.
   CREATE t-l-ophdr.
   BUFFER-COPY l-ophdr TO t-l-ophdr.
   ASSIGN t-l-ophdr.rec-id = RECID(l-ophdr).
END.
