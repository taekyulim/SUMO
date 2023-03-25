import numpy as np
import pickle
import random
from xml.etree.ElementTree import Element, SubElement, ElementTree, dump

with open('./route_lambda.pickle', 'rb') as f:
    lambds = pickle.load(f)

def get_traffic_volume(vertex, time):
    """
    vertex : 간선 번호(1~6)
    time : 시작 시간대(1~23)
    """
    lamd = lambds[vertex-1][time-1]
    result = np.random.poisson(lamd, 1)
    return result

def random_gen():
    rand_n1 = random.uniform(0.5, 0.7)
    rand_n2 = random.uniform(0.2, 0.3)
    rand_n3 = 1 - rand_n1 - rand_n2 # [0, 0.3] 범위에서 나옴.
    
    sorted_nums = sorted([rand_n1, rand_n2, rand_n3], reverse=True)
    return sorted_nums[0], sorted_nums[1], sorted_nums[2]

def straight_left_right(route, time):
    straight_coef, left_coef, right_coef = random_gen()
    total_traffic = get_traffic_volume(route, time)
    straight = int(straight_coef*total_traffic)
    left = int(left_coef*total_traffic)
    right = int(right_coef*total_traffic)
    
    return straight, left, right

street = {
    "a" : ["b", "c", "d"] # straight, left, right
}

def make_traffic_volume(node, direction, time):
    st, le, rig = straight_left_right(direction, time)
    straight = list(node.keys())[0] + ' ' + node["a"][0]
    left = list(node.keys())[0] +' '+ node["a"][1]
    right = list(node.keys())[0] +' '+ node["a"][2]
    
    result = {
        straight : st,
        left : le,
        right : rig
    }
    
    return result
# make_traffic_volume(node, 3, 15)
# {'a b': 846, 'a c': 286, 'a d': 255}

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
            
def generate_edge_xml(center, straight, left, right):
    """
    노드들 인풋으로 주면 됨.
    순서대로 기준 노드, 직진 코스 노드, 좌회전, 우회전 코스 만드는 노드
    """
    root = Element("edges")
    st_route = Element("edge")
    st_route.set("from", center)
    st_route.set("to", straight)
    st_route.set("id", "straight")
    st_route.set("type", "normal")
    root.append(st_route)
    
    le_route = Element("edge")
    le_route.set("from", center)
    le_route.set("to", left)
    le_route.set("id", "left")
    le_route.set("type", "normal")
    root.append(le_route)
    
    ri_route = Element("edge")
    ri_route.set("from", center)
    ri_route.set("to", right)
    ri_route.set("id", "right")
    ri_route.set("type", "normal")
    root.append(ri_route)
    
    indent(root)
    tree = ElementTree(root)
    file_name = f"{center}.edg.xml"
    with open(file_name, "wb") as file:
        tree.write(file, encoding="utf-8", xml_declaration=True)
        
def generate_route_tag():
    

# def main():
#     parser = argparse.ArgumentParser(description="Get Traffic Volume in specific route and time")
#     parser.add_argument('vertex', type=int, help='Vertex number 1~6')
#     parser.add_argument('time', type=int, help = "Specific Time 1~23")
    
#     args = parser.parse_args()
    
#     result = get_traffic_volume(args.vertex, args.time)
#     print(result)
    
    
# if __name__ == "__main__":
#     a, b, c = left_straight_right(3, 16)
#     print(a, b, c)