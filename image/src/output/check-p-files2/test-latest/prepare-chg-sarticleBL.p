{tb-guestbook.i}

DEFINE TEMP-TABLE l-art LIKE l-artikel.
DEFINE TEMP-TABLE t-l-art   
    FIELD artnr     LIKE l-artikel.artnr
    FIELD endkum    LIKE l-artikel.endkum
    FIELD zwkum     LIKE l-artikel.zwkum
    FIELD t-recid   AS INT.

DEF TEMP-TABLE tt-artnr
    FIELD curr-i    AS INTEGER
    FIELD ss-artnr  AS INTEGER
.
DEF TEMP-TABLE tt-content
    FIELD curr-i     AS INTEGER
    FIELD ss-content AS INTEGER
.
DEF TEMP-TABLE tt-bezeich
    FIELD curr-i     AS INTEGER
    FIELD ss-bezeich AS CHAR
.

/*IF 250319 - Show Picture from guestbook*/
DEFINE TEMP-TABLE ttGuestBook NO-UNDO LIKE vhp.guestBook.
/*END IF*/

DEFINE INPUT PARAMETER artnr        AS INT      NO-UNDO.
DEFINE INPUT PARAMETER changed      AS LOGICAL  NO-UNDO.
DEFINE OUTPUT PARAMETER fibukonto   AS CHAR     NO-UNDO INIT "".
DEFINE OUTPUT PARAMETER dml-art     AS LOGICAL  NO-UNDO INIT NO.
DEFINE OUTPUT PARAMETER bez-aend    AS LOGICAL  NO-UNDO INIT NO.
DEFINE OUTPUT PARAMETER s-unit      AS CHAR     NO-UNDO INIT "".

DEFINE OUTPUT PARAMETER TABLE FOR tt-artnr.
DEFINE OUTPUT PARAMETER TABLE FOR tt-content.
DEFINE OUTPUT PARAMETER TABLE FOR tt-bezeich.

DEFINE OUTPUT PARAMETER pict-file   AS CHAR     NO-UNDO INIT "". 
DEFINE OUTPUT PARAMETER recipe-bez  AS CHAR     NO-UNDO INIT "". 
DEFINE OUTPUT PARAMETER firma1      AS CHAR     NO-UNDO INIT "". 
DEFINE OUTPUT PARAMETER firma2      AS CHAR     NO-UNDO INIT "". 
DEFINE OUTPUT PARAMETER firma3      AS CHAR     NO-UNDO INIT "". 
DEFINE OUTPUT PARAMETER zw-bezeich  AS CHAR     NO-UNDO INIT "". 
DEFINE OUTPUT PARAMETER end-bezeich AS CHAR     NO-UNDO INIT "". 
DEFINE OUTPUT PARAMETER set-disp1   AS LOGICAL  NO-UNDO INIT NO.
DEFINE OUTPUT PARAMETER set-disp2   AS LOGICAL  NO-UNDO INIT NO.
DEFINE OUTPUT PARAMETER set-disp3   AS LOGICAL  NO-UNDO INIT NO.
DEFINE OUTPUT PARAMETER set-disp4   AS LOGICAL  NO-UNDO INIT NO.
DEFINE OUTPUT PARAMETER artnr-ok    AS LOGICAL  NO-UNDO INIT NO.
DEFINE OUTPUT PARAMETER TABLE FOR l-art.
DEFINE OUTPUT PARAMETER TABLE FOR t-l-art.
/*IF 250319*/
DEFINE OUTPUT PARAMETER TABLE FOR ttGuestBook.
/*END IF*/

/*M
DEFINE variable artnr        AS INT      NO-UNDO.
DEFINE variable changed      AS LOGICAL  NO-UNDO.
DEFINE variable fibukonto   AS CHAR     NO-UNDO INIT "".
DEFINE variable dml-art     AS LOGICAL  NO-UNDO INIT NO.
DEFINE variable bez-aend    AS LOGICAL  NO-UNDO INIT NO.
DEFINE variable s-unit      AS CHAR     NO-UNDO INIT "".
DEFINE variable ss-artnr    AS INTEGER  NO-UNDO EXTENT 3.
DEFINE variable ss-content  AS INTEGER  NO-UNDO EXTENT 3.
DEFINE variable ss-bezeich  AS CHAR     NO-UNDO EXTENT 3. 
DEFINE variable pict-file   AS CHAR     NO-UNDO INIT "". 
DEFINE variable recipe-bez  AS CHAR     NO-UNDO INIT "". 
DEFINE variable firma1      AS CHAR     NO-UNDO INIT "". 
DEFINE variable firma2      AS CHAR     NO-UNDO INIT "". 
DEFINE variable firma3      AS CHAR     NO-UNDO INIT "". 
DEFINE variable zw-bezeich  AS CHAR     NO-UNDO INIT "". 
DEFINE variable end-bezeich AS CHAR     NO-UNDO INIT "". 
DEFINE variable set-disp1   AS LOGICAL  NO-UNDO INIT NO.
DEFINE variable set-disp2   AS LOGICAL  NO-UNDO INIT NO.
DEFINE variable set-disp3   AS LOGICAL  NO-UNDO INIT NO.
DEFINE variable set-disp4   AS LOGICAL  NO-UNDO INIT NO.
DEFINE variable artnr-ok    AS LOGICAL  NO-UNDO INIT NO.
*/

