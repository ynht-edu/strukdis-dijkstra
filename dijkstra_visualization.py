import streamlit as st
import networkx as nx
from pyvis.network import Network
import ast

class DijkstraVisualizer:
    def __init__(self):
        self.G = nx.Graph()
        self.node_colors = {}
        self.steps = []
        self.current_step = 0
        self.node_positions = {}  # Store node positions

    def add_nodes_from_list(self, nodes):
        for node in nodes:
            self.G.add_node(node)
            self.node_colors[node] = '#97C2FC'
        return True

    def add_edges_from_list(self, edges):
        valid_edges = []
        for from_node, to_node, weight in edges:
            if from_node in self.G.nodes and to_node in self.G.nodes:
                self.G.add_edge(from_node, to_node, weight=weight)
                valid_edges.append((from_node, to_node, weight))
        return valid_edges

    def initialize_positions(self):
        # Only initialize positions if they haven't been set yet
        if not self.node_positions:
            # Use networkx to generate initial positions
            pos = nx.spring_layout(self.G)
            
            # Convert networkx positions to the format we need
            for node, position in pos.items():
                self.node_positions[node] = {
                    'x': float(position[0]) * 500,  # Scale the positions
                    'y': float(position[1]) * 500
                }

    def dijkstra(self, start_node):
        # Initialize positions before running Dijkstra
        self.initialize_positions()
        
        # Reset colors
        for node in self.G.nodes:
            self.node_colors[node] = '#97C2FC'

        # Run Dijkstra
        self.steps = []
        distances = {node: float('inf') for node in self.G.nodes}
        distances[start_node] = 0
        unvisited = set(self.G.nodes)
        previous = {node: None for node in self.G.nodes}

        while unvisited:
            current_state = {
                'visited': set(self.G.nodes) - unvisited,
                'current_node': None,
                'distances': distances.copy(),
                'previous': previous.copy()
            }

            current_node = min(unvisited, key=lambda node: distances[node])
            current_state['current_node'] = current_node
            self.steps.append(current_state)

            unvisited.remove(current_node)

            for neighbor in self.G.neighbors(current_node):
                if neighbor in unvisited:
                    tentative_distance = distances[current_node] + self.G[current_node][neighbor]['weight']
                    if tentative_distance < distances[neighbor]:
                        distances[neighbor] = tentative_distance
                        previous[neighbor] = current_node

        self.steps.append({
            'visited': set(self.G.nodes),
            'current_node': None,
            'distances': distances,
            'previous': previous
        })

    def get_path_to_node(self, node, previous):
        path = []
        current = node
        while current is not None:
            path.append(current)
            current = previous[current]
        return list(reversed(path))

    def visualize_step(self, step_index):
        net = Network(height="500px", width="100%", bgcolor="#ffffff")
        net.toggle_physics(False)  # Disable physics simulation
        
        step = self.steps[step_index]
        for node in self.G.nodes:
            color = '#FF6B6B' if node == step['current_node'] else \
                    '#2ECC71' if node in step['visited'] else '#97C2FC'
            
            distance = step['distances'][node]
            previous = step['previous'][node]
            label = f"{node}\n(D: {distance if distance != float('inf') else '∞'})"
            
            # Use stored position for the node
            position = self.node_positions.get(node, {})
            net.add_node(
                node, 
                label=label, 
                color=color, 
                title=label,
                x=position.get('x', 0),
                y=position.get('y', 0),
                physics=False  # Disable physics for individual nodes
            )

        for (u, v, d) in self.G.edges(data=True):
            net.add_edge(u, v, label=str(d['weight']))

        net.save_graph("temp_dijkstra_graph.html")
        with open("temp_dijkstra_graph.html", 'r') as f:
            return f.read()

def parse_nodes(node_input):
    try:
        nodes = [node.strip() for node in node_input.split(',')]
        return [node for node in nodes if node]
    except:
        return None

def parse_edges(edge_input):
    try:
        edges = ast.literal_eval(edge_input)
        if isinstance(edges, list):
            valid_edges = []
            for edge in edges:
                if isinstance(edge, (list, tuple)) and len(edge) == 3:
                    from_node, to_node, weight = edge
                    try:
                        weight = float(weight)
                        valid_edges.append((from_node, to_node, weight))
                    except ValueError:
                        continue
            return valid_edges
    except:
        pass
    return None

