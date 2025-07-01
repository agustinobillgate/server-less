
DEF TEMP-TABLE t-l-lager
    FIELD lager-nr   LIKE l-lager.lager-nr
    FIELD bezeich    LIKE l-lager.bezeich
    FIELD betriebsnr LIKE l-lager.betriebsnr.

DEF TEMP-TABLE t-hoteldpt
    FIELD num       LIKE hoteldpt.num
    FIELD depart    LIKE hoteldpt.depart.

DEF OUTPUT PARAMETER TABLE FOR t-l-lager.
DEF OUTPUT PARAMETER TABLE FOR t-hoteldpt.

FOR EACH l-lager:
    CREATE t-l-lager.
    ASSIGN
      t-l-lager.lager-nr   = l-lager.lager-nr
      t-l-lager.bezeich    = l-lager.bezeich
      t-l-lager.betriebsnr = l-lager.betriebsnr.
END.


FOR EACH hoteldpt:
    CREATE t-hoteldpt.
    ASSIGN
    t-hoteldpt.num       = hoteldpt.num
    t-hoteldpt.depart    = hoteldpt.depart.
END.
