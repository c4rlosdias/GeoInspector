import ifcopenshell
import mathutils
import multiprocessing
import ifcopenshell.util.selector as selector
import bonsai.tool as tool
import bpy
import json

rules = {}
results = {}

def get_tree():
    tree = ifcopenshell.geom.tree()
    model = tool.Ifc.get()
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_WORLD_COORDS, True)            
    iterator = ifcopenshell.geom.iterator(settings, model, multiprocessing.cpu_count())
    if iterator.initialize():
        while True:
            tree.add_element(iterator.get_native())
            if not iterator.next():
                break
    return tree

def get_box(obj, distance, side, decorator_color):
    bb_corners = []
    temp_corners=[]
    corners=[]
    sides = {
        'front':{
            'corners' : [0,1,5,4],
            'vector' : (0,-1,0)
        },
        'back':{
            'corners' : [3,2,6,7],
            'vector' : (0,1,0)
        },
        'right':{
            'corners' : [4,5,6,7],
            'vector' : (1,0,0)
        },
        'left':{
            'corners' : [0,1,2,3],
            'vector' : (-1,0,0)
        },
        'top':{
            'corners' : [1,2,6,5],
            'vector' : (0,0,1)
        },
        'bottom':{
            'corners' : [0,3,7,4],
            'vector' : (0,0,-1)
        },
    }
    
    vector_dist = distance * mathutils.Vector(sides[side]['vector'])
    for corner in obj.bound_box:       
        bb_corners.append(mathutils.Vector(corner))
        
        
    for n in sides[side]['corners']:
        temp_corners.append(bb_corners[n])
        temp_corners.append(bb_corners[n] + vector_dist)


    for corner in temp_corners:       
        corners.append(obj.matrix_world@mathutils.Vector(corner))

    edges = [
            (0, 1, decorator_color),
            (1, 3, decorator_color),
            (3, 2, decorator_color),
            (2, 0, decorator_color),
            (4, 5, decorator_color),
            (5, 7, decorator_color),
            (7, 6, decorator_color),
            (6, 4, decorator_color),
            (0, 6, decorator_color),
            (2, 4, decorator_color),
            (1, 7, decorator_color),
            (3, 5, decorator_color),
    ]

    pontos = [tuple(x) for x in corners]
    
    xs = [p[0] for p in pontos]
    ys = [p[1] for p in pontos]
    zs = [p[2] for p in pontos]
    min_pt = (min(xs), min(ys), min(zs))
    max_pt = (max(xs), max(ys), max(zs))

    return corners, edges, min_pt, max_pt

def search_filter(elements, query):
    model = tool.Ifc.get()
    search = selector.filter_elements(ifc_file=model, elements=elements,query=query)
    return search

def update_rules(context):
    props = context.scene.gei_props
    props.rules.clear()
    # rule2 = {}
    # c = 0
    # for rule in rules:
    #     print(rule)
    #     rule2[c] = rules[rule]
    #     c += 1
    # print(rule2)

    for rule in rules:
        new_item = props.rules.add()
        new_item.id = rule
        new_item.name = rules[rule]['name']
        new_item.description = rules[rule]['description']
        new_item.type = rules[rule]['type']

def update_active_rule(context, id):
    props = context.scene.gei_props
    props.active_rule_index = id
    props.rule_name        = rules[id]['name'] 
    props.rule_description = rules[id]['description']
    props.source_elements  = rules[id]['check']
    props.search_elements  = rules[id]['search']
    props.top_dist         = rules[id]['distances']['top']
    props.bottom_dist      = rules[id]['distances']['bottom'] 
    props.front_dist       = rules[id]['distances']['front'] 
    props.back_dist        = rules[id]['distances']['back'] 
    props.right_dist       = rules[id]['distances']['right']
    props.left_dist        = rules[id]['distances']['left'] 

def add_rule(context):
    props = context.scene.gei_props
    i = len(rules)
    rule = {
        "name"            : 'Unamed',
        "description"     : '',
        "type"            : 'CheckFreeArea',
        "check"           : 'IfcFireSuppressionTerminal',
        "search"          : 'IfcSlab',
        "distances"       : {
            'top'    : 0.0,
            'bottom' : 1.1,
            'front'  : 0.0,
            'back'   : 0.0,
            'right'  : 0.0,
            'left'   : 0.0
        },
    }
    rules[i] = rule    
    update_rules(context)
    props.active_rule_index = i
    props.show_rule = True
    print(rules)

