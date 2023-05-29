#!/usr/bin/env python

####### db-sync ###########################################################
import pymysql

import pandas as pd

from sqlalchemy import create_engine
import psycopg2 
from psycopg2.extras import RealDictCursor

import io
import datetime


p = "SELECT p.id, p.name, p.vorname, p.geburtsdatum, p.strasse, p.plz, p.ort, p.telefon, p.telefon_mobil,p.email, CASE WHEN vers_nr = '' or vers_nr is null THEN '-' ELSE vers_nr END as ver_nr, aufgen_am, k.name as kk FROM `hecrasoft-movimento`.patienten as p left join kassen as k on p.id_kassen = k.id;"
m = "SELECT id, name, vorname, geburtsdatum, strasse, plz, ort FROM `hecrasoft-movimento`.adresse where firma like 'Movi%' and id_adressart = 7;"
a = "select id, case when id_filiale = 1 then 'KS' when id_filiale = 2 then 'GÖ' end as filiale, bemerkung, kostenstelle, erstellt_am, case when geplante_abgabe_am = '0000-00-00' then CAST('3000-01-01' as date) else geplante_abgabe_am END  as geplante_abgabe_am,case when id_hilfsmittel_vl is not null then id_hilfsmittel_vl else 00 end as id_himi_vl from `hecrasoft-movimento`.auftraege where storno_am = 0 and id_patienten is not null"

p2a = "SELECT id_patienten as pid, id as aid from `hecrasoft-movimento`.auftraege where storno_am = 0 and id_patienten is not null"
m2a = "select id_ma_werkstatt as mid, id as aid from `hecrasoft-movimento`.auftraege where storno_am = 0"
p2u = "select id as pid, id_kassen as kid, id_aerzte as aeid, id_aerzte2 as aeid2, id_aerzte3 as aeid3, id_aerzte4 as aeid4, id_einrichtung as eid, id_therapeut as thid, id_therapeut2 as thid2 from `hecrasoft-movimento`.patienten"

a2state = "select id, id_abrech_kz, id_prod_status from auftraege"

l = "SELECT id, firma, name, vorname, geburtsdatum, strasse, plz, ort, telefon, telefax, email, internet, kundennr from `hecrasoft-movimento`.lieferanten"
ls = "SELECT lfdnum as id, id_auftraege as aid, erstellt_am, gedruckt_am, unterschrieben_am from `hecrasoft-movimento`.lieferschein"
kv = "select id, id_auftraege as aid, erstellt_am, gesendet_am, genehmigt_am, abgelehnt_am, ekv from kv where id_auftraege > 20000"

pgp = "select * from patients"
pga = "select id, filiale, bemerkung, kostenstelle, erstellt_am, geplante_abgabe_am::date, id_himi_vl from auftraege"
pgm = "select * from mitarbeiter"
pgp2a = "select * from p2a"
pgm2a = "select * from m2a"
pgp2u = "select * from p2u"

ae = "select id, name, vorname, namenszusatz as info, strasse, plz, ort, telefon, email, arztnr, betriebsnr from aerzte"
r = "select id_auftraege as aid, angefordert_am, eingegangen_am, abgerechnet_am from rezept"
artikel = "select id, mengeneinheit, artikel_nr, kurzbeschreibung, beschreibung, hmv_nr, preis \
            from artikelliste where id_artikelliste_katalog = 21 and id_artikelliste_gruppe = 1102"
re = "select r.id, r.id_auftraege, r.lfdnum, r.erstellt_am, r.gedruckt_am, r.faellig_am, r.bezahlt_am, r.eigenanteil, r.mahnung, r.mahnung_1_am,r.mahnung_2_am,r.mahnung_3_am, a.gesamt_brutto, a.eigenanteil_mwstvoll, a.eigenanteil_mwsthalb from `hecrasoft-movimento`.rechnung as r inner join `hecrasoft-movimento`.auftraege as a on r.id_auftraege = a.id"
#re = "select * from rechnung"

def getData(Query):
#    connection = pymysql.connect(host='85.214.197.218', user='movimento', password='SEVzbI1KqZ2094KU', db='hecrasoft-movimento', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
#    connection = pymysql.connect(host='81.169.134.104', user='movimento', password='Cvqy?yB6c#cVDt9L', db='hecrasoft-movimento', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    connection = pymysql.connect(host='www.movimento.hecrasoft.de', user='movimento', password='Cvqy?yB6c#cVDt9L', db='hecrasoft-movimento', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    print("hecrasoft data loaded")
    cursor = connection.cursor()
    cursor.execute(Query)
    data = cursor.fetchall()
    connection.commit()
    connection.close()
    return data


from psycopg2.extras import RealDictCursor



def getPGData(pg_Query):
    try:
        #connect = psycopg2.connect(dbname='mov_db', user='postgres', host='192.168.3.157', port='54321', password='postgres')
        connect = psycopg2.connect(dbname='mov_db', user='root', host='192.168.3.64', port='5432', password='postgres')
        cur = connect.cursor(cursor_factory = RealDictCursor)
        cur.execute(pg_Query)
        pg_data = cur.fetchall()
        connect.commit()
        connect.close()
    except:
        print("Error") 
    else:    
        print ("pg data loaded: "+pg_Query)
        return pg_data
    finally:
        print("everything went fine!")

