DEFINE TEMP-TABLE t-memozinr
    FIELD gastnr        LIKE res-line.gastnr
    FIELD memozinr      LIKE res-line.memozinr
    FIELD memodatum     LIKE res-line.memodatum
    FIELD NAME          LIKE res-line.name
    FIELD ankunft       LIKE res-line.ankunft 
    FIELD abreise       LIKE res-line.abreise
    FIELD anztage       LIKE res-line.anztage
    FIELD arrangement   LIKE res-line.arrangement
    FIELD zipreis       LIKE res-line.zipreis
    FIELD erwachs       LIKE res-line.erwachs
    FIELD kind1         LIKE res-line.kind1
    FIELD resstatus     LIKE res-line.resstatus
    FIELD resnr         LIKE res-line.resnr
    FIELD gastnrmember  LIKE res-line.gastnrmember
    FIELD zinr          LIKE res-line.zinr
    FIELD active-flag   LIKE res-line.active-flag
    FIELD reslinnr      LIKE res-line.reslinnr
    .

DEFINE INPUT PARAMETER memo-zinr AS CHAR.
DEFINE OUTPUT PARAMETER TABLE FOR t-memozinr.

IF memo-zinr = "" THEN
DO:
   FOR EACH res-line WHERE res-line.active-flag LE 1 
       AND res-line.memozinr MATCHES("*;*") 
       AND TRIM(ENTRY(2, res-line.memozinr,";")) NE "" 
       NO-LOCK BY res-line.memozinr BY res-line.memodatum BY res-line.resnr :
       RUN create-t-memozinr.
   END.
END.
ELSE 
DO:
   FOR EACH res-line WHERE res-line.active-flag LE 1 
        AND res-line.memozinr GE (";" + memo-zinr) NO-LOCK 
        BY res-line.memozinr BY res-line.memodatum BY res-line.resnr 
        BY res-line.ankunft :
        RUN create-t-memozinr.
   END.
END.

PROCEDURE create-t-memozinr :
    CREATE t-memozinr.
    ASSIGN 
      t-memozinr.gastnr       = res-line.gastnr
      t-memozinr.memozinr     = res-line.memozinr
      t-memozinr.memodatum    = res-line.memodatum
      t-memozinr.name         = res-line.name                       /* CR 09/05/24 | Fixing for Serverless */
      t-memozinr.ankunft      = res-line.ankunft
      t-memozinr.abreise      = res-line.abreise
      t-memozinr.anztage      = res-line.anztage
      t-memozinr.arrangement  = res-line.arrangement
      t-memozinr.zipreis      = res-line.zipreis
      t-memozinr.erwachs      = res-line.erwachs 
      t-memozinr.kind1        = res-line.kind1 
      t-memozinr.resstatus    = res-line.resstatus
      t-memozinr.resnr        = res-line.resnr
      t-memozinr.gastnrmember = res-line.gastnrmember
      t-memozinr.zinr         = res-line.zinr
      t-memozinr.active-flag  = res-line.active-flag
      t-memozinr.reslinnr     = res-line.reslinnr
    .

END.
