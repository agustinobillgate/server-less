DEFINE WORKFILE w-list 
    FIELD nr AS INTEGER 
    FIELD wabkurz AS CHAR FORMAT "x(4)" LABEL "Curr". 

DEFINE WORKFILE cost-list 
    FIELD nr AS INTEGER 
    FIELD bezeich AS CHAR FORMAT "x(24)". 

DEFINE buffer l-order1 FOR l-order. 
DEFINE buffer l-supp   FOR l-lieferant.
DEFINE BUFFER l-order2 FOR l-order.
DEFINE BUFFER l-art    FOR l-artikel.

DEF TEMP-TABLE q2-list
    FIELD bestelldatum              LIKE l-orderhdr.bestelldatum
    FIELD bezeich                   LIKE cost-list.bezeich
    FIELD firma                     LIKE l-lieferant.firma
    FIELD docu-nr                   LIKE l-orderhdr.docu-nr
    FIELD l-orderhdr-lieferdatum    LIKE l-orderhdr.lieferdatum
    FIELD wabkurz                   LIKE w-list.wabkurz
    FIELD bestellart                LIKE l-orderhdr.bestellart
    FIELD gedruckt                  LIKE l-orderhdr.gedruckt
    FIELD l-orderhdr-besteller      LIKE l-orderhdr.besteller
    FIELD l-order-gedruckt          LIKE l-order1.gedruckt
    FIELD zeit                      LIKE l-order1.zeit
    FIELD lief-fax-2                LIKE l-order1.lief-fax[2]
    FIELD l-order-lieferdatum       LIKE l-order1.lieferdatum
    FIELD lief-fax-3                LIKE l-order1.lief-fax[3]
    FIELD lieferdatum-eff           LIKE l-order1.lieferdatum-eff
    FIELD lief-fax-1                LIKE l-order1.lief-fax[1]
    FIELD lief-nr                   LIKE l-order1.lief-nr
    FIELD username                  AS CHAR
    FIELD del-reason                AS CHAR FORMAT "x(32)" /* d 080520 Reason on delete*/
    FIELD tot-amount                AS DECIMAL
    .

/*sis 020315*/
DEFINE TEMP-TABLE q-list LIKE q2-list
    FIELD to-sort AS INTEGER.

DEF INPUT PARAMETER t-liefNo        AS INT.
DEF INPUT PARAMETER last-docu-nr    AS CHAR.
DEF INPUT PARAMETER sorttype        AS INT.
DEF INPUT PARAMETER deptnr          AS INT.
DEF INPUT PARAMETER all-supp        AS LOGICAL.
DEF INPUT PARAMETER stattype        AS INT.
DEF INPUT PARAMETER usrName         AS CHAR.
DEF INPUT PARAMETER from-date       AS DATE.
DEF INPUT PARAMETER to-date         AS DATE.
DEF INPUT PARAMETER billdate        AS DATE.
DEF INPUT PARAMETER dml-only        AS LOGICAL.
DEF INPUT PARAMETER app-sort        AS CHARACTER.

DEF OUTPUT PARAMETER first-docu-nr  AS CHAR.
DEF OUTPUT PARAMETER curr-docu-nr   AS CHAR.
DEF OUTPUT PARAMETER p-267          AS LOGICAL.
DEF OUTPUT PARAMETER last-docu-nr1  AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR q2-list.

DEFINE VARIABLE counter         AS INTEGER  NO-UNDO INIT 0.
DEFINE VARIABLE curr-counter    AS INTEGER NO-UNDO.
DEFINE VARIABLE last-to-sort    AS INTEGER NO-UNDO.
DEFINE VARIABLE temp-docu-nr    AS CHARACTER.
DEFINE VARIABLE temp-counter-nr AS INTEGER.
DEFINE VARIABLE approval        AS INTEGER.
DEFINE VARIABLE p-71            AS LOGICAL.
DEFINE VARIABLE loop            AS INTEGER.
DEFINE VARIABLE app-lvl         AS INTEGER.

DEFINE BUFFER q245 FOR queasy.

IF app-sort EQ "Approve 2" THEN
    ASSIGN approval = 1.
IF app-sort EQ "Approve 3" THEN
    ASSIGN approval = 2.
IF app-sort EQ "Approve 4" THEN
    ASSIGN approval = 3.

FIND FIRST htparam WHERE paramnr EQ 71 NO-LOCK.
IF htparam.paramgr EQ 21 THEN
    ASSIGN p-71 = htparam.flogical.

IF t-liefNo NE 0 THEN FIND FIRST l-supp WHERE l-supp.lief-nr = t-liefNo.
RUN create-costlist.
RUN currency-list.
FIND FIRST htparam WHERE paramnr = 267 NO-LOCK.
p-267 = htparam.flogical.
/*MTIF po-number NE "" THEN
  RUN disp-po.
ELSE
DO:*/

IF sorttype = 1 THEN 
DO:
    IF all-supp THEN 
    DO: 
      IF deptnr LT 0 THEN RUN disp-list1. 
      ELSE IF deptnr GT 0 THEN RUN disp-list11. 
    END. 
    IF NOT all-supp THEN 
    DO: 
      IF deptnr LT 0 THEN RUN disp-list2. 
      ELSE IF deptnr GT 0 THEN RUN disp-list22. 
    END. 
END. 
ELSE IF sorttype = 2 THEN 
DO: 
    IF all-supp THEN 
    DO: 
      IF deptnr LT 0 THEN RUN disp-list1a. 
      ELSE IF deptnr GT 0 THEN RUN disp-list11a. 
    END. 
    IF NOT all-supp THEN 
    DO: 
      IF deptnr LT 0 THEN RUN disp-list2a. 
      ELSE IF deptnr GT 0 THEN RUN disp-list22a. 
    END. 
END. 
ELSE IF sorttype = 3 THEN 
DO: 
    IF all-supp THEN 
    DO: 
      IF deptnr LT 0 THEN RUN disp-list1b. 
      ELSE IF deptnr GT 0 THEN RUN disp-list11b. 
    END. 
    IF NOT all-supp THEN 
    DO: 
      IF deptnr LT 0 THEN RUN disp-list2b. 
      ELSE IF deptnr GT 0 THEN RUN disp-list22b. 
    END. 
END. 
/*MTEND.*/

/*MTPROCEDURE disp-po:
  IF usrName = "" THEN 
  FOR EACH l-orderhdr 
      WHERE l-orderhdr.betriebsnr LE 1 
      AND l-orderhdr.docu-nr = po-number NO-LOCK, 
      FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
      FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
      FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
      FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
      AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
      BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
  END.
  ELSE IF usrName NE "" THEN 
  FOR EACH l-orderhdr 
      WHERE l-orderhdr.betriebsnr LE 1 
      AND l-orderhdr.docu-nr = po-number 
      AND l-orderhdr.besteller = usrName NO-LOCK, 
      FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
      FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
      FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
      FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
      AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
      BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
  END.
END.
*/

PROCEDURE disp-list1:
  IF stattype = 0 AND usrName = "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
 
  ELSE IF stattype = 1 AND usrName = "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr
              WHERE l-orderhdr.bestelldatum GE from-date AND
              l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK,
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK,
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK,
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
      ELSE
          FOR EACH l-orderhdr
              WHERE l-orderhdr.bestelldatum GE from-date AND
              l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1 NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK,
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK,
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK,
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
 
  ELSE IF stattype = 2 AND usrName = "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.

  ELSE IF stattype = 3 AND usrName = "" THEN 
      IF last-docu-nr NE "" THEN 
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.

  ELSE IF stattype = 0 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName 
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
 
  ELSE IF stattype = 1 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
 
  ELSE IF stattype = 2 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.

  ELSE IF stattype = 3 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.

END. 
 
