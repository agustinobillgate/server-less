DEFINE TEMP-TABLE rmcat
    FIELD nr          AS INTEGER
    FIELD CODE        AS CHAR.

DEFINE TEMP-TABLE bed-setup
    FIELD nr            AS INTEGER
    FIELD bezeich       AS CHAR
    FIELD bed-code      AS CHAR.

DEFINE TEMP-TABLE rmtype LIKE zimkateg.
DEFINE TEMP-TABLE t-queasy LIKE queasy.
DEFINE TEMP-TABLE t-paramtext LIKE paramtext.
DEFINE TEMP-TABLE guest-pref LIKE queasy.
    

DEFINE OUTPUT PARAMETER TABLE FOR rmcat.
DEFINE OUTPUT PARAMETER TABLE FOR bed-setup.
DEFINE OUTPUT PARAMETER TABLE FOR rmtype.
DEFINE OUTPUT PARAMETER TABLE FOR t-queasy.
DEFINE OUTPUT PARAMETER TABLE FOR t-paramtext.
DEFINE OUTPUT PARAMETER TABLE FOR guest-pref.


FOR EACH queasy WHERE queasy.KEY = 152 NO-LOCK:
    CREATE rmcat.
    ASSIGN rmcat.nr = queasy.number1
           rmcat.CODE = queasy.char1.
END.

FOR EACH paramtext WHERE paramtext.txtnr GE 9201
    AND paramtext.txtnr LE 9299 NO-LOCK:
    CREATE bed-setup.
    ASSIGN 
        bed-setup.nr       = paramtext.txtnr - 9200
        bed-setup.bezeich  = paramtext.ptexte
        bed-setup.bed-code = paramtext.notes.
END.

FOR EACH zimkateg NO-LOCK:
    CREATE rmtype.
    BUFFER-COPY zimkateg TO rmtype.
END.

FOR EACH queasy WHERE queasy.KEY = 152 NO-LOCK:
    CREATE t-queasy.
    BUFFER-COPY queasy TO t-queasy.
END.

FOR EACH queasy WHERE queasy.KEY = 189
    AND queasy.logi2 = YES NO-LOCK:
    CREATE guest-pref.
    BUFFER-COPY queasy TO guest-pref.
END.

FOR EACH paramtext WHERE paramtext.txtnr = 230 
  AND paramtext.ptexte NE "" NO-LOCK: 
  CREATE t-paramtext.
  BUFFER-COPY paramtext TO t-paramtext.
END.