DEF VAR ss-artnr   AS INTEGER EXTENT 3 NO-UNDO INIT [0,0,0].
DEF VAR ss-content AS INTEGER EXTENT 3 NO-UNDO INIT [0,0,0].
DEF VAR ss-bezeich AS CHAR    EXTENT 3 NO-UNDO INIT ["","",""].

DEF VAR i-counter  AS INTEGER          NO-UNDO.

/*IF 250319*/
DEFINE VARIABLE strArtnr    AS CHARACTER NO-UNDO.
/*END IF*/
DEFINE VARIABLE lp-price    AS INTEGER NO-UNDO.

FIND FIRST l-artikel WHERE l-artikel.artnr = artnr NO-LOCK NO-ERROR.
IF NOT AVAILABLE l-artikel THEN RETURN.
fibukonto = l-artikel.fibukonto. 
IF l-artikel.fibukonto = "" THEN fibukonto = "00000000000000000000". 
 
IF NOT l-artikel.herkunft MATCHES ("*;*") THEN
DO:
  DEF BUFFER lbuff FOR l-artikel.
  FIND FIRST lbuff WHERE RECID(lbuff) = RECID(l-artikel) EXCLUSIVE-LOCK.
  lbuff.herkunft = lbuff.herkunft + ";".
  FIND CURRENT lbuff NO-LOCK.
END.

/*IF 250319 - Show Picture from GuestBook*/
strArtnr = "*" + STRING(artnr) + "*".

FIND FIRST guestbook WHERE guestbook.infostr MATCHES strArtnr NO-LOCK NO-ERROR.
IF AVAILABLE guestbook THEN
DO:
    CREATE ttGuestBook.
    BUFFER-COPY guestbook TO ttGuestBook.   
END.
/*END IF*/

CREATE l-art. 
RUN fill-lart. 
 
IF changed THEN 
DO: 
  FIND FIRST l-bestand WHERE l-bestand.artnr = artnr 
    AND l-bestand.lager-nr = 0 NO-LOCK NO-ERROR. 
  IF AVAILABLE l-bestand THEN set-disp1 = YES.  
  
  IF l-art.vk-preis NE 0 THEN set-disp2 = YES. 

  FIND FIRST l-ophis WHERE l-ophis.artnr = artnr NO-LOCK NO-ERROR.
  IF AVAILABLE l-ophis THEN set-disp3 = YES.
  
  RUN check-artno(OUTPUT artnr-ok). 

END. 
ELSE 
  FIND FIRST l-artikel WHERE l-artikel.artnr = artnr NO-LOCK. 
 
FIND FIRST htparam WHERE htparam.paramnr = 911 NO-LOCK.
IF htparam.paramgr = 21 AND htparam.flogical THEN set-disp4 = YES.

IF l-artikel.betriebsnr NE 0 THEN 
DO: 
  FIND FIRST h-rezept WHERE h-rezept.artnrrezept = l-artikel.betriebsnr 
    NO-LOCK NO-ERROR. 
  IF AVAILABLE h-rezept THEN recipe-bez = h-rezept.bezeich. 
END. 
 
IF l-art.lief-nr1 NE 0 THEN 
DO: 
  FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = l-art.lief-nr1 
  NO-LOCK NO-ERROR. 
  IF AVAILABLE l-lieferant THEN firma1 = l-lieferant.firma. 
END. 
IF l-art.lief-nr2 NE 0 THEN 
DO: 
  FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = l-art.lief-nr2 
  NO-LOCK NO-ERROR. 
  IF AVAILABLE l-lieferant THEN firma2 = l-lieferant.firma. 
END. 
IF l-art.lief-nr3 NE 0 THEN 
DO: 
  FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = l-art.lief-nr3 
  NO-LOCK NO-ERROR. 
  IF AVAILABLE l-lieferant THEN firma3 = l-lieferant.firma. 
END. 
 
IF l-art.zwkum NE 0 THEN 
DO: 
  FIND FIRST l-untergrup WHERE l-untergrup.zwkum = l-art.zwkum 
    NO-LOCK NO-ERROR. 
  IF AVAILABLE l-untergrup THEN zw-bezeich = l-untergrup.bezeich. 
END. 
 
IF l-art.endkum NE 0 THEN 
DO: 
  FIND FIRST l-hauptgrp WHERE l-hauptgrp.endkum = l-art.endkum 
    NO-LOCK NO-ERROR. 
  IF AVAILABLE l-hauptgrp THEN end-bezeich = l-hauptgrp.bezeich. 
END. 

CREATE t-l-art.
BUFFER-COPY l-artikel TO t-l-art.
t-l-art.t-recid = RECID(l-artikel).

/*************************** PROCEDURES ****************************************/ 