PROCEDURE disp-list1a: 
    IF NUM-ENTRIES(last-docu-nr, ";") GT 1 THEN
    DO:
        ASSIGN
            temp-docu-nr = ENTRY(1, last-docu-nr, ";")
            temp-counter-nr = INT(ENTRY(2, last-docu-nr, ";")).
    END.

    IF stattype = 0 AND usrName = "" THEN
      IF last-docu-nr NE "" THEN
      DO:
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1 NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN create-temp-table-list.
                END.
                ELSE RUN create-temp-table-list.
          END.

          /*sis 020315*/
          FOR EACH q-list WHERE q-list.to-sort GT temp-counter-nr NO-LOCK:
              curr-counter = curr-counter + 1.
              temp-counter-nr = q-list.to-sort.
              
              IF curr-counter GE 25 THEN LEAVE.
              ELSE
              DO:
                  CREATE q2-list.
                  BUFFER-COPY q-list EXCEPT q-list.to-sort TO q2-list.
                  last-to-sort = q-list.to-sort. 
              END.
          END.
          IF sorttype = 2 THEN last-docu-nr1 = last-docu-nr1 + ";" + STRING(last-to-sort).
      END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
 
  ELSE IF stattype = 1 AND usrName = "" THEN
      IF last-docu-nr NE "" THEN
      DO:
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1 NO-LOCK,
              /*AND l-orderhdr.docu-nr GT last-docu-nr sis 020315*/
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN create-temp-table-list.
                END.
                ELSE RUN create-temp-table-list.
          END.


          /*sis 020315*/
          FOR EACH q-list WHERE q-list.to-sort GT temp-counter-nr NO-LOCK:
              curr-counter = curr-counter + 1.
              temp-counter-nr = q-list.to-sort.
              
              IF curr-counter GE 25 THEN LEAVE.
              ELSE
              DO:
                  CREATE q2-list.
                  BUFFER-COPY q-list EXCEPT q-list.to-sort TO q2-list.
                  last-to-sort = q-list.to-sort. 
              END.
          END.
          IF sorttype = 2 THEN last-docu-nr1 = last-docu-nr1 + ";" + STRING(last-to-sort).
      END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1 
              NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
 
  ELSE IF stattype = 2 AND usrName = "" THEN
      IF last-docu-nr NE "" THEN
      DO:
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 NO-LOCK,
              /*AND l-orderhdr.docu-nr GT last-docu-nr sis 020315*/
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN create-temp-table-list.
                END.
                ELSE RUN create-temp-table-list.
          END.

          /*sis 020315*/
          FOR EACH q-list WHERE q-list.to-sort GT temp-counter-nr NO-LOCK:
              curr-counter = curr-counter + 1.
              temp-counter-nr = q-list.to-sort.
              
              IF curr-counter GE 25 THEN LEAVE.
              ELSE
              DO:
                  CREATE q2-list.
                  BUFFER-COPY q-list EXCEPT q-list.to-sort TO q2-list.
                  last-to-sort = q-list.to-sort. 
              END.
          END.
          IF sorttype = 2 THEN last-docu-nr1 = last-docu-nr1 + ";" + STRING(last-to-sort).
      END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.

  ELSE IF stattype = 3 AND usrName = "" THEN
      IF last-docu-nr NE "" THEN
      DO:
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1 NO-LOCK,
              /*AND l-orderhdr.docu-nr GT last-docu-nr sis 020315*/
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN create-temp-table-list.
                END.
                ELSE RUN create-temp-table-list.

          END.

          /*sis 020315*/
          FOR EACH q-list WHERE q-list.to-sort GT temp-counter-nr NO-LOCK:
              curr-counter = curr-counter + 1.
              temp-counter-nr = q-list.to-sort.
              
              IF curr-counter GE 25 THEN LEAVE.
              ELSE
              DO:
                  CREATE q2-list.
                  BUFFER-COPY q-list EXCEPT q-list.to-sort TO q2-list.
                  last-to-sort = q-list.to-sort. 
              END.
          END.
          IF sorttype = 2 THEN last-docu-nr1 = last-docu-nr1 + ";" + STRING(last-to-sort).
      END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1 
              NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.

  ELSE IF stattype = 0 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
      DO:
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              /*AND l-orderhdr.docu-nr GT last-docu-nr*/ NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN create-temp-table-list.
                END.
                ELSE RUN create-temp-table-list.
          END.

          /*sis 020315*/
          FOR EACH q-list WHERE q-list.to-sort GT temp-counter-nr NO-LOCK:
              curr-counter = curr-counter + 1.
              temp-counter-nr = q-list.to-sort.
              
              IF curr-counter GE 25 THEN LEAVE.
              ELSE
              DO:
                  CREATE q2-list.
                  BUFFER-COPY q-list EXCEPT q-list.to-sort TO q2-list.
                  last-to-sort = q-list.to-sort. 
              END.
          END.
          IF sorttype = 2 THEN last-docu-nr1 = last-docu-nr1 + ";" + STRING(last-to-sort).
      END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
 
  ELSE IF stattype = 1 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
      DO:
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              /*AND l-orderhdr.docu-nr GT last-docu-nr*/ NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN create-temp-table-list.
                END.
                ELSE RUN create-temp-table-list.
          END.

          /*sis 020315*/
          FOR EACH q-list WHERE q-list.to-sort GT temp-counter-nr NO-LOCK:
              curr-counter = curr-counter + 1.
              temp-counter-nr = q-list.to-sort.
              
              IF curr-counter GE 25 THEN LEAVE.
              ELSE
              DO:
                  CREATE q2-list.
                  BUFFER-COPY q-list EXCEPT q-list.to-sort TO q2-list.
                  last-to-sort = q-list.to-sort. 
              END.
          END.
          IF sorttype = 2 THEN last-docu-nr1 = last-docu-nr1 + ";" + STRING(last-to-sort).
      END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
 
  ELSE IF stattype = 2 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
      DO:
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              /*AND l-orderhdr.docu-nr GT last-docu-nr*/ NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN create-temp-table-list.
                END.
                ELSE RUN create-temp-table-list.
          END.


          /*sis 020315*/
          FOR EACH q-list WHERE q-list.to-sort GT temp-counter-nr NO-LOCK:
              curr-counter = curr-counter + 1.
              temp-counter-nr = q-list.to-sort.
              
              IF curr-counter GE 25 THEN LEAVE.
              ELSE
              DO:
                  CREATE q2-list.
                  BUFFER-COPY q-list EXCEPT q-list.to-sort TO q2-list.
                  last-to-sort = q-list.to-sort. 
              END.
          END.
          IF sorttype = 2 THEN last-docu-nr1 = last-docu-nr1 + ";" + STRING(last-to-sort).
      END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.

  ELSE IF stattype = 3 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
      DO:
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              /*AND l-orderhdr.docu-nr GT last-docu-nr*/ NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN create-temp-table-list.
                END.
                ELSE RUN create-temp-table-list.
          END.


          /*sis 020315*/
          FOR EACH q-list WHERE q-list.to-sort GT temp-counter-nr NO-LOCK:
              curr-counter = curr-counter + 1.
              temp-counter-nr = q-list.to-sort.
              
              IF curr-counter GE 25 THEN LEAVE.
              ELSE
              DO:
                  CREATE q2-list.
                  BUFFER-COPY q-list EXCEPT q-list.to-sort TO q2-list.
                  last-to-sort = q-list.to-sort. 
              END.
          END.
          IF sorttype = 2 THEN last-docu-nr1 = last-docu-nr1 + ";" + STRING(last-to-sort).
      END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
END. 

PROCEDURE disp-list1b: 
  IF stattype = 0 AND usrName = "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
 
  ELSE IF stattype = 1 AND usrName = "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1 
              NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
 
  ELSE IF stattype = 2 AND usrName = "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.

  ELSE IF stattype = 3 AND usrName = "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.

  ELSE IF stattype = 0 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
  ELSE IF stattype = 1 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
  ELSE IF stattype = 2 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
  ELSE IF stattype = 3 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
END. 
 
PROCEDURE disp-list11: 
  
  IF stattype = 0 AND usrName = "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
 
  ELSE IF stattype = 1 AND usrName = "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1 
              NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
 
  ELSE IF stattype = 2 AND usrName = "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.

  ELSE IF stattype = 3 AND usrName = "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK,
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK,
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.

  ELSE IF stattype = 0 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
 
  ELSE IF stattype = 1 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
 
  ELSE IF stattype = 2 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.

  ELSE IF stattype = 3 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
END. 
 
