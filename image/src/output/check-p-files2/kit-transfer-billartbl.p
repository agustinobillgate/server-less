
DEF INPUT PARAMETER billart AS INT.
DEF INPUT PARAMETER curr-dept AS INT.
DEF OUTPUT PARAMETER t-bezeich AS CHAR.
DEF OUTPUT PARAMETER avail-hartikel AS LOGICAL INIT NO.

find first h-artikel where h-artikel.artnr = billart
  and h-artikel.departement = curr-dept and h-artikel.activeflag
  and h-artikel.artart = 0 no-lock no-error.
if available h-artikel then
do:
  t-bezeich = h-artikel.bezeich.
  avail-hartikel = YES.
  /*MTmenu-bez = h-artikel.bezeich.
  description = h-artikel.bezeich.
  qty = 1.
  run get-price.
  enable billart qty with frame frame1.
  apply "entry" to qty.       
  disp qty description price menu-bez with frame frame1.*/
  return no-apply.
end.
/*MTelse 
do:
  run clear-bill-entry.
  apply "entry" to billart.
  return no-apply.
end.*/
