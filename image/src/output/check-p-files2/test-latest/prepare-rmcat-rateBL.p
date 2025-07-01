DEFINE TEMP-TABLE t-arrangement 
    FIELD arrangement LIKE arrangement.arrangement
    FIELD argtnr      LIKE arrangement.argtnr.
DEFINE TEMP-TABLE t-zimkateg  LIKE zimkateg.

DEFINE TEMP-TABLE q1-list
    FIELD betriebsnr    LIKE katpreis.betriebsnr
    FIELD kurzbez       LIKE zimkateg.kurzbez
    FIELD arrangement   LIKE arrangement.arrangement
    FIELD startperiode  LIKE katpreis.startperiode
    FIELD endperiode    LIKE katpreis.endperiode
    FIELD perspreis1    LIKE katpreis.perspreis[1]
    FIELD perspreis2    LIKE katpreis.perspreis[2]
    FIELD perspreis3    LIKE katpreis.perspreis[3]
    FIELD perspreis4    LIKE katpreis.perspreis[4]
    FIELD kindpreis1    LIKE katpreis.kindpreis[1]
    FIELD kindpreis2    LIKE katpreis.kindpreis[2]

    FIELD zikatnr       LIKE katpreis.zikatnr
    FIELD argtnr        LIKE katpreis.argtnr
    FIELD katpreis-recid AS INT.

DEF OUTPUT PARAMETER TABLE FOR q1-list.
DEF OUTPUT PARAMETER TABLE FOR t-zimkateg.
DEF OUTPUT PARAMETER TABLE FOR t-arrangement.


FOR EACH katpreis WHERE katpreis.betriebsnr GE 0 NO-LOCK, 
    FIRST zimkateg WHERE zimkateg.zikatnr = katpreis.zikatnr NO-LOCK, 
    FIRST arrangement WHERE arrangement.argtnr = katpreis.argtnr NO-LOCK 
    BY katpreis.zikatnr BY katpreis.argtnr  BY katpreis.startperiode:
    CREATE q1-list.
    ASSIGN
    q1-list.zikatnr       = zimkateg.zikatnr
    q1-list.betriebsnr    = katpreis.betriebsnr
    q1-list.kurzbez       = zimkateg.kurzbez
    q1-list.arrangement   = arrangement.arrangement
    q1-list.startperiode  = katpreis.startperiode
    q1-list.endperiode    = katpreis.endperiode
    q1-list.perspreis1    = katpreis.perspreis[1]
    q1-list.perspreis2    = katpreis.perspreis[2]
    q1-list.perspreis3    = katpreis.perspreis[3]
    q1-list.perspreis4    = katpreis.perspreis[4]
    q1-list.kindpreis1    = katpreis.kindpreis[1]
    q1-list.kindpreis2    = katpreis.kindpreis[2]
    q1-list.katpreis-recid = RECID(katpreis).
END.

FOR EACH zimkateg:
    CREATE t-zimkateg.
    BUFFER-COPY zimkateg TO t-zimkateg.
END.

FOR EACH arrangement:
    CREATE t-arrangement.
    ASSIGN t-arrangement.arrangement = arrangement.arrangement
           t-arrangement.argtnr      = arrangement.argtnr.
END.
