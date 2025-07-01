DEFINE TEMP-TABLE slist
    FIELD bjournal AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" LABEL "BillJournal"
    FIELD genstat  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" LABEL "Genstat"
    FIELD paxGenstat AS INTEGER FORMAT ">>>,>>9" LABEL "PaxGenstat"
    FIELD segmstat  AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" LABEL "SegmentStat"
    FIELD paxSegm   AS INTEGER FORMAT ">>>,>>9" LABEL "PaxSegm".

DEF INPUT PARAMETER lodg-artnr AS INT.
DEF INPUT PARAMETER date1 AS DATE.
DEF OUTPUT PARAMETER flag AS INT INIT 0.
DEF OUTPUT PARAMETER TABLE FOR slist.

DEFINE VARIABLE vat         AS DECIMAL.
DEFINE VARIABLE service     AS DECIMAL.
DEFINE VARIABLE d           AS DECIMAL.

FIND FIRST artikel WHERE artikel.artnr = lodg-artnr AND artikel.departement
    = 0 NO-LOCK NO-ERROR.
IF NOT AVAILABLE artikel THEN
DO:
    flag = 1.
    /*MTHIDE MESSAGE NO-PAUSE.
    MESSAGE "Artikel doesn't exist!"
        VIEW-AS ALERT-BOX INFORMATION.
    lodg-artnr = 100.
    DISP lodg-artnr WITH FRAME frame1.
    APPLY "entry" TO lodg-artnr.*/
    RETURN NO-APPLY.
END.
ELSE
DO:
    ASSIGN
      service = 0 
      vat = 0
    . 
    FOR EACH slist:
        DELETE slist.
    END.
    CREATE slist.
    FOR EACH billjournal WHERE billjournal.bill-datum = date1 
        AND billjournal.departement = 0 
        AND billjournal.artnr = lodg-artnr NO-LOCK:
        d = billjournal.betrag / (1 + vat + service).
        ASSIGN 
            slist.bjournal = slist.bjournal + d.
    END.
    FOR EACH segmentstat WHERE segmentstat.datum = date1 NO-LOCK:
        ASSIGN slist.segmstat = slist.segmstat + segmentstat.logis
            slist.paxsegm = slist.paxsegm + segmentstat.persanz 
            + segmentstat.kind1  + segmentstat.kind2 + segmentstat.gratis.
    END.
    FOR EACH genstat WHERE genstat.datum = date1 AND genstat.zinr NE "" 
        AND genstat.res-logic[2] EQ YES NO-LOCK:
        ASSIGN slist.genstat = slist.genstat + genstat.logis
            slist.paxgenstat = slist.paxgenstat +
            genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2
            + genstat.kind3.
    END.

    flag = 2.
    RETURN NO-APPLY.
END.