PROCEDURE disp-list11a: 
    IF NUM-ENTRIES(last-docu-nr, ";") GT 1 THEN
    DO:
        ASSIGN
            temp-docu-nr = ENTRY(1, last-docu-nr, ";")
            temp-counter-nr = INT(ENTRY(2, last-docu-nr, ";")).
    END.

  IF stattype = 0 AND usrName = "" THEN
      IF last-docu-nr NE "" THEN
      DO:
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1
              /*AND l-orderhdr.docu-nr GT last-docu-nr*/ NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN create-temp-table-list.
                END.
                ELSE RUN create-temp-table-list.

          END.


          /*sis 020315*/
          FOR EACH q-list WHERE q-list.to-sort GT temp-counter-nr NO-LOCK:
              curr-counter = curr-counter + 1.
              temp-counter-nr = q-list.to-sort.

              IF curr-counter GE 25 THEN LEAVE.
              ELSE
              DO:
                  CREATE q2-list.
                  BUFFER-COPY q-list EXCEPT q-list.to-sort TO q2-list.
                  last-to-sort = q-list.to-sort. 
              END.
          END.
          IF sorttype = 2 THEN last-docu-nr1 = last-docu-nr1 + ";" + STRING(last-to-sort).
      END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
 
  ELSE IF stattype = 1 AND usrName = "" THEN
      IF last-docu-nr NE "" THEN
      DO:
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1
              /*AND l-orderhdr.docu-nr GT last-docu-nr*/ NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN create-temp-table-list.
                END.
                ELSE RUN create-temp-table-list.

          END.

          /*sis 020315*/
          FOR EACH q-list WHERE q-list.to-sort GT temp-counter-nr NO-LOCK:
              curr-counter = curr-counter + 1.
              temp-counter-nr = q-list.to-sort.

              IF curr-counter GE 25 THEN LEAVE.
              ELSE
              DO:
                  CREATE q2-list.
                  BUFFER-COPY q-list EXCEPT q-list.to-sort TO q2-list.
                  last-to-sort = q-list.to-sort. 
              END.
          END.
          IF sorttype = 2 THEN last-docu-nr1 = last-docu-nr1 + ";" + STRING(last-to-sort).
      END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1 
              NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
 
  ELSE IF stattype = 2 AND usrName = "" THEN
      IF last-docu-nr NE "" THEN
      DO:
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1
              /*AND l-orderhdr.docu-nr GT last-docu-nr*/ NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN create-temp-table-list.
                END.
                ELSE RUN create-temp-table-list.
          END.

          /*sis 020315*/
          FOR EACH q-list WHERE q-list.to-sort GT temp-counter-nr NO-LOCK:
              curr-counter = curr-counter + 1.
              temp-counter-nr = q-list.to-sort.

              IF curr-counter GE 25 THEN LEAVE.
              ELSE
              DO:
                  CREATE q2-list.
                  BUFFER-COPY q-list EXCEPT q-list.to-sort TO q2-list.
                  last-to-sort = q-list.to-sort. 
              END.
          END.
          IF sorttype = 2 THEN last-docu-nr1 = last-docu-nr1 + ";" + STRING(last-to-sort).
      END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.

  ELSE IF stattype = 3 AND usrName = "" THEN
      IF last-docu-nr NE "" THEN
      DO:   
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1 
              /*AND l-orderhdr.docu-nr GT last-docu-nr*/ NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN create-temp-table-list.
                END.
                ELSE RUN create-temp-table-list.
          END.

          /*sis 020315*/
          FOR EACH q-list WHERE q-list.to-sort GT temp-counter-nr NO-LOCK:
              curr-counter = curr-counter + 1.
              temp-counter-nr = q-list.to-sort.

              IF curr-counter GE 25 THEN LEAVE.
              ELSE
              DO:
                  CREATE q2-list.
                  BUFFER-COPY q-list EXCEPT q-list.to-sort TO q2-list.
                  last-to-sort = q-list.to-sort. 
              END.
          END.
          IF sorttype = 2 THEN last-docu-nr1 = last-docu-nr1 + ";" + STRING(last-to-sort).
      END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1 
              NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.

  ELSE IF stattype = 0 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
      DO:
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              /*AND l-orderhdr.docu-nr GT last-docu-nr*/ NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
               IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN create-temp-table-list.
                END.
                ELSE RUN create-temp-table-list.

          END.

          /*sis 020315*/
          FOR EACH q-list WHERE q-list.to-sort GT temp-counter-nr NO-LOCK:
              curr-counter = curr-counter + 1.
              temp-counter-nr = q-list.to-sort.

              IF curr-counter GE 25 THEN LEAVE.
              ELSE
              DO:
                  CREATE q2-list.
                  BUFFER-COPY q-list EXCEPT q-list.to-sort TO q2-list.
                  last-to-sort = q-list.to-sort. 
              END.
          END.
          IF sorttype = 2 THEN last-docu-nr1 = last-docu-nr1 + ";" + STRING(last-to-sort).
      END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
              IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
 
  ELSE IF stattype = 1 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
      DO:
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              /*AND l-orderhdr.docu-nr GT last-docu-nr*/ NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN create-temp-table-list.
                END.
                ELSE RUN create-temp-table-list.
          END.

          /*sis 020315*/
          FOR EACH q-list WHERE q-list.to-sort GT temp-counter-nr NO-LOCK:
              curr-counter = curr-counter + 1.
              temp-counter-nr = q-list.to-sort.

              IF curr-counter GE 25 THEN LEAVE.
              ELSE
              DO:
                  CREATE q2-list.
                  BUFFER-COPY q-list EXCEPT q-list.to-sort TO q2-list.
                  last-to-sort = q-list.to-sort. 
              END.
          END.
          IF sorttype = 2 THEN last-docu-nr1 = last-docu-nr1 + ";" + STRING(last-to-sort).
      END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
 
  ELSE IF stattype = 2 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
      DO:
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              /*AND l-orderhdr.docu-nr GT last-docu-nr*/ NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN create-temp-table-list.
                END.
                ELSE RUN create-temp-table-list.
          END.

          /*sis 020315*/
          FOR EACH q-list WHERE q-list.to-sort GT temp-counter-nr NO-LOCK:
              curr-counter = curr-counter + 1.
              temp-counter-nr = q-list.to-sort.

              IF curr-counter GE 25 THEN LEAVE.
              ELSE
              DO:
                  CREATE q2-list.
                  BUFFER-COPY q-list EXCEPT q-list.to-sort TO q2-list.
                  last-to-sort = q-list.to-sort. 
              END.
          END.
          IF sorttype = 2 THEN last-docu-nr1 = last-docu-nr1 + ";" + STRING(last-to-sort).
      END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.

  ELSE IF stattype = 3 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
      DO:
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              /*AND l-orderhdr.docu-nr GT last-docu-nr*/ NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN create-temp-table-list.
                END.
                ELSE RUN create-temp-table-list.

          END.

          /*sis 020315*/
          FOR EACH q-list WHERE q-list.to-sort GT temp-counter-nr NO-LOCK:
              curr-counter = curr-counter + 1.
              temp-counter-nr = q-list.to-sort.

              IF curr-counter GE 25 THEN LEAVE.
              ELSE
              DO:
                  CREATE q2-list.
                  BUFFER-COPY q-list EXCEPT q-list.to-sort TO q2-list.
                  last-to-sort = q-list.to-sort. 
              END.
          END.
          IF sorttype = 2 THEN last-docu-nr1 = last-docu-nr1 + ";" + STRING(last-to-sort).
      END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
               IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
END. 
 
PROCEDURE disp-list11b: 
  IF stattype = 0 AND usrName EQ "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                 IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
 
  ELSE IF stattype = 1 AND usrName EQ "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
 
  ELSE IF stattype = 2 AND usrName EQ "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.

  ELSE IF stattype = 3 AND usrName EQ "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.

  ELSE IF stattype = 0 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
 
  ELSE IF stattype = 1 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
 
  ELSE IF stattype = 2 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.

  ELSE IF stattype = 3 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date AND 
              l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
END. 

PROCEDURE disp-list2: 
  IF stattype = 0 AND usrName EQ "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
 
  ELSE IF stattype = 1 AND usrName EQ "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
 
  ELSE IF stattype = 2 AND usrName EQ "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.

  ELSE IF stattype = 3 AND usrName EQ "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.

  ELSE IF stattype = 0 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
 
  ELSE IF stattype = 1 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
 
  ELSE IF stattype = 2 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.

  ELSE IF stattype = 3 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
END. 
 
