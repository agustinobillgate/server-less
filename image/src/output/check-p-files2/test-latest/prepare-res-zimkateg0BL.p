DEF TEMP-TABLE t-paramtext LIKE paramtext.

DEF TEMP-TABLE rmcat-list
  FIELD zikatnr  LIKE zimkateg.zikatnr
  FIELD kurzbez  LIKE zimkateg.kurzbez
  FIELD bezeich  LIKE zimkateg.bezeich
  FIELD kurzbez1 AS CHAR    FORMAT "x(6)"  COLUMN-LABEL "RmType " 
  FIELD setup    AS CHAR    FORMAT "x(20)" COLUMN-LABEL "Bed Setup" 
  FIELD nr       AS         INTEGER. 

DEF OUTPUT PARAMETER TABLE FOR rmcat-list.

DEFINE VARIABLE anz-setup    AS INTEGER INITIAL 0. 

RUN get-bedsetup.
RUN create-rmcat-list.

PROCEDURE get-bedsetup: 
  FOR EACH paramtext WHERE paramtext.txtnr GE 9201 
    AND paramtext.txtnr LE 9299 NO-LOCK BY paramtext.txtnr: 
    IF paramtext.notes NE "" THEN 
    DO: 
        anz-setup = anz-setup + 1.
        /*csetup-array[anz-setup] = SUBSTR(t-paramtext.notes,1,1).
        isetup-array[anz-setup] = t-paramtext.txtnr - 9200.*/
    END. 
  END. 
END. 

PROCEDURE create-rmcat-list: 

  IF anz-setup GT 0 THEN 
    RUN res-zimkateg0bl.p(OUTPUT TABLE rmcat-list).
  ELSE 
  DO: 
    FOR EACH zimkateg NO-LOCK: 
      CREATE rmcat-list. 
      rmcat-list.zikatnr  = zimkateg.zikatnr. 
      rmcat-list.kurzbez  = zimkateg.kurzbez. 
      rmcat-list.kurzbez1 = zimkateg.kurzbez. 
      rmcat-list.bezeich  = zimkateg.bezeich. 
    END. 
  END. 
END. 
