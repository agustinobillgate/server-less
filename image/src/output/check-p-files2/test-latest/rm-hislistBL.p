DEFINE TEMP-TABLE t-hislist 
    FIELD gastinfo      AS CHAR         FORMAT "x(56)"
    FIELD ankunft       AS DATE         FORMAT 99/99/99
    FIELD abreise       AS DATE         FORMAT 99/99/99
    FIELD abreisezeit   AS CHAR         FORMAT "x(5)"
    FIELD zikateg       AS CHAR         FORMAT "x(6)"   
    FIELD zinr          AS CHAR         FORMAT "x(5)"
    FIELD zipreis       AS DECIMAL      FORMAT ">>>,>>>,>>9.99"
    FIELD zimmeranz     AS INTEGER      FORMAT ">>9"
    FIELD arrangement   AS CHAR         FORMAT "x(3)"     
    FIELD resnr         AS INTEGER      FORMAT "->,>>>,>>9" 
    FIELD gesamtumsatz  AS DECIMAL      FORMAT "->,>>>,>>9.99"
    FIELD zahlungsart   AS INTEGER      FORMAT ">>>9"
    FIELD segmentcode   AS INTEGER      FORMAT ">>9"
    FIELD bemerk        AS CHAR         FORMAT "x(64)"
    FIELD betriebsnr    AS INTEGER      FORMAT ">>>>9".

DEFINE INPUT PARAMETER t-date AS DATE NO-UNDO.
DEFINE INPUT PARAMETER f-date AS DATE NO-UNDO.
DEFINE INPUT PARAMETER zinr   AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR t-hislist.

FOR EACH history WHERE history.betriebsnr LE 1 AND 
      NOT ( history.ankunft GT t-date ) AND 
      NOT ( history.abreise LE f-date ) 
      AND history.zinr = zinr AND history.gastnr GT 0 NO-LOCK, 
      FIRST guest WHERE guest.gastnr = history.gastnr
      BY history.gastinfo:
      CREATE t-hislist.
      ASSIGN 
        t-hislist.gastinfo      = history.gastinfo
        t-hislist.ankunft       = history.ankunft
        t-hislist.abreise       = history.abreise 
        t-hislist.abreisezeit   = history.abreisezeit
        t-hislist.zikateg       = history.zikateg 
        t-hislist.zinr          = history.zinr
        t-hislist.zipreis       = history.zipreis 
        t-hislist.zimmeranz     = history.zimmeranz 
        t-hislist.arrangement   = history.arrangement
        t-hislist.resnr         = history.resnr
        t-hislist.gesamtumsatz  = history.gesamtumsatz 
        t-hislist.zahlungsart   = history.zahlungsart 
        t-hislist.segmentcode   = history.segmentcode  
        t-hislist.bemerk        = history.bemerk 
        .

END.