PROCEDURE disp-list2a: 
    IF NUM-ENTRIES(last-docu-nr, ";") GT 1 THEN
    DO:
        ASSIGN
            temp-docu-nr = ENTRY(1, last-docu-nr, ";")
            temp-counter-nr = INT(ENTRY(2, last-docu-nr, ";")).
    END.

  IF stattype = 0 AND usrName = "" THEN
      IF last-docu-nr NE "" THEN
      DO:
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1
              /*AND l-orderhdr.docu-nr GT last-docu-nr*/ NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN create-temp-table-list.
                END.
                ELSE RUN create-temp-table-list.

          END.

          /*sis 020315*/
          FOR EACH q-list WHERE q-list.to-sort GT temp-counter-nr NO-LOCK:
              curr-counter = curr-counter + 1.
              temp-counter-nr = q-list.to-sort.

              IF curr-counter GE 25 THEN LEAVE.
              ELSE
              DO:
                  CREATE q2-list.
                  BUFFER-COPY q-list EXCEPT q-list.to-sort TO q2-list.
                  last-to-sort = q-list.to-sort. 
              END.
          END.
          IF sorttype = 2 THEN last-docu-nr1 = last-docu-nr1 + ";" + STRING(last-to-sort).
      END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
               IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
 
  ELSE IF stattype = 1 AND usrName = "" THEN
      IF last-docu-nr NE "" THEN
      DO:
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1
             /* AND l-orderhdr.docu-nr GT last-docu-nr*/ NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN create-temp-table-list.
                END.
                ELSE RUN create-temp-table-list.
          END.

          /*sis 020315*/
          FOR EACH q-list WHERE q-list.to-sort GT temp-counter-nr NO-LOCK:
              curr-counter = curr-counter + 1.
              temp-counter-nr = q-list.to-sort.

              IF curr-counter GE 25 THEN LEAVE.
              ELSE
              DO:
                  CREATE q2-list.
                  BUFFER-COPY q-list EXCEPT q-list.to-sort TO q2-list.
                  last-to-sort = q-list.to-sort. 
              END.
          END.
          IF sorttype = 2 THEN last-docu-nr1 = last-docu-nr1 + ";" + STRING(last-to-sort).
      END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
 
  ELSE IF stattype = 2 AND usrName = "" THEN
      IF last-docu-nr NE "" THEN
      DO:
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1
              /*AND l-orderhdr.docu-nr GT last-docu-nr*/ NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN create-temp-table-list.
                END.
                ELSE RUN create-temp-table-list.

          END.

          /*sis 020315*/
          FOR EACH q-list WHERE q-list.to-sort GT temp-counter-nr NO-LOCK:
              curr-counter = curr-counter + 1.
              temp-counter-nr = q-list.to-sort.

              IF curr-counter GE 25 THEN LEAVE.
              ELSE
              DO:
                  CREATE q2-list.
                  BUFFER-COPY q-list EXCEPT q-list.to-sort TO q2-list.
                  last-to-sort = q-list.to-sort. 
              END.
          END.
          IF sorttype = 2 THEN last-docu-nr1 = last-docu-nr1 + ";" + STRING(last-to-sort).
      END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.

  ELSE IF stattype = 3 AND usrName = "" THEN
      IF last-docu-nr NE "" THEN
      DO:
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1
              /*AND l-orderhdr.docu-nr GT last-docu-nr*/ NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN create-temp-table-list.
                END.
                ELSE RUN create-temp-table-list.
          END.

          /*sis 020315*/
          FOR EACH q-list WHERE q-list.to-sort GT temp-counter-nr NO-LOCK:
              curr-counter = curr-counter + 1.
              temp-counter-nr = q-list.to-sort.

              IF curr-counter GE 25 THEN LEAVE.
              ELSE
              DO:
                  CREATE q2-list.
                  BUFFER-COPY q-list EXCEPT q-list.to-sort TO q2-list.
                  last-to-sort = q-list.to-sort. 
              END.
          END.
          IF sorttype = 2 THEN last-docu-nr1 = last-docu-nr1 + ";" + STRING(last-to-sort).
      END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.

  ELSE IF stattype = 0 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
      DO:
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              /*AND l-orderhdr.docu-nr GT last-docu-nr*/ NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN create-temp-table-list.
                END.
                ELSE RUN create-temp-table-list.

          END.

          /*sis 020315*/
          FOR EACH q-list WHERE q-list.to-sort GT temp-counter-nr NO-LOCK:
              curr-counter = curr-counter + 1.
              temp-counter-nr = q-list.to-sort.

              IF curr-counter GE 25 THEN LEAVE.
              ELSE
              DO:
                  CREATE q2-list.
                  BUFFER-COPY q-list EXCEPT q-list.to-sort TO q2-list.
                  last-to-sort = q-list.to-sort. 
              END.
          END.
          IF sorttype = 2 THEN last-docu-nr1 = last-docu-nr1 + ";" + STRING(last-to-sort).
      END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
 
  ELSE IF stattype = 1 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
      DO:
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              /*AND l-orderhdr.docu-nr GT last-docu-nr*/ NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN create-temp-table-list.
                END.
                ELSE RUN create-temp-table-list.
          END.

          /*sis 020315*/
          FOR EACH q-list WHERE q-list.to-sort GT temp-counter-nr NO-LOCK:
              curr-counter = curr-counter + 1.
              temp-counter-nr = q-list.to-sort.

              IF curr-counter GE 25 THEN LEAVE.
              ELSE
              DO:
                  CREATE q2-list.
                  BUFFER-COPY q-list EXCEPT q-list.to-sort TO q2-list.
                  last-to-sort = q-list.to-sort. 
              END.
          END.
          IF sorttype = 2 THEN last-docu-nr1 = last-docu-nr1 + ";" + STRING(last-to-sort).
      END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
 
  ELSE IF stattype = 2 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
      DO:
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              /*AND l-orderhdr.docu-nr GT last-docu-nr*/ NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN create-temp-table-list.
                END.
                ELSE RUN create-temp-table-list.
          END.

          /*sis 020315*/
          FOR EACH q-list WHERE q-list.to-sort GT temp-counter-nr NO-LOCK:
              curr-counter = curr-counter + 1.
              temp-counter-nr = q-list.to-sort.

              IF curr-counter GE 25 THEN LEAVE.
              ELSE
              DO:
                  CREATE q2-list.
                  BUFFER-COPY q-list EXCEPT q-list.to-sort TO q2-list.
                  last-to-sort = q-list.to-sort. 
              END.
          END.
          IF sorttype = 2 THEN last-docu-nr1 = last-docu-nr1 + ";" + STRING(last-to-sort).
      END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
               IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.

  ELSE IF stattype = 3 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
      DO:
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
             /* AND l-orderhdr.docu-nr GT last-docu-nr*/ NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN create-temp-table-list.
                END.
                ELSE RUN create-temp-table-list.
          END.

          /*sis 020315*/
          FOR EACH q-list WHERE q-list.to-sort GT temp-counter-nr NO-LOCK:
              curr-counter = curr-counter + 1.
              temp-counter-nr = q-list.to-sort.

              IF curr-counter GE 25 THEN LEAVE.
              ELSE
              DO:
                  CREATE q2-list.
                  BUFFER-COPY q-list EXCEPT q-list.to-sort TO q2-list.
                  last-to-sort = q-list.to-sort. 
              END.
          END.
          IF sorttype = 2 THEN last-docu-nr1 = last-docu-nr1 + ";" + STRING(last-to-sort).
      END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
               IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
END. 
 
PROCEDURE disp-list2b: 
  IF stattype = 0 AND usrName = "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
 
  ELSE IF stattype = 1 AND usrName = "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
 
  ELSE IF stattype = 2 AND usrName = "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.

  ELSE IF stattype = 3 AND usrName = "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.

  ELSE IF stattype = 0 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
 
  ELSE IF stattype = 1 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
 
  ELSE IF stattype = 2 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
               IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.

  ELSE IF stattype = 3 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.bestelldatum LE to-date AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
END. 
 
PROCEDURE disp-list22: 
  IF stattype = 0 AND usrName = "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
 
  ELSE IF stattype = 1 AND usrName = "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
 
  ELSE IF stattype = 2 AND usrName = "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.

  ELSE IF stattype = 3 AND usrName = "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.

  ELSE IF stattype = 0 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
 
  ELSE IF stattype = 1 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
 
  ELSE IF stattype = 2 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.

  ELSE IF stattype = 3 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr BY l-lieferant.firma:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
END. 
 