def main():
    st.title("Interactive Dijkstra Algorithm Visualization")
    
    if 'visualizer' not in st.session_state:
        st.session_state.visualizer = DijkstraVisualizer()
    
    viz = st.session_state.visualizer

    tab1, tab2, tab3 = st.tabs(["Add Nodes & Edges", "View Graph", "Run Dijkstra"])

    # Add Nodes and Edges Tab
    with tab1:
        st.subheader("Add Nodes")
        st.write("Enter nodes separated by commas (e.g., A, B, C, D)")
        node_input = st.text_input("Nodes")
        
        st.subheader("Add Edges")
        st.write("Enter edges as list of tuples: [(from_node, to_node, weight), ...]")
        st.write("Example: [('A', 'B', 4), ('B', 'C', 3), ('A', 'C', 6)]")
        edge_input = st.text_area("Edges")

        if st.button("Add to Graph"):
            nodes = parse_nodes(node_input)
            if nodes:
                viz.add_nodes_from_list(nodes)
                st.success(f"Added nodes: {nodes}")
            else:
                st.error("Invalid node format")

            edges = parse_edges(edge_input)
            if edges:
                valid_edges = viz.add_edges_from_list(edges)
                if valid_edges:
                    st.success(f"Added edges: {valid_edges}")
                    # Initialize positions after adding edges
                    viz.initialize_positions()
                else:
                    st.warning("No valid edges added. Make sure nodes exist.")
            else:
                st.error("Invalid edge format")

    # View Graph Tab
    with tab2:
        if not viz.G.nodes:
            st.warning("Create a graph first")
        else:
            st.write("Current Graph:")
            st.write("Nodes:", list(viz.G.nodes))
            st.write("Edges:", [(u, v, d['weight']) for (u, v, d) in viz.G.edges(data=True)])
            
            net = Network(height="500px", width="100%", bgcolor="#ffffff")
            net.toggle_physics(False)  # Disable physics simulation
            
            # Use stored positions for visualization
            for node in viz.G.nodes:
                position = viz.node_positions.get(node, {})
                net.add_node(
                    node,
                    x=position.get('x', 0),
                    y=position.get('y', 0),
                    physics=False
                )
            for (u, v, d) in viz.G.edges(data=True):
                net.add_edge(u, v, label=str(d['weight']))
            
            net.save_graph("temp_graph.html")
            with open("temp_graph.html", 'r') as f:
                st.components.v1.html(f.read(), height=500)

    # Dijkstra Tab
    with tab3:
        if not viz.G.nodes:
            st.warning("Create a graph first")
        else:
            start_node = st.selectbox("Select Start Node", list(viz.G.nodes))
            
            if st.button("Run Dijkstra"):
                viz.dijkstra(start_node)
                st.session_state.current_step = 0

            if hasattr(st.session_state, 'current_step'):
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Previous Step"):
                        st.session_state.current_step = max(0, st.session_state.current_step - 1)
                with col2:
                    if st.button("Next Step"):
                        st.session_state.current_step = min(len(viz.steps) - 1, st.session_state.current_step + 1)

                step_html = viz.visualize_step(st.session_state.current_step)
                st.components.v1.html(step_html, height=500)

                current_step = viz.steps[st.session_state.current_step]
                
                # Display basic information
                st.write(f"Step {st.session_state.current_step}")
                st.write("Visited Nodes:", current_step['visited'])
                st.write("Current Node:", current_step['current_node'] or "None")
                
                # Create a table showing distances and paths
                st.subheader("Shortest Paths Table")
                
                # Create columns for the table
                table_data = []
                for node in viz.G.nodes:
                    distance = current_step['distances'][node]
                    previous = current_step['previous'][node]
                    path = viz.get_path_to_node(node, current_step['previous'])
                    
                    table_data.append({
                        "Node": node,
                        "Distance": distance if distance != float('inf') else '∞',
                        "Previous Node": previous or "None",
                        "Full Path": ' → '.join(path)
                    })
                
                st.table(table_data)

if __name__ == "__main__":
    main()