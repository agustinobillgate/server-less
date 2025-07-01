DEF TEMP-TABLE rmcat-list
  FIELD zikatnr  LIKE zimkateg.zikatnr
  FIELD kurzbez  LIKE zimkateg.kurzbez
  FIELD bezeich  LIKE zimkateg.bezeich
  FIELD kurzbez1 AS CHAR    FORMAT "x(6)"  COLUMN-LABEL "RmCat  " 
  FIELD setup    AS CHAR    FORMAT "x(20)" COLUMN-LABEL "Bed Setup" 
  FIELD nr       AS         INTEGER. 

DEFINE OUTPUT PARAMETER TABLE FOR rmcat-list.

DEF VAR i               AS INTEGER              NO-UNDO.
DEF VAR anz-setup       AS INTEGER INIT 0       NO-UNDO.
DEF VAR isetup-array    AS INTEGER EXTENT 99    NO-UNDO. 

FOR EACH paramtext WHERE paramtext.txtnr GE 9201 
  AND paramtext.txtnr LE 9299 NO-LOCK BY paramtext.txtnr: 
  IF paramtext.notes NE "" THEN 
  ASSIGN 
    anz-setup               = anz-setup + 1 
    isetup-array[anz-setup] = paramtext.txtnr - 9200
  . 
END.

FOR EACH zimkateg NO-LOCK: 
  FIND FIRST zimmer WHERE zimmer.zikatnr = zimkateg.zikatnr 
    AND zimmer.setup = 0 NO-LOCK NO-ERROR. 
  IF AVAILABLE zimmer THEN 
  DO: 
    CREATE rmcat-list.
    BUFFER-COPY zimkateg TO rmcat-list.
  END.
  DO i = 1 TO anz-setup: 
      FIND FIRST paramtext WHERE paramtext.txtnr 
          = (isetup-array[i] + 9200) NO-LOCK. 
      FIND FIRST zimmer WHERE zimmer.zikatnr = zimkateg.zikatnr 
          AND zimmer.setup = isetup-array[i] NO-LOCK NO-ERROR. 
      IF AVAILABLE zimmer THEN 
      DO: 
        CREATE rmcat-list. 
        rmcat-list.zikatnr  = zimkateg.zikatnr. 
        rmcat-list.kurzbez  = zimkateg.kurzbez. 
        rmcat-list.kurzbez1 = zimkateg.bezeich. 
        rmcat-list.bezeich  = zimkateg.bezeich. 
        /*MTBUFFER-COPY zimkateg TO rmcat-list.*/
        ASSIGN
          rmcat-list.kurzbez1 = zimkateg.kurzbez 
            + SUBSTR(paramtext.notes,1,1) 
          rmcat-list.setup    = paramtext.ptexte 
          rmcat-list.nr       = i
        .
      END. 
  END. 
END. 