PROCEDURE disp-list22a: 

    IF NUM-ENTRIES(last-docu-nr, ";") GT 1 THEN
    DO:
        ASSIGN
            temp-docu-nr = ENTRY(1, last-docu-nr, ";")
            temp-counter-nr = INT(ENTRY(2, last-docu-nr, ";")).
    END.

  IF stattype = 0 AND usrName = "" THEN
      IF last-docu-nr NE "" THEN
      DO:
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1
              /*AND l-orderhdr.docu-nr GT last-docu-nr*/ NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN create-temp-table-list.
                END.
                ELSE RUN create-temp-table-list.
          END.

          /*sis 020315*/
          FOR EACH q-list WHERE q-list.to-sort GT temp-counter-nr NO-LOCK:
              curr-counter = curr-counter + 1.
              temp-counter-nr = q-list.to-sort.

              IF curr-counter GE 25 THEN LEAVE.
              ELSE
              DO:
                  CREATE q2-list.
                  BUFFER-COPY q-list EXCEPT q-list.to-sort TO q2-list.
                  last-to-sort = q-list.to-sort. 
              END.
          END.
          IF sorttype = 2 THEN last-docu-nr1 = last-docu-nr1 + ";" + STRING(last-to-sort).
      END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
 
  ELSE IF stattype = 1 AND usrName = "" THEN 
      IF last-docu-nr NE "" THEN
      DO:
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1
              /*AND l-orderhdr.docu-nr GT last-docu-nr*/ NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN create-temp-table-list.
                END.
                ELSE RUN create-temp-table-list.
          END.

          /*sis 020315*/
          FOR EACH q-list WHERE q-list.to-sort GT temp-counter-nr NO-LOCK:
              curr-counter = curr-counter + 1.
              temp-counter-nr = q-list.to-sort.

              IF curr-counter GE 25 THEN LEAVE.
              ELSE
              DO:
                  CREATE q2-list.
                  BUFFER-COPY q-list EXCEPT q-list.to-sort TO q2-list.
                  last-to-sort = q-list.to-sort. 
              END.
          END.
          IF sorttype = 2 THEN last-docu-nr1 = last-docu-nr1 + ";" + STRING(last-to-sort).
      END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
 
  ELSE IF stattype = 2 AND usrName = "" THEN
      IF last-docu-nr NE "" THEN
      DO:
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1
              /*AND l-orderhdr.docu-nr GT last-docu-nr */ NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN create-temp-table-list.
                END.
                ELSE RUN create-temp-table-list.
          END.

          /*sis 020315*/
          FOR EACH q-list WHERE q-list.to-sort GT temp-counter-nr NO-LOCK:
              curr-counter = curr-counter + 1.
              temp-counter-nr = q-list.to-sort.

              IF curr-counter GE 25 THEN LEAVE.
              ELSE
              DO:
                  CREATE q2-list.
                  BUFFER-COPY q-list EXCEPT q-list.to-sort TO q2-list.
                  last-to-sort = q-list.to-sort. 
              END.
          END.
          IF sorttype = 2 THEN last-docu-nr1 = last-docu-nr1 + ";" + STRING(last-to-sort).
      END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.

  ELSE IF stattype = 3 AND usrName = "" THEN
      IF last-docu-nr NE "" THEN
      DO:
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1
              /*AND l-orderhdr.docu-nr GT last-docu-nr*/ NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN create-temp-table-list.
                END.
                ELSE RUN create-temp-table-list.
          END.

          /*sis 020315*/
          FOR EACH q-list WHERE q-list.to-sort GT temp-counter-nr NO-LOCK:
              curr-counter = curr-counter + 1.
              temp-counter-nr = q-list.to-sort.

              IF curr-counter GE 25 THEN LEAVE.
              ELSE
              DO:
                  CREATE q2-list.
                  BUFFER-COPY q-list EXCEPT q-list.to-sort TO q2-list.
                  last-to-sort = q-list.to-sort. 
              END.
          END.
          IF sorttype = 2 THEN last-docu-nr1 = last-docu-nr1 + ";" + STRING(last-to-sort).
      END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.

  ELSE IF stattype = 0 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
      DO:
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
             /*AND l-orderhdr.docu-nr GT last-docu-nr*/ NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN create-temp-table-list.
                END.
                ELSE RUN create-temp-table-list.

          END.

          /*sis 020315*/
          FOR EACH q-list WHERE q-list.to-sort GT temp-counter-nr NO-LOCK:
              curr-counter = curr-counter + 1.
              temp-counter-nr = q-list.to-sort.

              IF curr-counter GE 25 THEN LEAVE.
              ELSE
              DO:
                  CREATE q2-list.
                  BUFFER-COPY q-list EXCEPT q-list.to-sort TO q2-list.
                  last-to-sort = q-list.to-sort. 
              END.
          END.
          IF sorttype = 2 THEN last-docu-nr1 = last-docu-nr1 + ";" + STRING(last-to-sort).
      END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
 
  ELSE IF stattype = 1 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
      DO:
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              /*AND l-orderhdr.docu-nr GT last-docu-nr*/ NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN create-temp-table-list.
                END.
                ELSE RUN create-temp-table-list.
          END.

          /*sis 020315*/
          FOR EACH q-list WHERE q-list.to-sort GT temp-counter-nr NO-LOCK:
              curr-counter = curr-counter + 1.
              temp-counter-nr = q-list.to-sort.

              IF curr-counter GE 25 THEN LEAVE.
              ELSE
              DO:
                  CREATE q2-list.
                  BUFFER-COPY q-list EXCEPT q-list.to-sort TO q2-list.
                  last-to-sort = q-list.to-sort. 
              END.
          END.
          IF sorttype = 2 THEN last-docu-nr1 = last-docu-nr1 + ";" + STRING(last-to-sort).
      END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
 
  ELSE IF stattype = 2 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
      DO:
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              /*AND l-orderhdr.docu-nr GT last-docu-nr*/ NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN create-temp-table-list.
                END.
                ELSE RUN create-temp-table-list.
          END.


          /*sis 020315*/
          FOR EACH q-list WHERE q-list.to-sort GT temp-counter-nr NO-LOCK:
              curr-counter = curr-counter + 1.
              temp-counter-nr = q-list.to-sort.

              IF curr-counter GE 25 THEN LEAVE.
              ELSE
              DO:
                  CREATE q2-list.
                  BUFFER-COPY q-list EXCEPT q-list.to-sort TO q2-list.
                  last-to-sort = q-list.to-sort. 
              END.
          END.
          IF sorttype = 2 THEN last-docu-nr1 = last-docu-nr1 + ";" + STRING(last-to-sort).
      END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.

          END.

  ELSE IF stattype = 3 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
      DO:
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              /*AND l-orderhdr.docu-nr GT last-docu-nr*/ NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN create-temp-table-list.
                END.
                ELSE RUN create-temp-table-list.

          END.

          /*sis 020315*/
          FOR EACH q-list WHERE q-list.to-sort GT temp-counter-nr NO-LOCK:
              curr-counter = curr-counter + 1.
              temp-counter-nr = q-list.to-sort.

              IF curr-counter GE 25 THEN LEAVE.
              ELSE
              DO:
                  CREATE q2-list.
                  BUFFER-COPY q-list EXCEPT q-list.to-sort TO q2-list.
                  last-to-sort = q-list.to-sort. 
              END.
          END.
          IF sorttype = 2 THEN last-docu-nr1 = last-docu-nr1 + ";" + STRING(last-to-sort).
      END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-lieferant.firma BY l-orderhdr.bestelldatum BY l-orderhdr.docu-nr:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
END. 

PROCEDURE disp-list22b: 
  IF stattype = 0 AND usrName = "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
 
  ELSE IF stattype = 1 AND usrName = "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
 
  ELSE IF stattype = 2 AND usrName = "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.

  ELSE IF stattype = 3 AND usrName = "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1 NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.

  ELSE IF stattype = 0 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum GE billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
 
  ELSE IF stattype = 1 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 1 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
 
  ELSE IF stattype = 2 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr 
              AND l-orderhdr.lieferdatum LT billdate AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag = 0 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.

  ELSE IF stattype = 3 AND usrName NE "" THEN
      IF last-docu-nr NE "" THEN
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName
              AND l-orderhdr.docu-nr GT last-docu-nr NO-LOCK,
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
      ELSE
          FOR EACH l-orderhdr 
              WHERE l-orderhdr.bestelldatum GE from-date 
              AND l-orderhdr.bestelldatum LE to-date 
              AND l-orderhdr.lief-nr = l-supp.lief-nr 
              AND l-orderhdr.angebot-lief[1] = deptnr AND l-orderhdr.betriebsnr LE 1 
              AND l-orderhdr.besteller = usrName NO-LOCK, 
              FIRST w-list WHERE w-list.nr = l-orderhdr.angebot-lief[3] NO-LOCK, 
              FIRST cost-list WHERE cost-list.nr = l-orderhdr.angebot-lief[1] NO-LOCK, 
              FIRST l-lieferant WHERE l-lieferant.lief-nr = l-orderhdr.lief-nr NO-LOCK, 
              FIRST l-order1 WHERE l-order1.docu-nr = l-orderhdr.docu-nr 
              AND l-order1.loeschflag EQ 2 AND l-order1.pos = 0  NO-LOCK 
              BY l-orderhdr.docu-nr BY l-lieferant.firma BY l-orderhdr.bestelldatum:
                 IF dml-only THEN DO:
                     IF l-order1.lief-fax[1] MATCHES "D*" AND l-order1.lief-fax[3] = "DML" THEN
                         RUN cr-temp-table.
                END.
                ELSE RUN cr-temp-table.
          END.
END.


PROCEDURE create-costlist: 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE m AS INTEGER INITIAL 1. 
DEFINE VARIABLE n AS INTEGER INITIAL 0. 
  FOR EACH parameters WHERE progname = "CostCenter" 
    AND section = "Name" AND varname GT "" NO-LOCK: 
    create cost-list. 
    cost-list.nr = INTEGER(parameters.varname). 
    cost-list.bezeich = parameters.vstring. 
  END. 
END. 

PROCEDURE currency-list: 
DEFINE VARIABLE local-nr AS INTEGER INITIAL 0. 
  FIND FIRST htparam WHERE htparam.paramnr = 152 NO-LOCK. 
  FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR. 
  IF AVAILABLE waehrung THEN local-nr = waehrung.waehrungsnr. 
 
  create w-list. 
  IF local-nr NE 0 THEN w-list.wabkurz = waehrung.wabkurz. 
 
  FOR EACH waehrung NO-LOCK BY waehrung.wabkurz: 
    create w-list. 
    w-list.nr = waehrung.waehrungsnr. 
    w-list.wabkurz = waehrung.wabkurz. 
  END. 
END. 

