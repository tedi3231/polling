# -*- coding: utf-8 -*-
from openerp.osv import fields,osv
from openerp import tools
from lxml import etree
from openerp.tools import to_xml
from openerp.tools.translate import _
from openerp.modules.registry import RegistryManager
import string
import datetime

SECURITYLEVEL = [('high','High'),('low','Low'),('middle','Middle')]
EXECUTELEVEL = [('high','High'),('low','Low'),('middle','Middle')]
DATATYPE = [('string','String'),('integer','Integer'),('boolean','Boolean'),('decimal','Decimal')]
CONTROLTYPE = [('input','Input'),('dropdonlist','DropDownList'),('checkbox','CheckBox'),('radiolist','RadioList')]
RELATIONS = [('hoston',"Host On"),("allocateto","Allocate To"),("parentchild","Parent-Child"),
             ("connected","Connected"),("installedsoftware","Installed Software"),("documentbackup","Document backup"),
             ("dependent","Dependent"),("contains","Contains"),("ispartof","Is part of")]

"""
Positive 正向
Negative 反向
Double   双向
"""
RELATIONTYPES = [("positive","Positive"),("negative","Negative"),("double","Double")]

class polling_relationtype(osv.osv):
    _name = "polling.relationtype"
    _columns = {
        "name":fields.char(string="Name",size=100,required=True),
        "code":fields.char(string="Code",size=100,required=True),
        "direction":fields.selection(RELATIONTYPES,string="Direction",size=100,required=True),
        "description":fields.char(string="Description",size=500),
    }
    _sql_constraints = [("code_unique","unique(code)","code must be unique")]

polling_relationtype()

