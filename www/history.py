import dbconn
conn,cur = dbconn.getDbConn()
# Total conections history
sql = "INSERT INTO active_stat_history(tst,dhcpdhn,active_count_max,active_count_min,active_count_avg) SELECT date_trunc('day',current_timestamp - interval '24 hour'),dhcpdhn,max(active_count),min(active_count),avg(active_count) from active_stat WHERE date_trunc('day',tst)=date_trunc('day',current_timestamp - interval '24 hour') group by dhcpdhn;"
cur.execute(sql)
# Conections per ipblock history
sql = "INSERT INTO ipblock_stat_history(tst,dhcpdhn,ipblock,active_count_max,active_count_min,active_count_avg) SELECT date_trunc('day',current_timestamp - interval '24 hour'),dhcpdhn,ipblock,max(active_count),min(active_count),avg(active_count) from ipblock_stat WHERE date_trunc('day',tst)=date_trunc('day',current_timestamp - interval '24 hour') group by dhcpdhn,ipblock;"
cur.execute(sql)
# Conections per CPE model & vendor
sql = "INSERT INTO cpe_stat_history(tst,dhcpdhn,cpevendormodel,active_count_max,active_count_min,active_count_avg) SELECT date_trunc('day',current_timestamp - interval '24 hour'),dhcpdhn,cpevendormodel,max(active_count),min(active_count),avg(active_count) from cpe_stat WHERE date_trunc('day',tst)=date_trunc('day',current_timestamp - interval '24 hour') group by dhcpdhn,cpevendormodel;"
cur.execute(sql)
# Commit changes
conn.commit()
