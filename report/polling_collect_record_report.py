# -*-coding: utf-8 -*-
from openerp.osv import fields,osv
from openerp import tools
from .. import polling

MONTHS = [
    ('01', 'January'),
    ('02', 'February'),
    ('03', 'March'),
    ('04', 'April'),
    ('05', 'May'),
    ('06', 'June'),
    ('07', 'July'),
    ('08', 'August'),
    ('09', 'September'),
    ('10', 'October'),
    ('11', 'November'),
    ('12', 'December')
]

class polling_collect_record_report(osv.osv):
    _name = 'polling.collect.record.report'
    _auto = False
    _description = 'Polling collect record analysis'

    _columns = {
        'asset_id':fields.many2one('polling.asset',string='Asset'),
        'asset_attr_id':fields.many2one('polling.asset.attribute',string='Attribute'),
        'collect_point_id':fields.many2one('polling.asset.collectpoint',string='Collect point'),
        'collect_value':fields.char(string='Collect value',size=100),
        'collect_time':fields.datetime(string='Collect time'),
        'excep_type':fields.char(string='Excep type',size=100),
        # grouping fields based on Create Date
        'collect_year': fields.char('Collect Year', size=10, readonly=True, help="Collect year"),
        'collect_month': fields.selection(MONTHS, 'Collect Month', readonly=True, help="Collect month"),
        'collect_day': fields.char('Collect Day', size=10, readonly=True, help="Collect day"),
        'fault_count':fields.integer(string='Fault count'),
    }

    def init(self,cr):
        print "init method start"
        tools.drop_view_if_exists(cr,'polling_collect_record_report')
        cr.execute("""
            CREATE OR REPLACE VIEW polling_collect_record_report AS(
                   SELECT 
                        id,
                        c.asset_id,
                        c.asset_attr_id,
                        c.collect_point_id,
                        c.collect_value,
                        c.excep_type,
                        to_char(c.collect_time,'YYYY') as collect_year,
                        to_char(c.collect_time,'MM') as collect_month,
                        to_char(c.collect_time,'YYYY-MM-DD') as collect_day,
                        1 as fault_count
                   FROM 
                        polling_asset_collect_record  c
                  )""")
polling_collect_record_report()