class polling_assettemplatecategory(osv.osv):
    _name="polling.assettemplatecategory"
    _description = "Asset category"

    def name_get(self, cr, uid, ids, context=None):
        if isinstance(ids, (list, tuple)) and not len(ids):
            return []
        if isinstance(ids, (long, int)):
            ids = [ids]
        print "ids is %s " % ids
        reads = self.read(cr, uid, ids, ['name','parent_id'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['parent_id']:
                name = record['parent_id'][1]+' / '+name
            res.append((record['id'], name))
        return res

    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_get(cr, uid, ids, context=context)
        return dict(res)

    def child_get(self, cr, uid, ids):
        return [ids]

    def _check_recursion(self, cr, uid, ids, context=None):
        level = 100
        while len(ids):
            cr.execute('select distinct parent_id from polling_assettemplatecategory where id IN %s',(tuple(ids),))
            ids = filter(None, map(lambda x:x[0], cr.fetchall()))
            if not level:
                return False
            level -= 1
        return True
    
    _columns = {
        'name': fields.char(string='Name', size=64, required=True, translate=True, select=True),
        'complete_name': fields.function(_name_get_fnc, type="char", string='Full Name'),
        'parent_id': fields.many2one('polling.assettemplatecategory',string='Parent', select=True, ondelete='cascade'),
        'child_id': fields.one2many('polling.assettemplatecategory', 'parent_id', string='Children'),
        'sequence': fields.integer(string='Sequence', select=True, help="Gives the sequence order when displaying a list of product \
                                                             categories."),
        'parent_left': fields.integer('Left parent', select=True),
        'parent_right': fields.integer('Right parent', select=True),
        "remark":fields.text(string="Remark")
    }

    _constraints = [
        (_check_recursion, '错误！您不能循环创建目录.', ['parent_id'])
    ]

    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = 'sequence, name'
    _order = "parent_left"

polling_assettemplatecategory()

def get_tree_top2low(objname,cr,uid,parent_id,context=None):
    """
    自顶向下的寻找，不包含自己
    """
    print "objname is %s,cr.dbname is %s,uid is %s,parent_id is %s" % (objname,cr.dbname,uid,parent_id)
    if not objname:
        return None
    registry = RegistryManager.get(cr.dbname)
    rep = registry.get(objname)
    template = rep.read(cr,uid,parent_id,["parent_left","parent_right","id"],context=context)
    if not template:
        return None
    res = rep.search(cr,uid,[("parent_left",">",template["parent_left"]),("parent_right","<",template["parent_right"])],context=context)
    print "get_tree_low2top result is %s" % res
    return res

def get_tree_low2top(tablename,cr,uid,parent_id,context=None):
    """
    从自己向上找，即看自己所在的线上继承了多个元素 
    """    
    print "parent_id is %s" % parent_id
    cr.execute("SELECT A.* FROM %s as A \
                INNER JOIN %s as B \
                ON 1=1 \
                WHERE  A.parent_left < B.parent_left and \
                    A.parent_left < B.parent_right and   \
                    B.parent_left < A.parent_right and   \
                    B.parent_right < A.parent_right      \
                AND b.id=%s                               \
                ORDER BY A.id" % (tablename,tablename, parent_id))
    parent_ids = filter(None,map(lambda x:x[0],cr.fetchall()))
    parent_ids.append(parent_id)
    return parent_ids


def get_list_from_nestedlist(item):
    if not item:
        return []
    res = []
    for line in item:
        for i in line:
            res.append(i)
    return res

class polling_assettemplate(osv.osv):
    _name="polling.assettemplate"
    _description = "Asset Template"

    def name_get(self, cr, uid, ids, context=None):
        if isinstance(ids, (list, tuple)) and not len(ids):
            return []
        if isinstance(ids, (long, int)):
            ids = [ids]
        #print "ids is %s " % ids
        reads = self.read(cr, uid, ids, ['name','parent_id'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['parent_id']:
                name = record['parent_id'][1]+' / '+name
            res.append((record['id'], name))
        #print res
        return res

    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_get(cr, uid, ids, context=context)
        return dict(res)

    def child_get(self, cr, uid, ids):
        return [ids]

    def _check_recursion(self, cr, uid, ids, context=None):
        level = 100
        while len(ids):
            cr.execute('select distinct parent_id from polling_assettemplate where id IN %s',(tuple(ids),))
            ids = filter(None, map(lambda x:x[0], cr.fetchall()))
            if not level:
                return False
            level -= 1
        return True
    
    def get_inherit_attributes(self,cr,uid,ids,name,arg,context=None):
        res = {}
        for template in self.browse(cr,uid,ids,context=context):
            if not template.parent_id:
                continue
            parent_ids = get_tree_low2top("polling_assettemplate",cr,uid,template.parent_id.id,context=context) 
            if not parent_ids:
                continue
            attrs = self.read(cr,uid,parent_ids,["id","attributes"],context=context)
            temp = [item["attributes"] for item in attrs]
            attr_ids = get_list_from_nestedlist(temp)
            res[template.id] = attr_ids
        return res

    def get_inherit_actions(self,cr,uid,ids,name,arg,context=None):
        res = {}
        for template in self.browse(cr,uid,ids,context=context):
            if not template.parent_id:
                continue
            parent_ids = get_tree_low2top("polling_assettemplate",cr,uid,template.parent_id.id,context=context) 
            if not parent_ids:
                continue
            actions = self.read(cr,uid,parent_ids,["id","actions"],context=context)
            temp = [item["actions"] for item in actions]
            action_ids = get_list_from_nestedlist(temp)
            res[template.id] = action_ids
        return res

    def get_inherit_relations(self,cr,uid,ids,name,arg,context=None):
        res = {}
        for template in self.browse(cr,uid,ids,context=context):
            if not template.parent_id:
                continue
            parent_ids = get_tree_low2top("polling_assettemplate",cr,uid,template.parent_id.id,context=context) 
            if not parent_ids:
                continue
            relations = self.read(cr,uid,parent_ids,["id","relations"],context=context)
            temp = [item["relations"] for item in relations]
            relation_ids = get_list_from_nestedlist(temp)
            res[template.id] = relation_ids
        return res

    def onchange_parent_get_inherit_attributes(self,cr,uid,ids,parentid,context=None):
        result = []
        action_res = []
        relation_res = []
        parent_ids =  get_tree_low2top("polling_assettemplate",cr,uid,parentid,context=context) 
        #self._get_inherit_tree(cr, uid,parentid, context=context)
        attr_rep = self.pool.get("polling.assettemplate.attribute")
        attr_ids = attr_rep.search(cr,uid,[('assettemplate_id','in',parent_ids)],context=context)
        for item in attr_rep.read(cr,uid,attr_ids,[],context=context):
            result.append(item)
        
        action_rep = self.pool.get("polling.assettemplate.action")
        action_ids = attr_rep.search(cr,uid,[('assettemplate_id','in',parent_ids)],context=context)
        for item in action_rep.read(cr,uid,action_ids,[],context=context):
            action_res.append(item)

        relation_rep = self.pool.get("polling.assettemplate.relation")
        relation_ids = relation_rep.search(cr,uid,[('assettemplate_id','in',parent_ids)],context=context)
        for item in relation_rep.read(cr,uid,action_ids,[],context=context):
            relation_res.append(item)
        #result2[ids] = result
        print "result is %s" % result
        return  {
                    "value": {
                        "inherit_attributes" : result,
                        "inherit_actions": action_res,
                        "inherit_relations": relation_res,
                    }
                }
    
    _columns = {
        "category_id":fields.many2one("polling.assettemplatecategory",string="Category",select=True),
        'name': fields.char(string='Name', size=64, required=True, translate=True, select=True),
        "code":fields.char(string="Code",size=200,required=True,help="Code must be unique"),
        "description":fields.char(string="Description",size=1000,required=False,help="Description the target of template"),
        'complete_name': fields.function(_name_get_fnc, type="char", string='Full Name'),
        'parent_id': fields.many2one('polling.assettemplate',string='Parent', select=True, ondelete='cascade'),
        'child_id': fields.one2many('polling.assettemplate', 'parent_id', string='Children'),
        "attributes":fields.one2many("polling.assettemplate.attribute","assettemplate_id",string="Attributes"),
        "actions":fields.one2many("polling.assettemplate.action","assettemplate_id",string="Actions"),
        "relations":fields.one2many("polling.assettemplate.relation","assettemplate_id",string="Relations"),
        "inherit_attributes":fields.function(get_inherit_attributes,type="one2many",relation="polling.assettemplate.attribute",string="Inherit Attributes"),
        "inherit_actions":fields.function(get_inherit_actions,type="one2many",relation="polling.assettemplate.action",string="Inherit Actions"),
        "inherit_relations":fields.function(get_inherit_relations,type="one2many",relation="polling.assettemplate.relation",string="Inherit Relations"),
        'sequence': fields.integer(string='Sequence', select=True, help="Gives the sequence order when displaying a list of product \
                                                             categories."),
        'parent_left': fields.integer('Left parent', select=True),
        'parent_right': fields.integer('Right parent', select=True),
        "haspush":fields.boolean(string="Has Push",tooltip="template has asset instance"),
        "remark":fields.text(string="Remark"),
    }

    _constraints = [
        (_check_recursion, '错误！您不能循环创建目录.', ['parent_id'])
    ]

    _defaults = {
        #"code":lambda self,cr,uid,context:self.pool.get("ir.sequence").get(cr,uid,"seq.polling.assettemplate.code")
    }


    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = 'sequence, name'
    _order = "parent_left"
polling_assettemplate()

class polling_assettemplate_attribute(osv.osv):
    _name="polling.assettemplate.attribute"

    def push_attribute(self,cr,uid,ids,context=None):
        templates = self.read(cr,uid,ids,[],context=context)
        print "templates is %s "%templates 
        if not templates:
            return False
        template = templates[0]
        template_id = template["assettemplate_id"][0]
        res = get_tree_top2low("polling.assettemplate",cr,uid,template_id,context=context)
        res.append(template_id)
        #print "push res is %s " % res
        asset_rep = self.pool.get("polling.asset")
        asset_ids = asset_rep.search(cr,uid,[("assettemplate_id","in",res)],context=context)
        print "asset_ids is %s " % asset_ids
        asset_attr_rep = self.pool.get("polling.asset.attribute")
        for asset_id in asset_ids:
            template["asset_id"] = asset_id
            template["fromtemplate"] = True
            print "attr instance is %s " % template
            asset_attr_rep.create(cr,uid,template,context=context)
        self.write(cr,uid,ids,{'state':'haspush'},context=context)
        return True
    
    _columns = {
        "assettemplate_id":fields.many2one("polling.assettemplate",string="Template"),
        "name":fields.char(string="Name",size=200,required=True,help="The name of the attribute"),
        "code":fields.char(string="Code",size=200,required=True,help="unique"),
        "tooltip":fields.char(string="Tool Tip", size=500),
        "securitylevel":fields.selection(SECURITYLEVEL,string="Security Level"),
        "datatype":fields.selection(DATATYPE, string="Data Type", required=True ),
        "controltype":fields.selection(CONTROLTYPE, string="Control Type",required=True),
        "sourcefrom":fields.char(string="Value Source",size=100,required=False),
        "sourcetype":fields.selection(DATATYPE, string="Source Type",required=False,size=100),
        "defaultvalue":fields.char(string="Default Value",size=500,required=False),
        "remark":fields.char(string="Remark",size=500,required=False),
        "high":fields.char(string="High",size=500),
        "low":fields.char(string="Low",size=500),
        "state":fields.selection([("haspush","Pushed"),("nopush","Not Push")],string="State"),
    }

    _defaults = {
        "securitylevel":"low",
        "controltype":"input",
        "sourcetype":"integer",
        "state":"nopush",
        #"code":lambda self,cr,uid,context:self.pool.get("ir.sequence").get(cr,uid,"seq.polling.assettemplate.attribute.code")
    }

polling_assettemplate_attribute()

class polling_assettemplate_relation(osv.osv):
    _name = "polling.assettemplate.relation"
    
    _columns = {
        "assettemplate_id":fields.many2one("polling.assettemplate",string="AssetTemplate"),
        "relationtype_id":fields.many2one("polling.relationtype",string="Relation Type"),
        "assettemplate_id2":fields.many2one("polling.assettemplate",string="AssetTemplate To"),
        "relationtype_id2":fields.many2one("polling.relationtype",string="Relation from type"),
    }

    _defaults = {
        #"code":lambda self,cr,uid,context:self.pool.get("ir.sequence").get(cr,uid,"seq.assettemplate.relation.code"),
    }
polling_assettemplate_relation()

class polling_assettemplate_action(osv.osv):
    _name="polling.assettemplate.action"
    
    def removeattr(self,cr,uid,ids,context=None):
        self.unlink(cr,uid,ids,context=context)
        #return template_id
        return True

    def push_action(self,cr,uid,ids,context=None):
        templates = self.read(cr,uid,ids,[],context=context)
        print "templates is %s "%templates 
        if not templates:
            return False
        template = templates[0]
        template_id = template["assettemplate_id"][0]
        res = get_tree_top2low("polling.assettemplate",cr,uid,template_id,context=context)
        res.append(template_id)
        #print "push res is %s " % res
        asset_rep = self.pool.get("polling.asset")
        asset_ids = asset_rep.search(cr,uid,[("assettemplate_id","in",res)],context=context)
        print "asset_ids is %s " % asset_ids
        asset_action_rep = self.pool.get("polling.asset.action")
        for asset_id in asset_ids:
            template["asset_id"] = asset_id
            print "action instance is %s " % template
            asset_action_rep.create(cr,uid,template,context=context)
        self.write(cr,uid,ids,{'state':'haspush'},context=context)
        return True
    
    _columns = {
        "assettemplate_id":fields.many2one("polling.assettemplate",string="Template"),
        "name":fields.char(string="Name",size=200,required=True,),
        "code":fields.char(string="Code",size=200,required=True,),
        "executelevel":fields.selection(SECURITYLEVEL,string="Execute Level"),
        "estimatetime":fields.integer(string="Estimate Time",required=True,help="Estimate execute time by hour"),
        "command":fields.text(string="Command",required=True,help="Command template,parameters with {name}"),
        "ordernum":fields.integer(string="Order",required=True,help="The execute order"),
        "batch":fields.char(string="Batch",required=False,help="If set batch,must execute together"),
        "state":fields.selection([("haspush","Pushed"),("nopush","Not Push")],string="State"),
    }
    
    _defaults = {
        "executelevel":"low",
        "ordernum":10,
        "state":"nopush",
        #"code":lambda self,cr,uid,context:self.pool.get("ir.sequence").get(cr,uid,"seq.assettemplate.action.code")
    }
polling_assettemplate_action()


class polling_asset(osv.osv):
    _name="polling.asset"
    _description = "Asset"

    def maintain_tree_view(self, cr, uid, ids, context):
        domain = [
             ('asset_id', 'in', ids),
        ]
        res_id = ids and ids[0] or False
        return {
            'name': _('Maintain orders'),
            'domain': domain,
            'res_model': 'polling.maintain',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'view_type': 'form',
            'limit': 80,
            'context': "{'default_asset_id': %d}" % (res_id)
        }

    def repair_tree_view(self, cr, uid, ids, context):
        domain = [
             ('asset_id', 'in', ids),
        ]
        res_id = ids and ids[0] or False
        return {
            'name': _('Reparir orders'),
            'domain': domain,
            'res_model': 'polling.repair',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'view_type': 'form',
            'limit': 80,
            'context': "{'default_asset_id': %d}" % (res_id)
        }

    def attachment_tree_view(self, cr, uid, ids, context):
        domain = [
             '&', ('res_model', '=', 'polling.asset'), ('res_id', 'in', ids),
        ]
        res_id = ids and ids[0] or False
        return {
            'name': _('Documents'),
            'domain': domain,
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'view_type': 'form',
            'limit': 80,
            'context': "{'default_res_model': '%s','default_res_id': %d}" % (self._name, res_id)
        }

    def default_get(self, cr, uid, fields_list, context=None):
        print'default_get method context is %s,fields_list is %s' % (context,fields_list)
        default = super(polling_asset, self).default_get(cr, uid, fields_list, context=context)
        con = context.get('is_data_collect')
        default['is_data_collect'] = con=='1'
        return default

    def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
        print 'context is %s ' % context
        if context is None:
            context = {}
        result = super(polling_asset, self).fields_view_get(cr, uid, view_id,  view_type=view_type, context=context, toolbar=toolbar, submenu=submenu)  
        doc = etree.XML(result['arch'])
        is_data_collect = context.get('is_data_collect')
        if view_type=='form' and is_data_collect=='0':
            #for node in doc.xpath("//group[@name='collect_data_group']"):
            #    print 'data_collect_group is %s' % node
            #    doc.remove(node)
            for node in doc.xpath("//page[@name='collect_ports_page']"):
                #print 'field is %s' % node
                node.getparent().remove(node)
                #doc.remove(node)
        result['arch'] = etree.tostring(doc)
        #print result['arch']
        return result

    def onchange_template_get_attributes(self,cr,uid,ids,parentid,context=None):
        result = []
        action_result = []
        relation_result = []
        #parent_ids =  self._get_inherit_tree(cr, uid, ids, parentid, context=context)
        parent_ids = get_tree_low2top("polling_assettemplate",cr,uid,parentid,context=context) 
        attr_rep = self.pool.get("polling.assettemplate.attribute")
        action_rep = self.pool.get("polling.assettemplate.action")
        relation_rep = self.pool.get("polling.assettemplate.relation")

        attr_ids = attr_rep.search(cr,uid,[('assettemplate_id','in',parent_ids)],context=context)
        action_ids = action_rep.search(cr,uid,[('assettemplate_id','in',parent_ids)],context=context)
        relation_ids = relation_rep.search(cr,uid,[('assettemplate_id','in',parent_ids)],context=context)
        
        for item in attr_rep.read(cr,uid,attr_ids,[],context=context):
            item["fromtemplate"] ="yes" #item["yes"]
            result.append(item)
            print "attr item is %s " % item
        
        for item in action_rep.read(cr,uid,action_ids,[],context=context):
            action_result.append(item)
        
        for item in relation_rep.read(cr,uid,relation_ids,[],context=context):
            relation_result.append(item)
            print "relationitem is %s " % item 
        #result2[ids] = result
        print "result is %s" % relation_result
        return  {
                    "value": {
                        "attributes" : result,
                        "actions": action_result,
                        "relations": relation_result,
                    }
        }

    _columns = {
        "category_id":fields.many2one("polling.assettemplatecategory",string="Category",select=True),
        "assettemplate_id": fields.many2one('polling.assettemplate',string='Template', select=True, ondelete='cascade'),
        "code":fields.char(string="Code",size=200,required=True,help="Code must be unique"),
        "name": fields.char(string='Name', size=64, required=True, translate=True, select=True),
        "specification":fields.char(string="Specification", size=100, required=False ),
        "install_building_id":fields.many2one("polling.building",string="Building"),
        "install_position_id":fields.many2one("polling.building.position",string="Position"),
        "brand":fields.char(string="Brand",size=100,required=False),
        "producingarea":fields.char(string="Producting Area", size=100,required=False),
        "dateofproduced":fields.date(string="Date of produced"),
        #使用年限
        "service_life":fields.integer(string="Service life"),
        "dateofinstalled":fields.date(string="Date of installed"),
        "buying_price":fields.float(string="Buying price"),
        "factory_number":fields.char(string="Factory number"),
        "asset_count":fields.integer(string="Asset count"),
        "asset_used":fields.char(string="Asset used", size=500, required=False),
        "attachment_content":fields.text(string="Attachment content"),
        "remark":fields.text(string="Remark"),
        "is_data_collect":fields.boolean(string="Is data collect"),
        "attributes":fields.one2many("polling.asset.attribute","asset_id",string="Attributes"),
        "relations":fields.one2many("polling.asset.relation","asset_id",string="Relations"),
        "actions":fields.one2many("polling.asset.action","asset_id",string="Actions"), 
        'collect_points':fields.one2many('polling.asset.collectpoint','asset_id',string='Collect points'),
    }

    _defaults = {
        #"code":lambda self,cr,uid,context:self.pool.get("ir.sequence").get(cr,uid,"seq.polling.asset.code"),
        "is_data_collect":False,
    }
polling_asset()

COLLECT_TYPES = [
    ("second","Second"),
    ("minute","Minute"),
    ("hour","Hour"),
    ("day","Day"),
]

class polling_asset_collectpoint(osv.osv):
    _name = 'polling.asset.collectpoint'
    
    def default_get(self, cr, uid, fields_list, context=None):
        print 'default_get parameters is %s,context is %s ' % (fields_list,context)
        collected_asset_id = context.get("collected_asset_id",None)
        default = super(polling_asset_collectpoint, self).default_get(cr, uid, fields_list, context=context)
        if collected_asset_id:
            point_item_ids = self.search(cr,uid,[('asset_id','=',collected_asset_id)],[],context=context)
            print 'has choosed points is %s'%point_item_ids
            #if point_items:
            if point_item_ids:
                point_items = self.read(cr,uid,point_item_ids,[],context=context)
                print 'point_items is %s' % point_items
                if point_items:
                    default['asset_id_2'] = point_items[0]['asset_id_2'][0]
        return default

    def on_change_attribute(self,cr,uid,ids,attr_id,context=None):
        attr_rep = self.pool.get('polling.asset.attribute')
        item = attr_rep.read(cr,uid,attr_id,context=context)
        print 'collect_points is %s' % item
        return {
            'value':{
                'attribute_name':item['name'],
                'attribute_code':item['code'],
            }
        }

    _columns = {
        'name':fields.char(string='Collect name',size=100,required=True),
        'asset_id':fields.many2one('polling.asset',string='Collect Asset'),
        'asset_id_2':fields.many2one('polling.asset',string='Collected Asset'),
        'attribute_id':fields.many2one('polling.asset.attribute',string='Attribute'),
        'attribute_name':fields.related('attribute_id','name',type='char',string='Attribute name',store=True),
        'attribute_code':fields.related('attribute_id','code',type='char',string='Attribute code',store=True),
        'collect_type':fields.selection(COLLECT_TYPES,string="type"),
        'collect_period':fields.integer(string="collect",required=True),
        'collect_period_count':fields.integer(string="count",required=True),
        'hasstop':fields.boolean(string="Hasstop"),
        'remark':fields.text(string='Remark'),
    }
    _parent_name='asset_id'

polling_asset_collectpoint()                                                                       

class polling_asset_collect_record(osv.osv):
    _name = 'polling.asset.collect.record'
    _columns = {
        'asset_id':fields.many2one('polling.asset',string='Asset'),
        'asset_attr_id':fields.many2one('polling.asset.attribute',string='Attribute'),
        'asset_attr_name':fields.related('asset_attr_id','name',type='char',string='Attribute name'),
        'asset_attr_code':fields.related('asset_attr_id','code',type='char',string='Attribute code'),
        'asset_attr_high':fields.related('asset_attr_id','high',type='char',string='High'),
        'asset_attr_low':fields.related('asset_attr_id','low',type='char',string='Low'),
        'collect_point_id':fields.many2one('polling.asset.collectpoint',string='Collect point'),
        'collect_asset_id':fields.related('collect_point_id','asset_id',type='many2one',relation='polling.asset',string='Collect asset'),
        'collect_value':fields.char(string='Collect value',size=100),
        'collect_time':fields.datetime(string='Collect time'),
        'state':fields.selection([('normal','Normal'),('lost','Lost'),('over','Over')],string='Status'),
    }
polling_asset_collect_record()
                              
class polling_asset_attribute(osv.osv):
    _name="polling.asset.attribute"
   
    _columns = {
        "asset_id":fields.many2one("polling.asset",string="Asset"),
        "name":fields.char(string="Name",size=200,required=True,help="The name of the attribute"),
        "code":fields.char(string="Code",size=200,required=True,help="unique"),
        "tooltip":fields.char(string="Tool Tip", size=500),
        "securitylevel":fields.selection(SECURITYLEVEL,string="Security Level"),
        "datatype":fields.selection(DATATYPE, string="Data Type", required=False ),
        "controltype":fields.selection(CONTROLTYPE, string="Control Type",required=False),
        "sourcefrom":fields.char(string="Value Source",size=100,required=False),
        "sourcetype":fields.selection(DATATYPE, string="Source Type",required=False,size=100),
        "defaultvalue":fields.char(string="Value",size=500,required=False),
        "fromtemplate":fields.selection([("yes","Yes"),("no","No")],string="FromTemplate"),
        "high":fields.char(string="High",size=500),
        "low":fields.char(string="Low",size=500),
        "remark":fields.char(string="Remark",size=500,required=False),
    }

    _defaults = {
        "securitylevel":"low",
        "controltype":"input",
        "sourcetype":"integer",
        "fromtemplate":"no",
    }

polling_asset_attribute()

class polling_asset_action(osv.osv):
    _name="polling.asset.action"

    def _format_action_command(self,cr,uid,asset_id,command,context=None):
        attr_rep = self.pool.get("polling.asset.attribute")
        attr_ids = attr_rep.search(cr,uid,[('asset_id','=',asset_id)],context=context)
        attr_items = attr_rep.read(cr,uid,attr_ids,[],context=context)
        values = {}
        for item in attr_items:
            values[item['code']] = item['defaultvalue']
        t_cmd = string.Template(command)
        content = t_cmd.safe_substitute(values)
        return content

    def get_format_asset_action(self,cr,uid,ids,name,arg,context=None):
        result = dict.fromkeys(ids,'None')
        for item in self.read(cr,uid,ids,['id','asset_id','command'],context=context):
            print "get_format_asset_action item is %s " % item
            print "type names is %s" % type(self)._name
            #if type(self)._name != "polling.asset.action.backup":
            #    result[item["id"]] = self._format_action_command(cr,uid,item["asset_id"][0],item["command"],context=context)
            print result
            #result[item["id"]] = "abc"
        return result
    
    _columns = {
        "asset_id":fields.many2one("polling.asset",string="Asset"),
        "name":fields.char(string="Name",size=200,required=True,),
        "code":fields.char(string="Code",size=200,required=True,),
        "executelevel":fields.selection(SECURITYLEVEL,string="Execute Level"),
        "estimatetime":fields.integer(string="Estimate Time",required=True,help="Estimate execute time by hour"),
        "command":fields.text(string="Command",required=True,help="Command template,parameters with {name}"),
        "cmdcontent":fields.function(get_format_asset_action,string="CMD Content",type="char"),
        "ordernum":fields.integer(string="Order",required=True,help="The execute order"),
        "batch":fields.char(string="Batch",required=False,help="If set batch,must execute together"),
    }
    
    _defaults = {
        "executelevel":"low",
        "ordernum":10,
    }
polling_asset_action()

class polling_asset_relation(osv.osv):
    _name = "polling.asset.relation"
   
    def on_change_asset2(self,cr,uid,ids,asset_id,asset_id2,context=None):
        print "ids is %s, asset_id is %s, asset_id2 is %s " % (ids,asset_id,asset_id2)
        if asset_id2 == asset_id:
            return {
                "value":{
                    "asset_id2":None,
                },
                "warning":{
                    "title":"Warning",
                    "message":"You cannot choose some asset!You must choose another!",
                }
            }
        return {"value":{
                "asset_id2":asset_id2,
            }
        }

    def create(self,cr,uid,data,context=None):
        print "relation is %s " % data
        if data["asset_id"] == data["asset_id2"]:
            raise osv.except_osv(_('Cannot connect to self!'),_("You must select another asset !") )
            
        if isinstance(data["relationtype_id"],(list,tuple)):
            data["relationtype_id"] = data["relationtype_id"][0]
        print "relation is %s " % data
        rel_id = super(polling_asset_relation,self).create(cr,uid,data,context=context)
        #if not rel_id:
        #    return False
        #rel_from = {"asset_id":data["asset_id2"],"relationtype_id":data["relationtype_id"],"asset_id2":data["asset_id"]}
        #print "rel_from is %s " % rel_from
        #super(AssetRelation,self).create(cr,uid,rel_from,context=context)
        return rel_id

    _columns = {
        "asset_id":fields.many2one("polling.asset",string="Asset"),
        "template_relation_id":fields.integer(string="Template Relation Id"),
        "relationtype_id":fields.many2one("polling.relationtype",string="Asset to type"),
        "asset_id2":fields.many2one("polling.asset",string="Asset To"),
    }

polling_asset_relation()


class polling_building(osv.osv):                                                                
     _name = "polling.building"         

     _columns = {                                                                                    
         "name":fields.char(string="Name",required=True,size=100),                                   
         "remark":fields.char(string="Remark",size=500,required=True),                               
         "positions":fields.one2many("polling.building.position","polling_building_id",strin="Racks"),        
     }                                                                                               
polling_building()                                                                              
                                                                                                     
class polling_building_position(osv.osv):                                                           
    _name = "polling.building.position"                                                             
    _columns = {                                                                                    
        "name":fields.char(string="Name",size=200,required=True),                                   
        "polling_building_id":fields.many2one("polling.building",string="Building",required=True),
        "remark":fields.char(string="Remark",size=500,required=False),                              
    }                                                                                               
polling_building_position()  

class polling_repair(osv.osv):
    _name = "polling.repair"

    def act_repairing(self,cr,uid,ids,context=None):
        return self.write(cr,uid,ids,{'state':'repairing','repairing_time':datetime.datetime.now()},context=context)

    def act_finish(self,cr,uid,ids,context=None):
        return self.write(cr,uid,ids,{'state':'finished','finished_time':datetime.datetime.now()},context=context)

    def on_asset_change(self,cr,uid,ids,asset_id,context=None):
        asset_rep = self.pool.get('polling.asset')
        item = asset_rep.read(cr,uid,asset_id,context=context)
        print 'asset item is %s' % item
        return {
            'value':{
                'category_id':item['category_id'] and item['category_id'][0],
                'install_building':item['install_building_id'] and item['install_building_id'][0],
                'specification':item['specification'],
                'asset_code':item['code'],
                'install_building_position':item['install_position_id'] and item['install_position_id'][0],
            }
        }

    _columns = {
        "name":fields.char(string="Repair Number",required=True,size=100),
        "asset_id":fields.many2one("polling.asset",string="Asset"),
        'category_id':fields.related('asset_id','category_id',type='many2one',relation='polling.assettemplatecategory',string='Category'),
        "install_building":fields.related("asset_id","install_building_id",type="many2one",relation="polling.building",string="Building"),
        "install_building_position":fields.related("asset_id",'install_position_id',type='many2one',relation='polling.building.position',string='Position'),
        'asset_code':fields.related('asset_id','code',type='char',string='Asset Code'),
        'asset_specification':fields.related('asset_id','specification',type='char',string='Specification'),
        'repair_man':fields.many2one('hr.employee',string='Repair man'),
        'repair_date':fields.datetime(string='Repair date'),
        'repair_time':fields.integer(string='Repair time'),
        'fault_reason':fields.text(string='Fault reason'),
        'repair_method':fields.text(string='Repair method'),
        'prevent_suggest':fields.text(string='Prevent suggest'),
        'state':fields.selection([('draft','Wait confirm'),('repairing','Reparing'),('finished','Finished')],string='Status'),
        'create_time':fields.datetime(string='Create time'),
        'repairing_time':fields.datetime(string='Start repairing time'),
        'finished_time':fields.datetime(string='Finish repairing time'),
        'polling_repair_lines':fields.one2many('polling.repair.line','polling_repair_id',string='Repair lines'),
        'remark':fields.text(string='Remark'),
    }
    _defaults = {
        'state':'draft',
        "create_time":lambda self, cr, uid, context:datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
polling_repair()


class polling_repair_line(osv.osv):
    _name = "polling.repair.line"

    _columns = {
        "name":fields.char(string="Description",size=100,required=True),
        "polling_repair_id":fields.many2one("polling.repair","Repair Order",ondelete="cascade",select=True),
        "type":fields.selection([("add","Add"),("remove","Remove")],string="Operation",required=True),
        "product_id":fields.many2one("product.product","Product",required=True),
        "product_qty":fields.integer(string="Product Qty"),
        "operation_time":fields.datetime(string="Operation Time"),
    }
    _defaults = {
        "operation_time":lambda self,cr,uid,context:datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
polling_repair_line()

class polling_maintain_line(osv.osv):
    _name = 'polling.maintain.line'
    _inherit = 'polling.repair.line'
    _columns = {
        "name":fields.char(string="Description",size=100,required=True),
        "polling_maintain_id":fields.many2one("polling.maintain","Maintain Order",ondelete="cascade",select=True),
        "type":fields.selection([("add","Add"),("remove","Remove")],string="Operation",required=True),
        "product_id":fields.many2one("product.product","Product",required=True),
        "product_qty":fields.integer(string="Product Qty"),
        "operation_time":fields.datetime(string="Operation Time"),
    }
    _defaults = {
        "operation_time":lambda self,cr,uid,context:datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
polling_maintain_line()

class polling_maintain(osv.osv):
    _name = "polling.maintain"

    def act_maintaining(self,cr,uid,ids,context=None):
        return self.write(cr,uid,ids,{'state':'maintaining','maintaining_time':datetime.datetime.now()},context=context)

    def act_finish(self,cr,uid,ids,context=None):
        return self.write(cr,uid,ids,{'state':'finished','finished_time':datetime.datetime.now()},context=context)
    
    def on_asset_change(self,cr,uid,ids,asset_id,context=None):
        asset_rep = self.pool.get('polling.asset')
        item = asset_rep.read(cr,uid,asset_id,context=context)
        print 'asset item is %s' % item
        return {
            'value':{
                'category_id':item['category_id'] and item['category_id'][0],
                'install_building':item['install_building_id'] and item['install_building_id'][0],
                'specification':item['specification'],
                'asset_code':item['code'],
                'install_building_position':item['install_position_id'] and item['install_position_id'][0],
            }
        }
    
    _columns = {
        "name":fields.char(string="Maintain number",required=True,size=100),
        "asset_id":fields.many2one("polling.asset",string="Asset"),
        'category_id':fields.related('asset_id','category_id',type='many2one',relation='polling.assettemplatecategory',string='Category'),
        "install_building":fields.related("asset_id","install_building_id",type="many2one",relation="polling.building",string="Building"),
        "install_building_position":fields.related("asset_id",'install_position_id',type='many2one',relation='polling.building.position',string='Position'),
        'asset_code':fields.related('asset_id','code',type='char',string='Asset Code'),
        'asset_specification':fields.related('asset_id','specification',type='char',string='Specification'),
        'maintain_man':fields.many2one('hr.employee',string='Repair man'),
        'maintain_date':fields.datetime(string='Maintain date'),
        'maintain_time':fields.integer(string='Maitain time'),
        'maintain_reason':fields.text(string='Maintain reason'),
        'maintain_method':fields.text(string='Maintain method'),
        'state':fields.selection([('draft','Wait confirm'),('maintaining','Reparing'),('finished','Finished')],string='Status'),
        'create_time':fields.datetime(string='Create time'),
        'maintaining_time':fields.datetime(string='Start maintain time'),
        'finished_time':fields.datetime(string='Finish maintain time'),
        'polling_maintain_lines':fields.one2many('polling.maintain.line','polling_maintain_id',string='Maintain lines'),
        'remark':fields.text(string='Remark'),
    }
    _defaults = {
        'state':'draft',
        "create_time":lambda self, cr, uid, context:datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
polling_maintain()

###手动巡查功能区###
class polling_parol_frequent_record(osv.osv):
    _name = 'polling.parol.frequent.record'
    _columns = {
        'name':fields.datetime(string='Parol time'),
        'frequent_id':fields.many2one('polling.parol.frequent',string='Frequent'),
        'task_id':fields.many2one('polling.parol.task',string='Task'),
        'path_id':fields.many2one('polling.parol.path',string='Path'),
        'point_id':fields.many2one('polling.parol.path.point',string='Point'),
        'state':fields.selection([('normal','Normal'),('lost','Lost'),('ordererror','Order error')],string='Status'),
    }
polling_parol_frequent_record()

class polling_parol_frequent(osv.osv):
    _name='polling.parol.frequent'
    _columns = {
        'name':fields.char(string='Name',size=100,required=True),
        'code':fields.char(string='Code',size=100),
        'remark':fields.text(string='Remark'),
        'polling_parol_tasks':fields.one2many('polling.parol.task','polling_parol_frequent_id',string='Tasks'),
        'check_time_type':fields.selection([('byweek','By week'),('bydate','By date')],string='Check date'),
        'polling_parol_frequent_date':fields.one2many('polling.parol.frequent.date','polling_parol_frequent_id',string='Dates'),
        'polling_parol_frequent_week':fields.one2many('polling.parol.frequent.week','polling_parol_frequent_id',string='Weeks'),
    }
polling_parol_frequent()

class polling_parol_frequent_date(osv.osv):
    _name = 'polling.parol.frequent.date'
    _columns = {
        'name':fields.date(string='Date'),
        'polling_parol_frequent_id':fields.many2one('polling.parol.frequent',string='Frequent'),
    }
polling_parol_frequent_date()

class polling_parol_frequent_week(osv.osv):
    _name = 'polling.parol.frequent.week'
    _columns = {
        'name':fields.selection([('monday','Monday'),('tuesday','Tuesday'),('wednesday','Wednesday'),
                                 ('thursday','Thursday'),('friday','Friday'),('saturday','Saturday'),('sunday','Sunday')],string='Date'),
        'polling_parol_frequent_id':fields.many2one('polling.parol.frequent',string='Frequent'),
    }
polling_parol_frequent_week()

class polling_parol_task(osv.osv):
    _name = 'polling.parol.task'
    _columns = {
        'name':fields.char(string='Task name', size=100,required=True),
        'polling_parol_frequent_id':fields.many2one('polling.parol.frequent',string='Frequent'),
        'start_time':fields.char(string='Start time',size=20),
        'end_time':fields.char(string='End time',size=20),
        'is_current_day':fields.boolean(string='Is Current day'),
        'need_time':fields.integer(string='Need time'),
        'polling_parol_paths':fields.one2many('polling.parol.path','polling_parol_task_id',string='Paths'),
        'remark':fields.text(string='Remark'),
    }
polling_parol_task()

class polling_parol_path(osv.osv):
    _name = 'polling.parol.path'
    _columns = {
        'name':fields.char(string='Name',size=100,required=True),
        'code':fields.char(string='Code',size=100),
        'polling_parol_task_id':fields.many2one('polling.parol.task',string='Task'),
        'points':fields.one2many('polling.parol.path.point','polling_parol_path_id',string='Points'),
        'check_by_order':fields.boolean(string='Need check by order'),
        'remark':fields.text(string='Remark'),
    }
polling_parol_path()

class polling_parol_path_point(osv.osv):
    _name = 'polling.parol.path.point'
    _columns = {
        'name':fields.char(string='Point',size=100,required=True),
        'polling_parol_path_id':fields.many2one('polling.parol.path',string='Path'),
        'building_id':fields.many2one('polling.building',string='Building'),
        'position_id':fields.many2one('polling.building.position',string='Position'),
        'polling_parol_path_point_assets':fields.one2many("polling.parol.path.point.asset","polling_parol_path_point_id",string='Assets'),
        'ordernum':fields.integer(string='Order'),
        'hasinterval':fields.boolean(string='Has interval'),
        'early_interval':fields.integer(string='Early interval'),
        'last_interval':fields.integer(string='Last interval'),
        'remark':fields.text(string='Remark'),
    }
    _defaults = {
        'hasinterval':False,
    }
polling_parol_path_point()

class polling_parol_path_point_asset(osv.osv):
    _name ='polling.parol.path.point.asset'
    _columns = {
        'polling_parol_path_point_id':fields.many2one('polling.parol.path.point',string='Point'),
        'polling_asset_id':fields.many2one('polling.asset',string='Asset'),
    }
polling_parol_path_point_asset()
