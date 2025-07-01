
DEF TEMP-TABLE t-l-bestand      LIKE l-bestand.
DEF TEMP-TABLE t-l-op           LIKE l-op.
DEF TEMP-TABLE t-l-ophdr        LIKE l-ophdr.
DEF TEMP-TABLE t-l-pprice       LIKE l-pprice.
DEF TEMP-TABLE t-l-kredit       LIKE l-kredit.

DEF TEMP-TABLE t-ap-journal     LIKE ap-journal.
DEF TEMP-TABLE t-l-artikel      LIKE l-artikel.
DEF TEMP-TABLE t-l-besthis      LIKE l-besthis.
DEF TEMP-TABLE t-l-hauptgrp     LIKE l-hauptgrp.
DEF TEMP-TABLE t-l-lager        LIKE l-lager.
DEF TEMP-TABLE t-l-lieferant    LIKE l-lieferant.
DEF TEMP-TABLE t-l-liefumsatz   LIKE l-liefumsatz.
DEF TEMP-TABLE t-l-ophhis       LIKE l-ophhis.
DEF TEMP-TABLE t-l-ophis        LIKE l-ophis.
DEF TEMP-TABLE t-l-order        LIKE l-order.
DEF TEMP-TABLE t-l-orderhdr     LIKE l-orderhdr.
DEF TEMP-TABLE t-l-quote        LIKE l-quote.
DEF TEMP-TABLE t-l-segment      LIKE l-segment.
DEF TEMP-TABLE t-l-umsatz       LIKE l-umsatz.
DEF TEMP-TABLE t-l-untergrup    LIKE l-untergrup.
DEF TEMP-TABLE t-l-verbrauch    LIKE l-verbrauch.
DEF TEMP-TABLE t-l-zahlbed      LIKE l-zahlbed.
DEF TEMP-TABLE t-h-rezept       LIKE h-rezept.
DEF TEMP-TABLE t-h-rezlin       LIKE h-rezlin.


DEFINE TEMP-TABLE tlist NO-UNDO
    FIELD table-name AS CHAR
    FIELD objfile    AS BLOB.


DEF INPUT PARAMETER inv-type AS INT.
DEF INPUT PARAMETER port     AS CHAR.

DEF OUTPUT PARAMETER f-endkum AS INT.
DEF OUTPUT PARAMETER b-endkum AS INT.
DEF OUTPUT PARAMETER m-endkum AS INT.
DEF OUTPUT PARAMETER m-datum AS DATE.
DEF OUTPUT PARAMETER fb-datum AS DATE.
DEF OUTPUT PARAMETER billdate AS DATE.
DEF OUTPUT PARAMETER closedate AS DATE.
DEF OUTPUT PARAMETER begindate AS DATE.
DEF OUTPUT PARAMETER todate AS DATE.
DEF OUTPUT PARAMETER TABLE FOR tlist.

    /*
DEF OUTPUT PARAMETER TABLE FOR t-l-bestand.
DEF OUTPUT PARAMETER TABLE FOR t-l-op.
DEF OUTPUT PARAMETER TABLE FOR t-l-ophdr.
DEF OUTPUT PARAMETER TABLE FOR t-l-pprice.
DEF OUTPUT PARAMETER TABLE FOR t-l-kredit.
DEF OUTPUT PARAMETER TABLE FOR t-ap-journal.
DEF OUTPUT PARAMETER TABLE FOR t-l-artikel.
DEF OUTPUT PARAMETER TABLE FOR t-l-besthis.
DEF OUTPUT PARAMETER TABLE FOR t-l-hauptgrp.
DEF OUTPUT PARAMETER TABLE FOR t-l-lager.
DEF OUTPUT PARAMETER TABLE FOR t-l-lieferant.
DEF OUTPUT PARAMETER TABLE FOR t-l-liefumsatz.
DEF OUTPUT PARAMETER TABLE FOR t-l-ophhis.      
DEF OUTPUT PARAMETER TABLE FOR t-l-ophis.
DEF OUTPUT PARAMETER TABLE FOR t-l-order.
DEF OUTPUT PARAMETER TABLE FOR t-l-orderhdr.
DEF OUTPUT PARAMETER TABLE FOR t-l-quote.
DEF OUTPUT PARAMETER TABLE FOR t-l-segment.
DEF OUTPUT PARAMETER TABLE FOR t-l-umsatz.
DEF OUTPUT PARAMETER TABLE FOR t-l-untergrup.
DEF OUTPUT PARAMETER TABLE FOR t-l-verbrauch.
DEF OUTPUT PARAMETER TABLE FOR t-l-zahlbed.*/