PROCEDURE cr-temp-table:
    DEFINE VARIABLE t-amount AS DECIMAL.
    ASSIGN app-lvl = 0.
    FIND FIRST queasy WHERE queasy.KEY EQ 245 AND queasy.char1 EQ l-orderhdr.docu-nr NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE queasy:
        ASSIGN app-lvl = queasy.number1.
        FIND NEXT queasy WHERE queasy.KEY EQ 245 AND queasy.char1 EQ l-orderhdr.docu-nr NO-LOCK NO-ERROR.
    END.
    IF app-sort EQ "ALL" THEN
    DO:
        IF counter = 1 THEN first-docu-nr = l-orderhdr.docu-nr.
        IF (counter GE 25) AND (curr-docu-nr NE l-orderhdr.docu-nr) THEN LEAVE.
        IF (counter GE 25) AND (last-docu-nr1 NE l-orderhdr.docu-nr) THEN LEAVE.
        
        /*MTCREATE t-l-orderhdr.
        BUFFER-COPY l-orderhdr TO t-l-orderhdr.*/
        CREATE q2-list.
        ASSIGN
            q2-list.bestelldatum            = l-orderhdr.bestelldatum
            q2-list.bezeich                 = cost-list.bezeich
            q2-list.firma                   = l-lieferant.firma
            q2-list.docu-nr                 = l-orderhdr.docu-nr
            q2-list.l-orderhdr-lieferdatum  = l-orderhdr.lieferdatum
            q2-list.wabkurz                 = w-list.wabkurz
            q2-list.bestellart              = l-orderhdr.bestellart
            q2-list.gedruckt                = l-orderhdr.gedruckt
            q2-list.l-orderhdr-besteller    = l-orderhdr.besteller
            q2-list.l-order-gedruckt        = l-order1.gedruckt
            q2-list.zeit                    = l-order1.zeit
            q2-list.lief-fax-2              = l-order1.lief-fax[2]
            q2-list.l-order-lieferdatum     = l-order1.lieferdatum
            q2-list.lief-fax-3              = l-order1.lief-fax[3]
            q2-list.lieferdatum-eff         = l-order1.lieferdatum-eff
            q2-list.lief-fax-1              = l-order1.lief-fax[1]
            q2-list.lief-nr                 = l-order1.lief-nr.
            last-docu-nr1                   = l-orderhdr.docu-nr.
        /*Naufal - if param 71 yes then fill from queasy 245*/
        IF p-71 THEN
        DO:
            FIND FIRST queasy WHERE queasy.KEY EQ 245 AND queasy.char1 EQ l-orderhdr.docu-nr NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
            DO:
                FIND FIRST q245 WHERE q245.KEY EQ 245 AND q245.char1 EQ l-orderhdr.docu-nr NO-LOCK NO-ERROR.
                DO WHILE AVAILABLE q245:
                    IF q2-list.username NE "" THEN
                    DO:
                        IF NUM-ENTRIES(q2-list.username,";") LT 4 THEN
                            q2-list.username = q2-list.username + ENTRY(1,q245.char3,"|") + ";".
                        ELSE
                            q2-list.username = q2-list.username + ENTRY(1,q245.char3,"|").
                    END.
                    ELSE
                    DO:
                        q2-list.username = ENTRY(1,q245.char3,"|") + ";".
                    END.
                    FIND NEXT q245 WHERE q245.KEY EQ 245 AND q245.char1 EQ l-orderhdr.docu-nr NO-LOCK NO-ERROR.
                END.
                DO loop = 1 TO 4:
                    IF NUM-ENTRIES(q2-list.username,";") NE 4 THEN
                    DO:
                        q2-list.username = q2-list.username + ";".
                    END.
                END.
            END.
            ELSE
            DO:
                /*Naufal - add look for user that release po on queasy*/
                FIND FIRST queasy WHERE queasy.KEY = 214 AND queasy.char1 = STRING(RECID(l-orderhdr)) NO-LOCK NO-ERROR.
                IF AVAILABLE queasy THEN
                DO:
                    q2-list.username            = queasy.char3.
                END.
                ELSE 
                DO:
                    q2-list.username            = "".
                END.
            END.
        END.
        ELSE
        DO:
            /*Naufal - add look for user that release po on queasy*/
            FIND FIRST queasy WHERE queasy.KEY = 214 AND queasy.char1 = STRING(RECID(l-orderhdr)) NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
            DO:
                q2-list.username            = queasy.char3.
            END.
            ELSE 
            DO:
                q2-list.username            = "".
            END.
        END.
        FIND FIRST l-order2 WHERE l-order2.docu-nr = l-orderhdr.docu-nr AND l-order2.pos GT 0 
            AND l-order2.loeschflag = 0 NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE l-order2:
            FIND FIRST l-art WHERE l-art.artnr = l-order2.artnr NO-LOCK NO-ERROR.
            IF AVAILABLE l-art THEN 
            DO:
                t-amount = t-amount + l-order2.warenwert.
            END.
            FIND NEXT l-order2 WHERE l-order2.docu-nr = l-orderhdr.docu-nr AND l-order2.pos GT 0 
                AND l-order2.loeschflag = 0 NO-LOCK NO-ERROR.
        END.
        ASSIGN
            q2-list.tot-amount = t-amount.
        IF sorttype = 2 THEN last-docu-nr1 =  last-docu-nr1 + ";" + STRING(counter).
    END.
    ELSE IF app-sort EQ "Approve 1" THEN
    DO:
        FIND FIRST queasy WHERE queasy.KEY EQ 214 AND queasy.char1 = STRING(RECID(l-orderhdr)) NO-LOCK NO-ERROR.
        IF NOT AVAILABLE queasy THEN
        DO:
            FIND FIRST queasy WHERE queasy.KEY EQ 245 AND queasy.char1 EQ l-orderhdr.docu-nr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE queasy THEN
            DO:
                IF counter = 1 THEN first-docu-nr = l-orderhdr.docu-nr.
                IF (counter GE 25) AND (curr-docu-nr NE l-orderhdr.docu-nr) THEN LEAVE.
                IF (counter GE 25) AND (last-docu-nr1 NE l-orderhdr.docu-nr) THEN LEAVE.
                
                /*MTCREATE t-l-orderhdr.
                BUFFER-COPY l-orderhdr TO t-l-orderhdr.*/
                CREATE q2-list.
                ASSIGN
                    q2-list.bestelldatum            = l-orderhdr.bestelldatum
                    q2-list.bezeich                 = cost-list.bezeich
                    q2-list.firma                   = l-lieferant.firma
                    q2-list.docu-nr                 = l-orderhdr.docu-nr
                    q2-list.l-orderhdr-lieferdatum  = l-orderhdr.lieferdatum
                    q2-list.wabkurz                 = w-list.wabkurz
                    q2-list.bestellart              = l-orderhdr.bestellart
                    q2-list.gedruckt                = l-orderhdr.gedruckt
                    q2-list.l-orderhdr-besteller    = l-orderhdr.besteller
                    q2-list.l-order-gedruckt        = l-order1.gedruckt
                    q2-list.zeit                    = l-order1.zeit
                    q2-list.lief-fax-2              = l-order1.lief-fax[2]
                    q2-list.l-order-lieferdatum     = l-order1.lieferdatum
                    q2-list.lief-fax-3              = l-order1.lief-fax[3]
                    q2-list.lieferdatum-eff         = l-order1.lieferdatum-eff
                    q2-list.lief-fax-1              = l-order1.lief-fax[1]
                    q2-list.lief-nr                 = l-order1.lief-nr.
                    last-docu-nr1                   = l-orderhdr.docu-nr.
                /*Naufal - if param 71 yes then fill from queasy 245*/
                IF p-71 THEN
                DO:
                    /*Naufal - add look for user that release po on queasy*/
                    FIND FIRST queasy WHERE queasy.KEY = 214 AND queasy.char1 = STRING(RECID(l-orderhdr)) NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN
                    DO:
                        q2-list.username            = queasy.char3.
                    END.
                    ELSE 
                    DO:
                        q2-list.username            = "".
                    END.
                END.
                ELSE
                DO:
                    /*Naufal - add look for user that release po on queasy*/
                    FIND FIRST queasy WHERE queasy.KEY = 214 AND queasy.char1 = STRING(RECID(l-orderhdr)) NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN
                    DO:
                        q2-list.username            = queasy.char3.
                    END.
                    ELSE 
                    DO:
                        q2-list.username            = "".
                    END.
                END.
                FIND FIRST l-order2 WHERE l-order2.docu-nr = l-orderhdr.docu-nr AND l-order2.pos GT 0 
                    AND l-order2.loeschflag = 0 NO-LOCK NO-ERROR.
                DO WHILE AVAILABLE l-order2:
                    FIND FIRST l-art WHERE l-art.artnr = l-order2.artnr NO-LOCK NO-ERROR.
                    IF AVAILABLE l-art THEN 
                    DO:
                        t-amount = t-amount + l-order2.warenwert.
                    END.
                    FIND NEXT l-order2 WHERE l-order2.docu-nr = l-orderhdr.docu-nr AND l-order2.pos GT 0 
                        AND l-order2.loeschflag = 0 NO-LOCK NO-ERROR.
                END.
                ASSIGN
                    q2-list.tot-amount = t-amount.
                IF sorttype = 2 THEN last-docu-nr1 =  last-docu-nr1 + ";" + STRING(counter).
            END.
        END.
    END.
    ELSE
    DO:
        IF app-lvl EQ approval THEN
        DO:
            IF counter = 1 THEN first-docu-nr = l-orderhdr.docu-nr.
            IF (counter GE 25) AND (curr-docu-nr NE l-orderhdr.docu-nr) THEN LEAVE.
            IF (counter GE 25) AND (last-docu-nr1 NE l-orderhdr.docu-nr) THEN LEAVE.
            
            /*MTCREATE t-l-orderhdr.
            BUFFER-COPY l-orderhdr TO t-l-orderhdr.*/
            CREATE q2-list.
            ASSIGN
                q2-list.bestelldatum            = l-orderhdr.bestelldatum
                q2-list.bezeich                 = cost-list.bezeich
                q2-list.firma                   = l-lieferant.firma
                q2-list.docu-nr                 = l-orderhdr.docu-nr
                q2-list.l-orderhdr-lieferdatum  = l-orderhdr.lieferdatum
                q2-list.wabkurz                 = w-list.wabkurz
                q2-list.bestellart              = l-orderhdr.bestellart
                q2-list.gedruckt                = l-orderhdr.gedruckt
                q2-list.l-orderhdr-besteller    = l-orderhdr.besteller
                q2-list.l-order-gedruckt        = l-order1.gedruckt
                q2-list.zeit                    = l-order1.zeit
                q2-list.lief-fax-2              = l-order1.lief-fax[2]
                q2-list.l-order-lieferdatum     = l-order1.lieferdatum
                q2-list.lief-fax-3              = l-order1.lief-fax[3]
                q2-list.lieferdatum-eff         = l-order1.lieferdatum-eff
                q2-list.lief-fax-1              = l-order1.lief-fax[1]
                q2-list.lief-nr                 = l-order1.lief-nr.
                last-docu-nr1                   = l-orderhdr.docu-nr.
            /*Naufal - if param 71 yes then fill from queasy 245*/
            IF p-71 THEN
            DO:
                FIND FIRST queasy WHERE queasy.KEY EQ 245 AND queasy.char1 EQ l-orderhdr.docu-nr NO-LOCK NO-ERROR.
                IF AVAILABLE queasy THEN
                DO:
                    FIND FIRST q245 WHERE q245.KEY EQ 245 AND q245.char1 EQ l-orderhdr.docu-nr NO-LOCK NO-ERROR.
                    DO WHILE AVAILABLE q245:
                        IF q2-list.username NE "" THEN
                        DO:
                            IF NUM-ENTRIES(q2-list.username,";") LT 4 THEN
                                q2-list.username = q2-list.username + ENTRY(1,q245.char3,"|") + ";".
                            ELSE
                                q2-list.username = q2-list.username + ENTRY(1,q245.char3,"|").
                        END.
                        ELSE
                        DO:
                            q2-list.username = ENTRY(1,q245.char3,"|") + ";".
                        END.
                        FIND NEXT q245 WHERE q245.KEY EQ 245 AND q245.char1 EQ l-orderhdr.docu-nr NO-LOCK NO-ERROR.
                    END.
                    DO loop = 1 TO 4:
                        IF NUM-ENTRIES(q2-list.username,";") NE 4 THEN
                        DO:
                            q2-list.username = q2-list.username + ";".
                        END.
                    END.
                END.
                ELSE
                DO:
                    /*Naufal - add look for user that release po on queasy*/
                    FIND FIRST queasy WHERE queasy.KEY = 214 AND queasy.char1 = STRING(RECID(l-orderhdr)) NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN
                    DO:
                        q2-list.username            = queasy.char3.
                    END.
                    ELSE 
                    DO:
                        q2-list.username            = "".
                    END.
                END.
            END.
	        ELSE
            DO:
                /*Naufal - add look for user that release po on queasy*/
                FIND FIRST queasy WHERE queasy.KEY = 214 AND queasy.char1 = STRING(RECID(l-orderhdr)) NO-LOCK NO-ERROR.
                IF AVAILABLE queasy THEN
                DO:
                    q2-list.username            = queasy.char3.
                END.
                ELSE 
                DO:
                    q2-list.username            = "".
                END.
            END.
            FIND FIRST l-order2 WHERE l-order2.docu-nr = l-orderhdr.docu-nr AND l-order2.pos GT 0 
                AND l-order2.loeschflag = 0 NO-LOCK NO-ERROR.
            DO WHILE AVAILABLE l-order2:
                FIND FIRST l-art WHERE l-art.artnr = l-order2.artnr NO-LOCK NO-ERROR.
                IF AVAILABLE l-art THEN 
                DO:
                    t-amount = t-amount + l-order2.warenwert.
                END.
                FIND NEXT l-order2 WHERE l-order2.docu-nr = l-orderhdr.docu-nr AND l-order2.pos GT 0 
                    AND l-order2.loeschflag = 0 NO-LOCK NO-ERROR.
            END.
            ASSIGN
                q2-list.tot-amount = t-amount.
            IF sorttype = 2 THEN last-docu-nr1 =  last-docu-nr1 + ";" + STRING(counter).
        END.
    END.
