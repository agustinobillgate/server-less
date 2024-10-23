
DEFINE TEMP-TABLE t-zimmer LIKE zimmer
    FIELD outlook AS CHAR.

DEFINE INPUT PARAMETER rmtype    AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER bed-setup AS INTEGER NO-UNDO.

DEFINE OUTPUT PARAMETER TABLE FOR t-zimmer.

FOR EACH zimmer WHERE zimmer.zikatnr = rmtype 
    /*AND zimmer.setup = bed-setup*/ NO-LOCK:
     CREATE t-zimmer.
     BUFFER-COPY zimmer TO t-zimmer.

     FIND FIRST paramtext WHERE paramtext.txtnr = 230 AND paramtext.ptexte NE ""
         AND paramtext.sprachcode = zimmer.typ NO-LOCK NO-ERROR.
     IF AVAILABLE paramtext THEN ASSIGN t-zimmer.outlook = paramtext.ptexte.
END.