DEFINE STREAM s1.
DEFINE VARIABLE curr-folder AS CHAR NO-UNDO.
DEFINE VARIABLE lic-nr      AS CHAR NO-UNDO INIT " ".
DEFINE VARIABLE type-inv    AS CHAR NO-UNDO INIT " ".
DEFINE VARIABLE period      AS DATE NO-UNDO.
DEFINE VARIABLE fb-close-date      AS DATE NO-UNDO.
DEFINE VARIABLE mat-close-date     AS DATE NO-UNDO.
DEFINE VARIABLE last-journ-transgl AS DATE NO-UNDO.
DEFINE VARIABLE doit               AS LOGICAL NO-UNDO.

DEFINE BUFFER ophis-fnb FOR l-ophis.
DEFINE BUFFER ophis-mat FOR l-ophis.

FIND FIRST htparam WHERE paramnr = 257 NO-LOCK. 
f-endkum = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 258 NO-LOCK. 
b-endkum = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 268 NO-LOCK. 
m-endkum = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 221 NO-LOCK. 
m-datum  = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 224 NO-LOCK. 
fb-datum = htparam.fdate. 
 
/* CURRENT closing DATE */ 
IF inv-type = 1 THEN FIND FIRST htparam WHERE paramnr = 224 NO-LOCK. 
ELSE FIND FIRST htparam WHERE paramnr = 221 NO-LOCK. 
billdate = htparam.fdate. 
 
/* the closing date must be the last DAY of the MONTH */
IF MONTH(billdate) = 1 THEN closedate = billdate + 28. 
ELSE closedate = billdate + 30.

closedate = DATE(MONTH(closedate), 1, YEAR(closedate)) - 1. 
begindate = DATE(MONTH(closedate), 1, YEAR(closedate)).

/* this is the date of the next inventory closing */
todate = closedate + 32.
todate = DATE(MONTH(todate), 1, YEAR(todate)) - 1. 

/*** inventory is running ***/ 
DO TRANSACTION: 
  FIND FIRST htparam WHERE paramnr = 232 EXCLUSIVE-LOCK. 
  htparam.flogical = YES. 
  FIND CURRENT htparam NO-LOCK. 
END.

FIND FIRST paramtext WHERE txtnr = 243 NO-LOCK NO-ERROR. 
IF AVAILABLE paramtext AND ptexte NE "" THEN 
  RUN decode-string(ptexte, OUTPUT lic-nr). 

IF inv-type = 1 THEN 
    ASSIGN type-inv = "FnB"
           period = fb-datum.
ELSE IF inv-type = 2 THEN 
    ASSIGN type-inv = "MAT"
           period = m-datum.
ELSE IF inv-type = 3 THEN 
    ASSIGN type-inv = "ALL"
           period = fb-datum.

/*Noted : Jika inv-type = 1 dan 2 maka auto backup hanya diawal saja*/
ASSIGN doit = YES.
FIND FIRST htparam WHERE paramnr = 1035 NO-LOCK NO-ERROR.
last-journ-transgl = htparam.fdate.

IF inv-type = 1 THEN DO:
    RUN htpdate.p(221, OUTPUT mat-close-date).
    IF mat-close-date = last-journ-transgl THEN
    DO:
      FIND FIRST ophis-mat WHERE ophis-mat.op-art = 3 
        AND MONTH(ophis-mat.datum) = MONTH(mat-close-date) 
        AND YEAR(ophis-mat.datum) = YEAR(mat-close-date) NO-LOCK NO-ERROR.
      IF AVAILABLE ophis-mat THEN doit = NO.
      ELSE IF NOT AVAILABLE ophis-mat THEN doit = YES.
    END.
    ELSE doit = NO.