END.


PROCEDURE create-temp-table-list:
    DEFINE VARIABLE t-amount AS DECIMAL.
    ASSIGN app-lvl = 0.
    FIND FIRST queasy WHERE queasy.KEY EQ 245 AND queasy.char1 EQ l-orderhdr.docu-nr NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE queasy:
        ASSIGN app-lvl = queasy.number1.
        FIND NEXT queasy WHERE queasy.KEY EQ 245 AND queasy.char1 EQ l-orderhdr.docu-nr NO-LOCK NO-ERROR.
    END.
    IF app-sort EQ "ALL" THEN
    DO:
        counter = counter + 1.
        CREATE q-list.
        ASSIGN
            q-list.bestelldatum             = l-orderhdr.bestelldatum
            q-list.bezeich                  = cost-list.bezeich
            q-list.firma                    = l-lieferant.firma
            q-list.docu-nr                  = l-orderhdr.docu-nr
            q-list.l-orderhdr-lieferdatum   = l-orderhdr.lieferdatum
            q-list.wabkurz                  = w-list.wabkurz
            q-list.bestellart               = l-orderhdr.bestellart
            q-list.gedruckt                 = l-orderhdr.gedruckt
            q-list.l-orderhdr-besteller     = l-orderhdr.besteller
            q-list.l-order-gedruckt         = l-order1.gedruckt
            q-list.zeit                     = l-order1.zeit
            q-list.lief-fax-2               = l-order1.lief-fax[2]
            q-list.l-order-lieferdatum      = l-order1.lieferdatum
            q-list.lief-fax-3               = l-order1.lief-fax[3]
            q-list.lieferdatum-eff          = l-order1.lieferdatum-eff
            q-list.lief-fax-1               = l-order1.lief-fax[1]
            q-list.lief-nr                  = l-order1.lief-nr
            q-list.to-sort                  = counter.
        IF sorttype = 2 THEN last-docu-nr1 = l-orderhdr.docu-nr.
        /*Naufal - if param 71 yes then fill from queasy 245*/
        IF p-71 THEN
        DO:
            FIND FIRST queasy WHERE queasy.KEY EQ 245 AND queasy.char1 EQ l-orderhdr.docu-nr NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
            DO:
                FIND FIRST q245 WHERE q245.KEY EQ 245 AND q245.char1 EQ l-orderhdr.docu-nr NO-LOCK NO-ERROR.
                DO WHILE AVAILABLE q245:
                    IF q-list.username NE "" THEN
                    DO:
                        IF NUM-ENTRIES(q-list.username,";") LT 4 THEN
                            q-list.username = q-list.username + ENTRY(1,q245.char3,"|") + ";".
                        ELSE
                            q-list.username = q-list.username + ENTRY(1,q245.char3,"|").
                    END.
                    ELSE
                    DO:
                        q-list.username = ENTRY(1,q245.char3,"|") + ";".
                    END.
                    FIND NEXT q245 WHERE q245.KEY EQ 245 AND q245.char1 EQ l-orderhdr.docu-nr NO-LOCK NO-ERROR.
                END.
                DO loop = 1 TO 4:
                    IF NUM-ENTRIES(q-list.username,";") NE 4 THEN
                    DO:
                        q-list.username = q-list.username + ";".
                    END.
                END.
            END.
            ELSE
            DO:
                /*Naufal - add look for user that release po on queasy*/
                FIND FIRST queasy WHERE queasy.KEY = 214 AND queasy.char1 = STRING(RECID(l-orderhdr)) NO-LOCK NO-ERROR.
                IF AVAILABLE queasy THEN
                DO:
                    q-list.username            = queasy.char3.
                END.
                ELSE 
                DO:
                    q-list.username            = "".
                END.
            END.
        END.
	    ELSE
        DO:
            /*Naufal - add look for user that release po on queasy 214*/
            FIND FIRST queasy WHERE queasy.KEY = 214 AND queasy.char1 = STRING(RECID(l-orderhdr)) NO-LOCK NO-ERROR.
            IF AVAILABLE queasy THEN
            DO:
                q-list.username            = queasy.char3.
            END.
            ELSE 
            DO:
                q-list.username            = "".
            END.
        END.
        FIND FIRST l-order2 WHERE l-order2.docu-nr = l-orderhdr.docu-nr AND l-order2.pos GT 0 
            AND l-order2.loeschflag = 0 NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE l-order2:
            FIND FIRST l-art WHERE l-art.artnr = l-order2.artnr NO-LOCK NO-ERROR.
            IF AVAILABLE l-art THEN 
            DO:
                t-amount = t-amount + l-order2.warenwert.
            END.
            FIND NEXT l-order2 WHERE l-order2.docu-nr = l-orderhdr.docu-nr AND l-order2.pos GT 0 
                AND l-order2.loeschflag = 0 NO-LOCK NO-ERROR.
        END.
        ASSIGN
            q-list.tot-amount = t-amount.
    END.
    ELSE IF app-sort EQ "Approve 1" THEN
    DO:
        FIND FIRST queasy WHERE queasy.KEY = 214 AND queasy.char1 = STRING(RECID(l-orderhdr)) NO-LOCK NO-ERROR.
        IF NOT AVAILABLE queasy THEN
        DO:
            FIND FIRST queasy WHERE queasy.KEY EQ 245 AND queasy.char1 EQ l-orderhdr.docu-nr NO-LOCK NO-ERROR.
            IF NOT AVAILABLE queasy THEN
            DO:
                counter = counter + 1.
                CREATE q-list.
                ASSIGN
                    q-list.bestelldatum             = l-orderhdr.bestelldatum
                    q-list.bezeich                  = cost-list.bezeich
                    q-list.firma                    = l-lieferant.firma
                    q-list.docu-nr                  = l-orderhdr.docu-nr
                    q-list.l-orderhdr-lieferdatum   = l-orderhdr.lieferdatum
                    q-list.wabkurz                  = w-list.wabkurz
                    q-list.bestellart               = l-orderhdr.bestellart
                    q-list.gedruckt                 = l-orderhdr.gedruckt
                    q-list.l-orderhdr-besteller     = l-orderhdr.besteller
                    q-list.l-order-gedruckt         = l-order1.gedruckt
                    q-list.zeit                     = l-order1.zeit
                    q-list.lief-fax-2               = l-order1.lief-fax[2]
                    q-list.l-order-lieferdatum      = l-order1.lieferdatum
                    q-list.lief-fax-3               = l-order1.lief-fax[3]
                    q-list.lieferdatum-eff          = l-order1.lieferdatum-eff
                    q-list.lief-fax-1               = l-order1.lief-fax[1]
                    q-list.lief-nr                  = l-order1.lief-nr
                    q-list.to-sort                  = counter.
                IF sorttype = 2 THEN last-docu-nr1 = l-orderhdr.docu-nr.
                /*Naufal - if param 71 yes then fill from queasy 245*/
                IF p-71 THEN
                DO:
                    /*Naufal - add look for user that release po on queasy*/
                    FIND FIRST queasy WHERE queasy.KEY = 214 AND queasy.char1 = STRING(RECID(l-orderhdr)) NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN
                    DO:
                        q-list.username            = queasy.char3.
                    END.
                    ELSE 
                    DO:
                        q-list.username            = "".
                    END.
                END.
	            ELSE
                DO:
                    /*Naufal - add look for user that release po on queasy 214*/
                    FIND FIRST queasy WHERE queasy.KEY = 214 AND queasy.char1 = STRING(RECID(l-orderhdr)) NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN
                    DO:
                        q-list.username = queasy.char3.
                    END.
                    ELSE 
                    DO:
                        q-list.username = "".
                    END.
                END.
                FIND FIRST l-order2 WHERE l-order2.docu-nr = l-orderhdr.docu-nr AND l-order2.pos GT 0 
                    AND l-order2.loeschflag = 0 NO-LOCK NO-ERROR.
                DO WHILE AVAILABLE l-order2:
                    FIND FIRST l-art WHERE l-art.artnr = l-order2.artnr NO-LOCK NO-ERROR.
                    IF AVAILABLE l-art THEN 
                    DO:
                        t-amount = t-amount + l-order2.warenwert.
                    END.
                    FIND NEXT l-order2 WHERE l-order2.docu-nr = l-orderhdr.docu-nr AND l-order2.pos GT 0 
                        AND l-order2.loeschflag = 0 NO-LOCK NO-ERROR.
                END.
                ASSIGN
                    q-list.tot-amount = t-amount.
            END.
        END.     
    END.
    ELSE
    DO:
        IF app-lvl EQ approval THEN
        DO:
            counter = counter + 1.
            CREATE q-list.
            ASSIGN
                q-list.bestelldatum             = l-orderhdr.bestelldatum
                q-list.bezeich                  = cost-list.bezeich
                q-list.firma                    = l-lieferant.firma
                q-list.docu-nr                  = l-orderhdr.docu-nr
                q-list.l-orderhdr-lieferdatum   = l-orderhdr.lieferdatum
                q-list.wabkurz                  = w-list.wabkurz
                q-list.bestellart               = l-orderhdr.bestellart
                q-list.gedruckt                 = l-orderhdr.gedruckt
                q-list.l-orderhdr-besteller     = l-orderhdr.besteller
                q-list.l-order-gedruckt         = l-order1.gedruckt
                q-list.zeit                     = l-order1.zeit
                q-list.lief-fax-2               = l-order1.lief-fax[2]
                q-list.l-order-lieferdatum      = l-order1.lieferdatum
                q-list.lief-fax-3               = l-order1.lief-fax[3]
                q-list.lieferdatum-eff          = l-order1.lieferdatum-eff
                q-list.lief-fax-1               = l-order1.lief-fax[1]
                q-list.lief-nr                  = l-order1.lief-nr
                q-list.to-sort                  = counter.
            IF sorttype = 2 THEN last-docu-nr1 = l-orderhdr.docu-nr.
            /*Naufal - if param 71 yes then fill from queasy 245*/
            IF p-71 THEN
            DO:
                FIND FIRST queasy WHERE queasy.KEY EQ 245 AND queasy.char1 EQ l-orderhdr.docu-nr NO-LOCK NO-ERROR.
                IF AVAILABLE queasy THEN
                DO:
                    FIND FIRST q245 WHERE q245.KEY EQ 245 AND q245.char1 EQ l-orderhdr.docu-nr NO-LOCK NO-ERROR.
                    DO WHILE AVAILABLE q245:
                        IF q-list.username NE "" THEN
                        DO:
                            IF NUM-ENTRIES(q-list.username,";") LT 4 THEN
                                q-list.username = q-list.username + ENTRY(1,q245.char3,"|") + ";".
                            ELSE
                                q-list.username = q-list.username + ENTRY(1,q245.char3,"|").
                        END.
                        ELSE
                        DO:
                            q-list.username = ENTRY(1,q245.char3,"|") + ";".
                        END.
                        FIND NEXT q245 WHERE q245.KEY EQ 245 AND q245.char1 EQ l-orderhdr.docu-nr NO-LOCK NO-ERROR.
                    END.
                    DO loop = 1 TO 4:
                        IF NUM-ENTRIES(q-list.username,";") NE 4 THEN
                        DO:
                            q-list.username = q-list.username + ";".
                        END.
                    END.
                END.
                ELSE
                DO:
                    /*Naufal - add look for user that release po on queasy*/
                    FIND FIRST queasy WHERE queasy.KEY = 214 AND queasy.char1 = STRING(RECID(l-orderhdr)) NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN
                    DO:
                        q-list.username            = queasy.char3.
                    END.
                    ELSE 
                    DO:
                        q-list.username            = "".
                    END.
                END.
            END.
	        ELSE
            DO:
                /*Naufal - add look for user that release po on queasy 214*/
                FIND FIRST queasy WHERE queasy.KEY = 214 AND queasy.char1 = STRING(RECID(l-orderhdr)) NO-LOCK NO-ERROR.
                IF AVAILABLE queasy THEN
                DO:
                    q-list.username            = queasy.char3.
                END.
                ELSE 
                DO:
                    q-list.username            = "".
                END.
            END.
            FIND FIRST l-order2 WHERE l-order2.docu-nr = l-orderhdr.docu-nr AND l-order2.pos GT 0 
                AND l-order2.loeschflag = 0 NO-LOCK NO-ERROR.
            DO WHILE AVAILABLE l-order2:
                FIND FIRST l-art WHERE l-art.artnr = l-order2.artnr NO-LOCK NO-ERROR.
                IF AVAILABLE l-art THEN 
                DO:
                    t-amount = t-amount + l-order2.warenwert.
                END.
                FIND NEXT l-order2 WHERE l-order2.docu-nr = l-orderhdr.docu-nr AND l-order2.pos GT 0 
                    AND l-order2.loeschflag = 0 NO-LOCK NO-ERROR.
            END.
            ASSIGN
                q-list.tot-amount = t-amount.
        END.
    END.
END.
