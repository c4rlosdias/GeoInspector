import ifcopenshell
import mathutils
import multiprocessing
import ifcopenshell.util.selector as selector
import bonsai.tool as tool
import bpy


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

class Rules():
    rules = {}
    results = {}



    @staticmethod
    def search_filter(elements, query):
        model = tool.Ifc.get()
        search = selector.filter_elements(ifc_file=model, elements=elements,query=query)
        return search



    def load(self):
        self.rules = {
            "rule 1": {
                "type"            : 'CheckFreeArea',
                "search elements" : 'IfcDoor',
                "components"      : 'IfcFurniture',
                "distances"       : {
                    'top'    : 0.0,
                    'bottom' : 0.0,
                    'front'  : 1.0,
                    'back'   : 0.0,
                    'right'  : 0.0,
                    'left'   : 0.0
                },

            }
        }

    def clear(self):
        self.rules = {}

    def check_free_area(self, element, color, query, distances ):
        sides = ['front', 'back', 'right', 'left', 'top', 'bottom']
        components = {}
        obj = tool.Ifc.get_object_by_identifier(element.id())
        self.results = {}
        if obj:
            print('creating tree...')
            tree = get_tree()
            print('tree created')
            for side in sides:
                dist_side = distances[side]
                if dist_side > 0:
                    corners, edges, minpt, maxpt = get_box(obj, dist_side, side, color)
                    print(f'find elements for {side}...')
                    elements = tree.select_box((minpt,maxpt), completely_within=True)
                    print('filtering...')
                    elements = self.search_filter(elements, query)
                    components[side] = elements
            print('checking done!')
            self.results = components