END.
ELSE IF inv-type = 2 THEN DO:
    RUN htpdate.p(224, OUTPUT fb-close-date).
    IF fb-close-date = last-journ-transgl THEN
    DO:
      FIND FIRST ophis-fnb WHERE ophis-fnb.op-art = 1 
        AND MONTH(ophis-fnb.datum) = MONTH(fb-close-date) 
        AND YEAR(ophis-fnb.datum) = YEAR(fb-close-date) NO-LOCK NO-ERROR.
      IF AVAILABLE ophis-fnb THEN doit = NO.
      ELSE IF NOT AVAILABLE ophis-fnb THEN doit = YES.
    END.
    ELSE doit = NO.
END.

IF doit THEN DO:
    IF OPSYS = "WIN32" THEN 
        ASSIGN curr-folder = "c:\backupinv\bkpinv-" + port + "-" + lic-nr + "-ALL-" 
                              + STRING(MONTH(period), "99") + STRING(YEAR(period), "9999")   .
    ELSE ASSIGN curr-folder = "/usr1/vhp/backupinv/bkpinv-" + port + "-" + lic-nr + "-ALL-" 
                              + STRING(MONTH(period), "99") + STRING(YEAR(period), "9999")   .

    OS-COMMAND SILENT VALUE("mkdir -p " + curr-folder).

    RUN dump-files. 
    RUN create-file.
END.
/*end*/


PROCEDURE dump-files: 
  
  OS-DELETE VALUE(curr-folder + "/l-bestan.d").
  OS-DELETE VALUE(curr-folder + "/l-op.d").
  OS-DELETE VALUE(curr-folder + "/l-ophdr.d").
  OS-DELETE VALUE(curr-folder + "/l-pprice.d").
  OS-DELETE VALUE(curr-folder + "/l-kredit.d").
  OS-DELETE VALUE(curr-folder + "/ap-journ.d").
  OS-DELETE VALUE(curr-folder + "/l-artike.d").
  OS-DELETE VALUE(curr-folder + "/l-besta1.d").
  OS-DELETE VALUE(curr-folder + "/l-hauptg.d").
  OS-DELETE VALUE(curr-folder + "/l-lager.d").
  OS-DELETE VALUE(curr-folder + "/l-liefer.d").
  OS-DELETE VALUE(curr-folder + "/l-liefum.d").
  OS-DELETE VALUE(curr-folder + "/l-ophhis.d").
  OS-DELETE VALUE(curr-folder + "/l-ophis.d").
  OS-DELETE VALUE(curr-folder + "/l-order.d").
  OS-DELETE VALUE(curr-folder + "/l-orderh.d").
  OS-DELETE VALUE(curr-folder + "/l-quote.d").
  OS-DELETE VALUE(curr-folder + "/l-segmen.d").
  OS-DELETE VALUE(curr-folder + "/l-umsatz.d").
  OS-DELETE VALUE(curr-folder + "/l-unterg.d").
  OS-DELETE VALUE(curr-folder + "/l-verbra.d").
  OS-DELETE VALUE(curr-folder + "/l-zahlbe.d").

    
  FOR EACH l-bestand NO-LOCK: 
      CREATE t-l-bestand.
      BUFFER-COPY l-bestand TO t-l-bestand.
  END.
  
  FOR EACH l-op NO-LOCK BY l-op.datum:
      CREATE t-l-op.
      BUFFER-COPY l-op TO t-l-op.
  END.
    
  FOR EACH l-ophdr NO-LOCK:
      CREATE t-l-ophdr.
      BUFFER-COPY l-ophdr TO t-l-ophdr.
  END.
  
  FOR EACH l-pprice NO-LOCK:
      CREATE t-l-pprice.
      BUFFER-COPY l-pprice TO t-l-pprice.
  END.
    
  FOR EACH l-kredit NO-LOCK:
      CREATE t-l-kredit.
      BUFFER-COPY l-kredit TO t-l-kredit.
  END.

  FOR EACH ap-journal NO-LOCK:
      CREATE t-ap-journal.
      BUFFER-COPY ap-journal TO t-ap-journal.
  END.

  FOR EACH l-artikel NO-LOCK:
      CREATE t-l-artikel.
      BUFFER-COPY l-artikel TO t-l-artikel.
  END.

  FOR EACH l-besthis NO-LOCK:
      CREATE t-l-besthis.
      BUFFER-COPY l-besthis TO t-l-besthis.
  END.

  FOR EACH l-hauptgrp NO-LOCK:
      CREATE t-l-hauptgrp.
      BUFFER-COPY l-hauptgrp TO t-l-hauptgrp.
  END.
    
  FOR EACH l-lager NO-LOCK:
      CREATE t-l-lager.
      BUFFER-COPY l-lager TO t-l-lager.
  END.
    
  FOR EACH l-lieferant NO-LOCK:
      CREATE t-l-lieferant.
      BUFFER-COPY l-lieferant TO t-l-lieferant.
  END.
    
  FOR EACH l-liefumsatz NO-LOCK:
      CREATE t-l-liefumsatz.
      BUFFER-COPY l-liefumsatz TO t-l-liefumsatz.
  END.
    
  FOR EACH l-ophhis NO-LOCK:
      CREATE t-l-ophhis.
      BUFFER-COPY l-ophhis TO t-l-ophhis.
  END.
    
  FOR EACH l-ophis NO-LOCK:
      CREATE t-l-ophis.
      BUFFER-COPY l-ophis TO t-l-ophis.
  END.
    
  FOR EACH l-order NO-LOCK:
      CREATE t-l-order.
      BUFFER-COPY l-order TO t-l-order.
  END.
    
  FOR EACH l-orderhdr NO-LOCK:
      CREATE t-l-orderhdr.
      BUFFER-COPY l-orderhdr TO t-l-orderhdr.
  END.
    
  FOR EACH l-quote NO-LOCK:
      CREATE t-l-quote.
      BUFFER-COPY l-quote TO t-l-quote.
  END.
    
  FOR EACH l-segment NO-LOCK:
      CREATE t-l-segment.
      BUFFER-COPY l-segment TO t-l-segment.
  END.
    
  FOR EACH l-umsatz NO-LOCK:
      CREATE t-l-umsatz.
      BUFFER-COPY l-umsatz TO t-l-umsatz.
  END.
    
  FOR EACH l-untergrup NO-LOCK:
      CREATE t-l-untergrup.
      BUFFER-COPY l-untergrup TO t-l-untergrup.
  END.
    
  FOR EACH l-verbrauch NO-LOCK:
      CREATE t-l-verbrauch.
      BUFFER-COPY l-verbrauch TO t-l-verbrauch.
  END.
    
  FOR EACH l-zahlbed NO-LOCK:
      CREATE t-l-zahlbed.
      BUFFER-COPY l-zahlbed TO t-l-zahlbed.
  END.

  FOR EACH h-rezept NO-LOCK:
      CREATE t-h-rezept.
      BUFFER-COPY h-rezept TO t-h-rezept.
  END.

  FOR EACH h-rezlin NO-LOCK:
      CREATE t-h-rezlin.
      BUFFER-COPY h-rezlin TO t-h-rezlin.
  END.

