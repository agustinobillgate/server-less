from functions.additional_functions import *
from decimal import Decimal
from datetime import datetime
from models import Genstat, Guest, Nation, Htparam, Arrangement, Artikel
from functions.calc_servtaxesbl import calc_servtaxesbl
from sqlalchemy import text

def ta_nationstat_go_listbl(from_date: str, last_period: str, sorttype: int, text2: str, text3: str):
    # Initialize variables for subtotals and grand totals
    sub_mrm, sub_mlod, sub_margt, sub_yrm, sub_ylod, sub_yargt = 0, Decimal('0.0'), Decimal('0.0'), 0, Decimal('0.0'), Decimal('0.0')
    grand_mrm, grand_mlod, grand_margt, grand_yrm, grand_ylod, grand_yargt = 0, Decimal('0.0'), Decimal('0.0'), 0, Decimal('0.0'), Decimal('0.0')
    
    db_session = local_storage.db_session
    tmp_list, ta_nat_stat = [], []

    # Prepare cache for models
    prepare_cache([Guest, Genstat, Nation, Htparam, Arrangement, Artikel])

    from sqlalchemy import extract

    def create_list():
        nonlocal tmp_list
        mm = int(from_date[:2])
        yr = int(from_date[2:6])
        
        # Clear temp list
        tmp_list = []

        # Optimized SQL query to fetch genstat, guest, nation, and arrangement data
        query = db_session.query(Genstat.gastnr, Genstat.argt, Genstat.datum, Genstat.logis, Genstat.ratelocal, 
                                Genstat.resstatus, Guest.land, Guest.name, Guest.anredefirma, Nation.kurzbez).join(Guest, Guest.gastnr == Genstat.gastnr).join(Nation, Nation.kurzbez == Guest.land).filter(
            Genstat.zinr != '',
            Genstat.karteityp == 2,
            Genstat.res_logic[2] == True,
            extract('year', Genstat.datum) == yr,
            extract('month', Genstat.datum) <= mm
        ).order_by(Genstat.gastnr).all()

        # Process the results
        for row in query:
            gastnr, argt, datum, logis, ratelocal, resstatus, land, name, anredefirma, nation = row
            # Fetch arrangement details for taxes calculation
            arrangement = db_session.query(Arrangement).filter(Arrangement.arrangement == argt).first()
            artikel = db_session.query(Artikel).filter(Artikel.artnr == arrangement.artnr_logis, Artikel.departement == 0).first() if arrangement else None

            service, vat, vat2, fact = Decimal('0.0'), Decimal('0.0'), Decimal('0.0'), Decimal('0.0')

            if artikel:
                result_tax = calc_servtaxesbl(1, artikel.artnr, artikel.departement, datum)
                service = result_tax.get('service', Decimal('0.0'))
                vat = result_tax.get('vat', Decimal('0.0'))
                vat2 = result_tax.get('vat2', Decimal('0.0'))
                fact = result_tax.get('fact', Decimal('0.0'))
                vat += vat2

            tmp_list.append({
                'gastnr': gastnr,
                'ta_name': f"{name}, {anredefirma}",
                'nation': nation if nation else "***",
                'rmnite': 1 if resstatus != 13 else 0,
                'argtumz': ratelocal / (1 + vat + service),
                'logiumz': logis,
                'ytd_rmnite': 1 if resstatus != 13 else 0,
                'ytd_logi': logis,
                'ytd_argt': ratelocal / (1 + vat + service)
            })
            
    def create_browse_or_browse1(is_browse1=False):
        nonlocal ta_nat_stat, sub_mrm, sub_mlod, sub_margt, sub_yrm, sub_ylod, sub_yargt
        nonlocal grand_mrm, grand_mlod, grand_margt, grand_yrm, grand_ylod, grand_yargt
        
        ta_nat_stat = []
        i = 0
        curr_key = "" if not is_browse1 else ""
        it_exists = False
        
        # Reset totals
        sub_mrm, sub_mlod, sub_margt, sub_yrm, sub_ylod, sub_yargt = 0, Decimal('0.0'), Decimal('0.0'), 0, Decimal('0.0'), Decimal('0.0')
        grand_mrm, grand_mlod, grand_margt, grand_yrm, grand_ylod, grand_yargt = 0, Decimal('0.0'), Decimal('0.0'), 0, Decimal('0.0'), Decimal('0.0')
        
        # Sort by nation or guestnr based on the flag
        sorted_list = sorted(tmp_list, key=lambda x: x['nation'] if is_browse1 else x['gastnr'])
        
        for item in sorted_list:
            if curr_key != "" and curr_key != item['nation'] and is_browse1 or curr_key != item['gastnr'] and not is_browse1:
                # Add subtotal
                i += 1
                ta_nat_stat.append({'nr': i})

                i += 1
                ta_nat_stat.append({
                    'nr': i,
                    'ta_name': text2,
                    'rmnite': format_number(sub_mrm, ">,>>9"),
                    'logiumz': format_number(sub_mlod, "->>>,>>>,>>9.99"),
                    'argtumz': format_number(sub_margt, "->>>,>>>,>>9.99"),
                    'ytd_rmnite': format_number(sub_yrm, ">>>,>>9"),
                    'ytd_logi': format_number(sub_ylod, "->>,>>>,>>>,>>9.99"),
                    'ytd_argt': format_number(sub_yargt, "->>,>>>,>>>,>>9.99")
                })
                
                i += 1
                ta_nat_stat.append({'nr': i})
                
                # Reset subtotals
                sub_mrm, sub_mlod, sub_margt, sub_yrm, sub_ylod, sub_yargt = 0, Decimal('0.0'), Decimal('0.0'), 0, Decimal('0.0'), Decimal('0.0')

            # Add detail line
            i += 1
            ta_nat_stat.append({
                'nr': i,
                'ta_name': item['ta_name'][:36],
                'nation': item['nation'][:3] if is_browse1 else item['nation'],
                'rmnite': format_number(item['rmnite'], ">,>>9"),
                'logiumz': format_number(item['logiumz'], "->>>,>>>,>>9.99"),
                'argtumz': format_number(item['argtumz'], "->>>,>>>,>>9.99"),
                'ytd_rmnite': format_number(item['ytd_rmnite'], ">>>,>>9"),
                'ytd_logi': format_number(item['ytd_logi'], "->>,>>>,>>>,>>9.99"),
                'ytd_argt': format_number(item['ytd_argt'], "->>,>>>,>>>,>>9.99")
            })

            # Update totals
            sub_mrm += item['rmnite']
            sub_mlod += item['logiumz']
            sub_margt += item['argtumz']
            sub_yrm += item['ytd_rmnite']
            sub_ylod += item['ytd_logi']
            sub_yargt += item['ytd_argt']

            grand_mrm += item['rmnite']
            grand_mlod += item['logiumz']
            grand_margt += item['argtumz']
            grand_yrm += item['ytd_rmnite']
            grand_ylod += item['ytd_logi']
            grand_yargt += item['ytd_argt']

            it_exists = True
            curr_key = item['nation'] if is_browse1 else item['gastnr']
        
        if it_exists:
            # Add final subtotal
            i += 1
            ta_nat_stat.append({'nr': i})

            i += 1
            ta_nat_stat.append({
                'nr': i,
                'ta_name': text2,
                'rmnite': format_number(sub_mrm, ">,>>9"),
                'logiumz': format_number(sub_mlod, "->>>,>>>,>>9.99"),
                'argtumz': format_number(sub_margt, "->>>,>>>,>>9.99"),
                'ytd_rmnite': format_number(sub_yrm, ">>>,>>9"),
                'ytd_logi': format_number(sub_ylod, "->>,>>>,>>>,>>9.99"),
                'ytd_argt': format_number(sub_yargt, "->>,>>>,>>>,>>9.99")
            })

            i += 1
            ta_nat_stat.append({'nr': i})

            # Add grand total
            i += 1
            ta_nat_stat.append({
                'nr': i,
                'ta_name': text3,
                'rmnite': format_number(grand_mrm, ">,>>9"),
                'logiumz': format_number(grand_mlod, "->>>,>>>,>>9.99"),
                'argtumz': format_number(grand_margt, "->>>,>>>,>>9.99"),
                'ytd_rmnite': format_number(grand_yrm, ">>>,>>9"),
                'ytd_logi': format_number(grand_ylod, "->>,>>>,>>>,>>9.99"),
                'ytd_argt': format_number(grand_yargt, "->>,>>>,>>>,>>9.99")
            })

    def format_number(value, format_str):
        """Helper function to format numbers according to Progress format strings"""
        if isinstance(value, Decimal):
            value = float(value)
        
        if format_str == ">,>>9":
            return f"{value:,.0f}".replace(",", "'")
        elif format_str == "->>>,>>>,>>9.99":
            return f"{value:,.2f}".replace(",", "'")
        elif format_str == ">>>,>>9":
            return f"{value:,.0f}".replace(",", "'")
        elif format_str == "->>,>>>,>>>,>>9.99":
            return f"{value:,.2f}".replace(",", "'")
        else:
            return str(value)

    # Main execution
    if from_date != last_period:
        create_list()
    
    if sorttype == 1:
        create_browse_or_browse1(is_browse1=True)
    else:
        create_browse_or_browse1(is_browse1=False)
    
    def generate_output():
        return {'ta_nat_stat': ta_nat_stat}
    
    return generate_output()