def syncDB():
    df_p = pd.DataFrame(getData(p))
    df_m = pd.DataFrame(getData(m))
    df_p2a = pd.DataFrame(getData(p2a))
    df_m2a = pd.DataFrame(getData(m2a))
    df_p2u = pd.DataFrame(getData(p2u))
    df_a = pd.DataFrame(getData(a))
    df_l = pd.DataFrame(getData(l))
    df_ls = pd.DataFrame(getData(ls))
    df_a2state = pd.DataFrame(getData(a2state))
    df_kv = pd.DataFrame(getData(kv))
    df_ae = pd.DataFrame(getData(ae))
    df_r = pd.DataFrame(getData(r))
    df_artikel = pd.DataFrame(getData(artikel))
    df_re = pd.DataFrame(getData(re))
    print ("Hecrasoft-Data sucessfully loaded!")
    # do some decoding / encoding bullshit to fix php-windows bug
    #df_p["name"]=df_p["name"].str.encode('windows-1252').str.decode('utf-8')
    #df_p["vorname"]=df_p["vorname"].str.encode('windows-1252').str.decode('utf-8') 
    #df_p["strasse"]=df_p["strasse"].str.encode('windows-1252').str.decode('utf-8')
    #df_p["ort"]=df_p["ort"].str.encode('windows-1252').str.decode('utf-8')
    #df_a["bemerkung"]=df_a["bemerkung"].str.encode('windows-1252').str.decode('utf-8')

    df_p["name"]=df_p["name"]
    df_p["vorname"]=df_p["vorname"]
    df_p["strasse"]=df_p["strasse"]
    df_p["ort"]=df_p["ort"]
    df_a["bemerkung"]=df_a["bemerkung"]


    # get pg-Data
    df_pgp = pd.DataFrame(getPGData(pgp))
    df_pgm = pd.DataFrame(getPGData(pgm))
    df_pgp2a = pd.DataFrame(getPGData(pgp2a))
    df_pgm2a = pd.DataFrame(getPGData(pgm2a))
    df_pgp2u = pd.DataFrame(getPGData(pgp2u))
    df_pga = pd.DataFrame(getPGData(pga))
    print ("postgres-Data sucessfully loaded!")
    df_diff_p = pd.concat([df_pgp, df_p], sort=False).loc[df_pgp.index.symmetric_difference(df_p.index)]
    df_diff_a = pd.concat([df_pga, df_a], sort=False).loc[df_pga.index.symmetric_difference(df_a.index)]
    df_diff_m = pd.concat([df_pgm, df_m], sort=False).loc[df_pgm.index.symmetric_difference(df_m.index)]
    df_diff_p2a = pd.concat([df_pgp2a, df_p2a], sort=False).loc[df_pgp2a.index.symmetric_difference(df_p2a.index)]
    df_diff_m2a = pd.concat([df_pgm2a, df_m2a], sort=False).loc[df_pgm2a.index.symmetric_difference(df_m2a.index)]
    df_diff_p2u = pd.concat([df_pgp2u, df_p2u], sort=False).loc[df_pgp2u.index.symmetric_difference(df_p2u.index)]
    print("differences checked!")
    #
    #
    #upload to postgres
    #connect = psycopg2.connect(dbname='mov_db', user='root', host='192.168.3.64', port='5432', password='postgres')
    #connect.set_client_encoding('UTF8')
    #engine = create_engine(connect)

    engine = create_engine('postgresql+psycopg2://service_user:service@192.168.3.64:5432/mov_db',encoding="utf-8")
    #engine = create_engine('postgresql+psycopg2://service_user:service@192.168.3.157:54321/mov_db')
    df_diff_p.to_sql('patients', engine, if_exists='replace',index=False)
    df_diff_a.to_sql('auftraege', engine, if_exists='append',index=False)
    df_diff_m.to_sql('mitarbeiter', engine, if_exists='append',index=False)
    df_diff_p2a.to_sql('p2a', engine, if_exists='append',index=False)
    df_diff_m2a.to_sql('m2a', engine, if_exists='append',index=False)
    df_diff_p2u.to_sql('p2u', engine, if_exists='append',index=False)
    df_a2state.to_sql('a2state', engine, if_exists='replace', index=False)
    df_kv.to_sql('kv', engine, if_exists='replace', index=False)
    df_ls.to_sql('lieferschein', engine, if_exists='append',index=False)
    df_r.to_sql('rezepte', engine, if_exists='replace',index=False)
    #df_artikel.to_sql('artikel_gwq_pg23', engine, if_exists='replace',index=False)
    df_re.to_sql('rechnung', engine, if_exists='replace',index=False)

    print("update lieferschein")
    df_ae.to_sql('aerzte', engine, if_exists='append',index=False)
    print("update aerzte")    
    print("data loaded to postgres!")
    connect = psycopg2.connect(dbname='mov_db', user='root', host='192.168.3.64', port='5432', password='postgres')
    cur = connect.cursor(cursor_factory = RealDictCursor)
    cur.execute('select company.update_tables();')
    print("update completed")
    cur.execute('TRUNCATE public.aerzte;')
    cur.execute('TRUNCATE public.lieferschein;')
    connect.commit()
    connect.close()
    df_ls.to_sql('lieferschein', engine, if_exists='append',index=False)
    print("update lieferschein")   
    now = datetime.datetime.now()
    print("db-sync completed:"+now.strftime("%Y-%m-%d %H:%M:%S"))
    

#connect.set_client_encoding('UTF8')