END PROCEDURE. 



PROCEDURE create-file:
  OUTPUT STREAM s1 TO VALUE(curr-folder + "/l-bestan.d").   
  FOR EACH t-l-bestand NO-LOCK:   
    EXPORT STREAM s1 t-l-bestand.     
  END.  
  OUTPUT STREAM s1 CLOSE.   

  CREATE tlist.
  ASSIGN tlist.table-name = "l-bestan.d".
  COPY-LOB FROM FILE curr-folder + "/l-bestan.d" TO tlist.objfile.
   
  OUTPUT STREAM s1 TO VALUE(curr-folder + "/l-op.d").   
  FOR EACH t-l-op NO-LOCK:   
    EXPORT STREAM s1 t-l-op.       
  END.   
  OUTPUT STREAM s1 CLOSE.   

  CREATE tlist.
  ASSIGN tlist.table-name = "l-op.d".
  COPY-LOB FROM FILE curr-folder + "/l-op.d" TO tlist.objfile.
   
  OUTPUT STREAM s1 TO VALUE(curr-folder + "/l-ophdr.d").   
  FOR EACH t-l-ophdr NO-LOCK:   
    EXPORT STREAM s1 t-l-ophdr.   
  END.   
  OUTPUT STREAM s1 CLOSE.   

  CREATE tlist.
  ASSIGN tlist.table-name = "l-ophdr.d".
  COPY-LOB FROM FILE curr-folder + "/l-ophdr.d" TO tlist.objfile.
   
  OUTPUT STREAM s1 TO VALUE(curr-folder + "/l-pprice.d").   
  FOR EACH t-l-pprice NO-LOCK:   
    EXPORT STREAM s1 t-l-pprice.   
  END.   
  OUTPUT STREAM s1 CLOSE.   

  CREATE tlist.
  ASSIGN tlist.table-name = "l-pprice.d".
  COPY-LOB FROM FILE curr-folder + "/l-pprice.d" TO tlist.objfile.
   
  OUTPUT STREAM s1 TO VALUE(curr-folder + "/l-kredit.d").   
  FOR EACH t-l-kredit NO-LOCK:   
    EXPORT STREAM s1 t-l-kredit.   
  END.   
  OUTPUT STREAM s1 CLOSE.   

  CREATE tlist.
  ASSIGN tlist.table-name = "l-kredit.d".
  COPY-LOB FROM FILE curr-folder + "/l-kredit.d" TO tlist.objfile.

  OUTPUT STREAM s1 TO VALUE(curr-folder + "/ap-journ.d"). 
  FOR EACH t-ap-journal NO-LOCK: 
    EXPORT STREAM s1 t-ap-journal. 
  END. 
  OUTPUT STREAM s1 CLOSE. 

  CREATE tlist.
  ASSIGN tlist.table-name = "ap-journ.d".
  COPY-LOB FROM FILE curr-folder + "/ap-journ.d" TO tlist.objfile.

  OUTPUT STREAM s1 TO VALUE(curr-folder + "/l-artike.d"). 
  FOR EACH t-l-artikel NO-LOCK: 
    EXPORT STREAM s1 t-l-artikel. 
  END. 
  OUTPUT STREAM s1 CLOSE. 

  CREATE tlist.
  ASSIGN tlist.table-name = "l-artike.d".
  COPY-LOB FROM FILE curr-folder + "/l-artike.d" TO tlist.objfile.

  OUTPUT STREAM s1 TO VALUE(curr-folder + "/l-besta1.d"). 
  FOR EACH t-l-besthis NO-LOCK: 
    EXPORT STREAM s1 t-l-besthis. 
  END. 
  OUTPUT STREAM s1 CLOSE. 

  CREATE tlist.
  ASSIGN tlist.table-name = "l-besta1.d".
  COPY-LOB FROM FILE curr-folder + "/l-besta1.d" TO tlist.objfile.

  OUTPUT STREAM s1 TO VALUE(curr-folder + "/l-hauptg.d"). 
  FOR EACH t-l-hauptgrp NO-LOCK: 
    EXPORT STREAM s1 t-l-hauptgrp. 
  END. 
  OUTPUT STREAM s1 CLOSE. 

  CREATE tlist.
  ASSIGN tlist.table-name = "l-hauptg.d".
  COPY-LOB FROM FILE curr-folder + "/l-hauptg.d" TO tlist.objfile.

  OUTPUT STREAM s1 TO VALUE(curr-folder + "/l-lager.d"). 
  FOR EACH t-l-lager NO-LOCK: 
    EXPORT STREAM s1 t-l-lager. 
  END. 
  OUTPUT STREAM s1 CLOSE. 

  CREATE tlist.
  ASSIGN tlist.table-name = "l-lager.d".
  COPY-LOB FROM FILE curr-folder + "/l-lager.d" TO tlist.objfile.

  OUTPUT STREAM s1 TO VALUE(curr-folder + "/l-liefer.d"). 
  FOR EACH t-l-lieferant NO-LOCK: 
    EXPORT STREAM s1 t-l-lieferant. 
  END. 
  OUTPUT STREAM s1 CLOSE. 

  CREATE tlist.
  ASSIGN tlist.table-name = "l-liefer.d".
  COPY-LOB FROM FILE curr-folder + "/l-liefer.d" TO tlist.objfile.

  OUTPUT STREAM s1 TO VALUE(curr-folder + "/l-liefum.d"). 
  FOR EACH t-l-liefumsatz NO-LOCK: 
    EXPORT STREAM s1 t-l-liefumsatz. 
  END. 
  OUTPUT STREAM s1 CLOSE. 

  CREATE tlist.
  ASSIGN tlist.table-name = "l-liefum.d".
  COPY-LOB FROM FILE curr-folder + "/l-liefum.d" TO tlist.objfile.

  OUTPUT STREAM s1 TO VALUE(curr-folder + "/l-ophhis.d"). 
  FOR EACH t-l-ophhis NO-LOCK: 
    EXPORT STREAM s1 t-l-ophhis. 
  END. 
  OUTPUT STREAM s1 CLOSE. 

  CREATE tlist.
  ASSIGN tlist.table-name = "l-ophhis.d".
  COPY-LOB FROM FILE curr-folder + "/l-ophhis.d" TO tlist.objfile.

  OUTPUT STREAM s1 TO VALUE(curr-folder + "/l-ophis.d"). 
  FOR EACH t-l-ophis NO-LOCK: 
    EXPORT STREAM s1 t-l-ophis. 
  END. 
  OUTPUT STREAM s1 CLOSE. 

  CREATE tlist.
  ASSIGN tlist.table-name = "l-ophis.d".
  COPY-LOB FROM FILE curr-folder + "/l-ophis.d" TO tlist.objfile.

  OUTPUT STREAM s1 TO VALUE(curr-folder + "/l-order.d"). 
  FOR EACH t-l-order NO-LOCK: 
    EXPORT STREAM s1 t-l-order. 
  END. 
  OUTPUT STREAM s1 CLOSE. 

  CREATE tlist.
  ASSIGN tlist.table-name = "l-order.d".
  COPY-LOB FROM FILE curr-folder + "/l-order.d" TO tlist.objfile.

  OUTPUT STREAM s1 TO VALUE(curr-folder + "/l-orderh.d"). 
  FOR EACH t-l-orderhdr NO-LOCK: 
    EXPORT STREAM s1 t-l-orderhdr. 
  END. 
  OUTPUT STREAM s1 CLOSE. 

  CREATE tlist.
  ASSIGN tlist.table-name = "l-orderh.d".
  COPY-LOB FROM FILE curr-folder + "/l-orderh.d" TO tlist.objfile.

  OUTPUT STREAM s1 TO VALUE(curr-folder + "/l-quote.d"). 
  FOR EACH t-l-quote NO-LOCK: 
    EXPORT STREAM s1 t-l-quote. 
  END. 
  OUTPUT STREAM s1 CLOSE. 

  CREATE tlist.
  ASSIGN tlist.table-name = "l-quote.d".
  COPY-LOB FROM FILE curr-folder + "/l-quote.d" TO tlist.objfile.

  OUTPUT STREAM s1 TO VALUE(curr-folder + "/l-segmen.d"). 
  FOR EACH t-l-segment NO-LOCK: 
    EXPORT STREAM s1 t-l-segment. 
  END. 
  OUTPUT STREAM s1 CLOSE. 

  CREATE tlist.
  ASSIGN tlist.table-name = "l-segmen.d".
  COPY-LOB FROM FILE curr-folder + "/l-segmen.d" TO tlist.objfile.

  OUTPUT STREAM s1 TO VALUE(curr-folder + "/l-umsatz.d"). 
  FOR EACH t-l-umsatz NO-LOCK: 
    EXPORT STREAM s1 t-l-umsatz. 
  END. 
  OUTPUT STREAM s1 CLOSE. 

  CREATE tlist.
  ASSIGN tlist.table-name = "l-umsatz.d".
  COPY-LOB FROM FILE curr-folder + "/l-umsatz.d" TO tlist.objfile.

  OUTPUT STREAM s1 TO VALUE(curr-folder + "/l-unterg.d"). 
  FOR EACH t-l-untergrup NO-LOCK: 
    EXPORT STREAM s1 t-l-untergrup. 
  END. 
  OUTPUT STREAM s1 CLOSE. 

  CREATE tlist.
  ASSIGN tlist.table-name = "l-unterg.d".
  COPY-LOB FROM FILE curr-folder + "/l-unterg.d" TO tlist.objfile.
                                                          
  OUTPUT STREAM s1 TO VALUE(curr-folder + "/l-verbra.d"). 
  FOR EACH t-l-verbrauch NO-LOCK: 
    EXPORT STREAM s1 t-l-verbrauch. 
  END. 
  OUTPUT STREAM s1 CLOSE. 

  CREATE tlist.
  ASSIGN tlist.table-name = "l-verbra.d".
  COPY-LOB FROM FILE curr-folder + "/l-verbra.d" TO tlist.objfile.

  OUTPUT STREAM s1 TO VALUE(curr-folder + "/l-zahlbe.d"). 
  FOR EACH t-l-zahlbed NO-LOCK: 
    EXPORT STREAM s1 t-l-zahlbed. 
  END. 
  OUTPUT STREAM s1 CLOSE. 

  CREATE tlist.
  ASSIGN tlist.table-name = "l-zahlbe.d".
  COPY-LOB FROM FILE curr-folder + "/l-zahlbe.d" TO tlist.objfile.

  OUTPUT STREAM s1 TO VALUE(curr-folder + "/h-rezept.d"). 
  FOR EACH t-h-rezept NO-LOCK: 
    EXPORT STREAM s1 t-h-rezept. 
  END. 
  OUTPUT STREAM s1 CLOSE. 

  CREATE tlist.
  ASSIGN tlist.table-name = "h-rezept.d".
  COPY-LOB FROM FILE curr-folder + "/h-rezept.d" TO tlist.objfile.

  OUTPUT STREAM s1 TO VALUE(curr-folder + "/h-rezlin.d"). 
  FOR EACH t-h-rezlin NO-LOCK: 
    EXPORT STREAM s1 h-rezlin. 
  END. 
  OUTPUT STREAM s1 CLOSE. 

  CREATE tlist.
  ASSIGN tlist.table-name = "h-rezlin.d".
  COPY-LOB FROM FILE curr-folder + "/h-rezlin.d" TO tlist.objfile.
