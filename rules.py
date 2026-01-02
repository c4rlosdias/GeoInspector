import bpy
import bonsai.tool as tool

rules = {}
results = {}



def search_filter(elements, query):
    model = tool.Ifc.get()
    search = selector.filter_elements(ifc_file=model, elements=elements,query=query)
    return search



def load(self):
        operators.rules = {
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


