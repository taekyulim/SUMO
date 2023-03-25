from xml.etree.ElementTree import Element, ElementTree


def create_vertices(grid):
    # np.array 형태의 input
    # edg.xml 만들때 필요함
    vertices = []

    rows, cols = grid.shape
    for i in range(rows):
        for j in range(cols):
            current_cell = grid[i, j]

            # Connect to the right cell
            if j < cols - 1:
                right_cell = grid[i, j + 1]
                vertices.append((current_cell, right_cell))

            # Connect to the bottom cell
            if i < rows - 1:
                bottom_cell = grid[i + 1, j]
                vertices.append((current_cell, bottom_cell))

    return vertices

def calculate_interval_points(total_length, num_intervals):
    # nod.xml 만들때 필요함
    # Calculate the step size between intervals
    step = total_length / num_intervals

    # Initialize the starting point
    start = -total_length / 2

    # Calculate the interval points
    interval_points = [start + i * step for i in range(num_intervals + 1)]

    return interval_points

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
            
def make_node_tag(h, v, x_grid, y_grid):
    attrib = {
        "id" : f'n{v+1}{h+1}',
        "x" : f"{x_grid[h]}",
        "y" : f"{y_grid[v]}",
        "type" : "traffic_light"
    }
    root = Element("node", attrib=attrib)
    return root
            
def make_node_xml(total_width, num_width_interval, total_height, num_height_interval):
    root = Element("nodes")
    x_grid = calculate_interval_points(total_width, num_width_interval)
    y_grid = list(reversed(calculate_interval_points(total_height, num_height_interval)))
    for h in range(len(x_grid)):
        for v in range(len(y_grid)):
            node_tag = make_node_tag(h, v, x_grid, y_grid)
            root.append(node_tag)
    indent(root)
    tree = ElementTree(root)
    file_name = "filab.nod.xml"
    tree.write(file_name, encoding="utf-8", xml_declaration=True)
        
def create_edge_tag(start, end):
    attrib = {
        "from" : start,
        "to" : end,
        "id" : f"{start}to{end}",
        "type": "normal"
    }
    root = Element("edge", attrib=attrib)
    return root
            
def generate_edge_xml(num_width_interval, num_height_interval):
    root = Element("edges")
    nodes_list = [[f"n{i+1}{j+1}" for j in range(num_height_interval)] for i in range(num_width_interval)]
    vertices = create_vertices(nodes_list)
    for vertex in vertices:
        start = vertex[0]
        end = vertex[1]
        edge_tag = create_edge_tag(start, end)
        root.append(edge_tag)
    indent(root)
    tree = ElementTree(root)
    file_name = "filab.edg.xml"
    tree.write(file_name, encoding='utf-8', xml_declaration=True)