END.


PROCEDURE decode-string: 
    DEFINE INPUT PARAMETER in-str   AS CHAR. 
    DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "". 
    DEFINE VARIABLE s   AS CHAR. 
    DEFINE VARIABLE j   AS INTEGER. 
    DEFINE VARIABLE len AS INTEGER. 
      s = in-str. 
      j = ASC(SUBSTR(s, 1, 1)) - 70. 
      len = LENGTH(in-str) - 1. 
      s = SUBSTR(in-str, 2, len). 
      DO len = 1 TO LENGTH(s): 
        out-str = out-str + chr(asc(SUBSTR(s,len,1)) - j). 
      END. 
END. 

/*
PROCEDURE dump-files: 
 
  FOR EACH l-bestand NO-LOCK: 
      CREATE t-l-bestand.
      BUFFER-COPY l-bestand TO t-l-bestand.
  END.
  
  FOR EACH l-op NO-LOCK BY l-op.datum:
      CREATE t-l-op.
      BUFFER-COPY l-op TO t-l-op.
  END.
    
  FOR EACH l-ophdr NO-LOCK:
      CREATE t-l-ophdr.
      BUFFER-COPY l-ophdr TO t-l-ophdr.
  END.
    
  FOR EACH l-pprice NO-LOCK:
      CREATE t-l-pprice.
      BUFFER-COPY l-pprice TO t-l-pprice.
  END.
    
  FOR EACH l-kredit NO-LOCK:
      CREATE t-l-kredit.
      BUFFER-COPY l-kredit TO t-l-kredit.
  END.

 
  FOR EACH ap-journal NO-LOCK:
      CREATE t-ap-journal.
      BUFFER-COPY ap-journal TO t-ap-journal.
  END.

  FOR EACH l-artikel NO-LOCK:
      CREATE t-l-artikel.
      BUFFER-COPY l-artikel TO t-l-artikel.
  END.

  FOR EACH l-besthis NO-LOCK:
      CREATE t-l-besthis.
      BUFFER-COPY l-besthis TO t-l-besthis.
  END.

  FOR EACH l-hauptgrp NO-LOCK:
      CREATE t-l-hauptgrp.
      BUFFER-COPY l-hauptgrp TO t-l-hauptgrp.
  END.
    
  FOR EACH l-lager NO-LOCK:
      CREATE t-l-lager.
      BUFFER-COPY l-lager TO t-l-lager.
  END.
    
  FOR EACH l-lieferant NO-LOCK:
      CREATE t-l-lieferant.
      BUFFER-COPY l-lieferant TO t-l-lieferant.
  END.
    
  FOR EACH l-liefumsatz NO-LOCK:
      CREATE t-l-liefumsatz.
      BUFFER-COPY l-liefumsatz TO t-l-liefumsatz.
  END.
    
  FOR EACH l-ophhis NO-LOCK:
      CREATE t-l-ophhis.
      BUFFER-COPY l-ophhis TO t-l-ophhis.
  END.
    
  FOR EACH l-ophis NO-LOCK:
      CREATE t-l-ophis.
      BUFFER-COPY l-ophis TO t-l-ophis.
  END.
    
  FOR EACH l-order NO-LOCK:
      CREATE t-l-order.
      BUFFER-COPY l-order TO t-l-order.
  END.
    
  FOR EACH l-orderhdr NO-LOCK:
      CREATE t-l-orderhdr.
      BUFFER-COPY l-orderhdr TO t-l-orderhdr.
  END.
    
  FOR EACH l-quote NO-LOCK:
      CREATE t-l-quote.
      BUFFER-COPY l-quote TO t-l-quote.
  END.
    
  FOR EACH l-segment NO-LOCK:
      CREATE t-l-segment.
      BUFFER-COPY l-segment TO t-l-segment.
  END.
    
  FOR EACH l-umsatz NO-LOCK:
      CREATE t-l-umsatz.
      BUFFER-COPY l-umsatz TO t-l-umsatz.
  END.
    
  FOR EACH l-untergrup NO-LOCK:
      CREATE t-l-untergrup.
      BUFFER-COPY l-untergrup TO t-l-untergrup.
  END.
    
  FOR EACH l-verbrauch NO-LOCK:
      CREATE t-l-verbrauch.
      BUFFER-COPY l-verbrauch TO t-l-verbrauch.
  END.
    
  FOR EACH l-zahlbed NO-LOCK:
      CREATE t-l-zahlbed.
      BUFFER-COPY l-zahlbed TO t-l-zahlbed.
  END.

  /*MT
  /*MTcurr-anz = 0.*/
  curr-bezeich = translateExtended ("Dump Files contents",lvCAREA,""). 
 
  OUTPUT STREAM s1 TO "l-bestan.d". 
  FOR EACH l-bestand NO-LOCK: 
    EXPORT STREAM s1 l-bestand. 
    /*MTcurr-anz = curr-anz + 1.*/
    DISP curr-bezeich /*MTcurr-anz*/ WITH FRAME frame1. 
  END. 
  OUTPUT STREAM s1 CLOSE. 
 
  OUTPUT STREAM s1 TO "l-op.d". 
  FOR EACH l-op NO-LOCK: 
    EXPORT STREAM s1 l-op. 
    /*MTcurr-anz = curr-anz + 1.*/
    DISP curr-bezeich /*MTcurr-anz*/ WITH FRAME frame1. 
  END. 
  OUTPUT STREAM s1 CLOSE. 
 
  OUTPUT STREAM s1 TO "l-ophdr.d". 
  FOR EACH l-ophdr NO-LOCK: 
    EXPORT STREAM s1 l-ophdr. 
    /*MTcurr-anz = curr-anz + 1.*/
    DISP curr-bezeich /*MTcurr-anz*/ WITH FRAME frame1. 
  END. 
  OUTPUT STREAM s1 CLOSE. 
 
  OUTPUT STREAM s1 TO "l-pprice.d". 
  FOR EACH l-pprice NO-LOCK: 
    EXPORT STREAM s1 l-pprice. 
    /*MTcurr-anz = curr-anz + 1.*/
    DISP curr-bezeich /*MTcurr-anz*/ WITH FRAME frame1. 
  END. 
  OUTPUT STREAM s1 CLOSE. 
 
  OUTPUT STREAM s1 TO "l-kredit.d". 
  FOR EACH l-kredit NO-LOCK: 
    EXPORT STREAM s1 l-kredit. 
    /*MTcurr-anz = curr-anz + 1.*/
    DISP curr-bezeich /*MTcurr-anz*/ WITH FRAME frame1. 
  END. 
  OUTPUT STREAM s1 CLOSE. 
  */
END PROCEDURE. */