PROCEDURE check-artno: 
DEFINE OUTPUT PARAMETER its-ok AS LOGICAL INITIAL YES. 
DEFINE VARIABLE nr AS INTEGER. 
DEFINE VARIABLE s AS CHAR. 
  IF l-art.zwkum GT 99 THEN nr = l-art.endkum * 1000 + l-art.zwkum. 
  ELSE nr = l-art.endkum * 100 + l-art.zwkum. 
  IF nr GT 999 THEN s = SUBSTR(STRING(l-art.artnr),1,4). 
  ELSE s = SUBSTR(STRING(l-art.artnr),1,3). 
  its-ok = (s = STRING(nr)). 
END. 

PROCEDURE fill-lart: 
DEF BUFFER l-art1 FOR l-artikel. 
 
  dml-art = l-artikel.bestellt. 
  IF l-artikel.jahrgang = 0 THEN bez-aend = NO. 
  ELSE bez-aend = YES. 
  ASSIGN
    l-art.artnr = l-artikel.artnr
    l-art.fibukonto = l-artikel.fibukonto
    l-art.bezeich = l-artikel.bezeich
    l-art.zwkum = l-artikel.zwkum
    l-art.endkum = l-artikel.endkum 
    l-art.herkunft = ENTRY(1, l-artikel.herkunft, ";")
    s-unit = ENTRY(2, l-artikel.herkunft, ";")
    l-art.masseinheit = l-artikel.masseinheit
    l-art.betriebsnr = l-artikel.betriebsnr
    l-art.inhalt = l-artikel.inhalt
    l-art.traubensort = l-artikel.traubensort
    l-art.lief-einheit = l-artikel.lief-einheit 
    l-art.min-bestand = l-artikel.min-bestand
    l-art.anzverbrauch = l-artikel.anzverbrauch 
    l-art.alkoholgrad = l-artikel.alkoholgrad
    l-art.lief-nr1 = l-artikel.lief-nr1
    l-art.lief-artnr[1] = l-artikel.lief-artnr[2]
    l-art.lief-nr2 = l-artikel.lief-nr2
    l-art.lief-artnr[2] = l-artikel.lief-artnr[2] 
    l-art.lief-nr3 = l-artikel.lief-nr3
    l-art.lief-artnr[3] = l-artikel.lief-artnr[3]
    l-art.ek-aktuell = l-artikel.ek-aktuell
    l-art.ek-letzter = l-artikel.ek-letzter 
    l-art.vk-preis = l-artikel.vk-preis
  . 
 
  FIND FIRST queasy WHERE queasy.KEY = 20 AND queasy.number1 = l-artikel.artnr 
      NO-LOCK NO-ERROR. 
  IF AVAILABLE queasy THEN 
  DO: 
      ASSIGN
        ss-artnr[1]   = INTEGER(queasy.deci1) 
        ss-artnr[2]   = INTEGER(queasy.deci2) 
        ss-artnr[3]   = INTEGER(queasy.deci3) 
      .
      IF LENGTH(queasy.char3) = 12 THEN
      ASSIGN
        ss-content[1] = INTEGER(SUBSTR(queasy.char3,1,3)) 
        ss-content[2] = INTEGER(SUBSTR(queasy.char3,5,3)) 
        ss-content[3] = INTEGER(SUBSTR(queasy.char3,9,3))
      .
      ELSE      
      ASSIGN
        ss-content[1] = INTEGER(SUBSTR(queasy.char2,1,3)) 
        ss-content[2] = INTEGER(SUBSTR(queasy.char2,5,3)) 
        ss-content[3] = INTEGER(SUBSTR(queasy.char2,9,3))
        pict-file  = queasy.char3 NO-ERROR
      .

      DO i-counter = 1 TO 3:
          CREATE tt-artnr.
          ASSIGN
               tt-artnr.curr-i   = i-counter
               tt-artnr.ss-artnr = ss-artnr[i-counter]
          .
      END.
      DO i-counter = 1 TO 3:
          CREATE tt-content.
          ASSIGN
               tt-content.curr-i   = i-counter
               tt-content.ss-content = ss-content[i-counter]
          .
      END.
      DO i-counter = 1 TO 3:
          CREATE tt-bezeich.
          ASSIGN
               tt-bezeich.curr-i   = i-counter
               tt-bezeich.ss-bezeich = ss-bezeich[i-counter]
          .
      END.

      IF ss-artnr[1] NE 0 THEN 
      DO: 
          FIND FIRST l-art1 WHERE l-art1.artnr = ss-artnr[1] NO-LOCK NO-ERROR. 
          IF AVAILABLE l-art1 THEN ss-bezeich[1] = l-art1.bezeich. 
      END. 
      IF ss-artnr[2] NE 0 THEN 
      DO: 
          FIND FIRST l-art1 WHERE l-art1.artnr = ss-artnr[2] NO-LOCK NO-ERROR. 
          IF AVAILABLE l-art1 THEN ss-bezeich[2] = l-art1.bezeich. 
      END. 
      IF ss-artnr[3] NE 0 THEN 
      DO: 
          FIND FIRST l-art1 WHERE l-art1.artnr = ss-artnr[3] NO-LOCK NO-ERROR. 
          IF AVAILABLE l-art1 THEN ss-bezeich[3] = l-art1.bezeich. 
      END. 
  END. 
END. 