def delete_rule(context, i):
    k = len(rules)-1
    w = 0 if i==0 else i-1
    if i == len(rules) - 1:
        rules.pop(i)
    else:
        for j in range(w, k):
            rules[j]=rules[j+1]
        rules.pop(k)


    if i != 0:
        update_rules(context)
        update_active_rule(context, 0)
    print(rules)

def load_rules(context, dados):    
    props = context.scene.gei_props
    props.rules.clear()
    n = 0
    rules.clear()        
    for dado in dados['rules']:
        rules[n] = dado
        n += 1

    for rule  in rules:
        new_item = props.rules.add()
        new_item.id = rule
        new_item.name = rules[rule]['name']
        new_item.description = rules[rule]['description']
        new_item.type = rules[rule]['type']

def save_rules():    
    dados = [] 
    for rule  in rules:
        values = rules[rule]
        dados.append(values)
    return dados

def clear_rules():
    rules.clear()

def save_rule(context, id):    
    props = context.scene.gei_props
    rules[id]['name'] = props.rule_name 
    rules[id]['description'] = props.rule_description
    rules[id]['check'] = props.source_elements
    rules[id]['search'] = props.search_elements
    rules[id]['distances']['top'] = props.top_dist
    rules[id]['distances']['bottom'] = props.bottom_dist 
    rules[id]['distances']['front'] = props.front_dist 
    rules[id]['distances']['back'] = props.back_dist 
    rules[id]['distances']['right'] = props.right_dist 
    rules[id]['distances']['left'] = props.left_dist 

    update_rules(context)

def check_free_area(color):
    sides = ['front', 'back', 'right', 'left', 'top', 'bottom']
    
    results.clear()
    tree = None
    print(rules)
    model = tool.Ifc.get()
    for rule in rules:
        print(f'initializing rule {rule}...')
        source_query = rules[rule]['check']
        search_query = rules[rule]['search']            
        distances = rules[rule]['distances']        
        elements = selector.filter_elements(ifc_file=model, query=source_query)    
        res_elements = {}    
        for element in elements:
            obj = tool.Ifc.get_object_by_identifier(element.id())        
            if obj:
                print('verify if tree exists...')
                if not tree:
                    print('creating tree...')
                    tree = get_tree()
                    print('tree created')
                else:
                    print('tree exist')
                components = {}
                for side in distances:
                    if distances[side] > 0:
                        corners, edges, minpt, maxpt = get_box(obj, distances[side], side, color)
                        print(f'find elements for {side}...')
                        elements2 = tree.select_box((minpt,maxpt), completely_within=True)
                        print('filtering...')
                        elements2 = search_filter(elements2, search_query)
                        components[side] = list(elements2)
            res_elements[element.id()]=components
        print(f'checking rule {rule} done!')
        results[rule] = res_elements

def _check_free_area(rule, source_query, search_query, color, distances ):
    sides = ['front', 'back', 'right', 'left', 'top', 'bottom']
    components = {}
    tree = None
    print(f'initializing rule {rule}...')
    elements = search_filter(None, source_query)
    for element in elements:
        obj = tool.Ifc.get_object_by_identifier(element.id())        
        if obj:
            print('verify if tree exists...')
            if not tree:
                print('creating tree...')
                tree = get_tree()
                print('tree created')
            else:
                print('tree exist')

            for side in sides:
                dist_side = distances[side]
                if dist_side > 0:
                    corners, edges, minpt, maxpt = get_box(obj, dist_side, side, color)
                    print(f'find elements for {side}...')
                    elements = tree.select_box((minpt,maxpt), completely_within=True)
                    print('filtering...')
                    elements = search_filter(elements, search_query)
                    components[side] = elements
            print(f'checking rule {rule} done!')
    return components 

def localview(with_zoom):
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            with bpy.context.temp_override(area=area, region=area.regions[-1]):
                bpy.ops.view3d.localview(frame_selected=with_zoom)
            break




