#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "beautifulsoup4>=4.9.0",
#     "haversine>=2.8.0",
#     "networkx>=3.0",
# ]
# ///
"""
World Courier Shortest Path Finder

This script finds the shortest path between two cities using:
1. HTML files for direct flight connections and city coordinates
2. Haversine distance calculation for real-world distances
3. NetworkX Dijkstra's algorithm for shortest path finding

The script:
- Parses city coordinates from city-coordinates.html
- Parses direct flight connections from from-to.html
- Builds a weighted graph with Haversine distances
- Uses Dijkstra's algorithm to find the shortest path

Author: World Courier Operations
Date: 2025-07-18
"""

import re
from typing import Dict, List, Tuple, Optional
from bs4 import BeautifulSoup
from haversine import haversine, Unit
import networkx as nx

def parse_city_coordinates(html_file: str) -> Dict[str, Tuple[float, float]]:
    """
    Parse city coordinates from HTML table.
    
    Args:
        html_file: Path to the HTML file containing city coordinates
        
    Returns:
        Dictionary mapping city names to (latitude, longitude) tuples
    """
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    coordinates = {}
    
    # Find all table rows
    rows = soup.find_all('tr')
    
    for row in rows:
        cells = row.find_all('td')
        if len(cells) >= 3:
            city = cells[0].get_text(strip=True)
            try:
                lat = float(cells[1].get_text(strip=True))
                lon = float(cells[2].get_text(strip=True))
                coordinates[city] = (lat, lon)
            except ValueError:
                continue
    
    return coordinates

def parse_flight_connections(html_file: str) -> List[Tuple[str, str]]:
    """
    Parse direct flight connections from HTML table.
    
    Args:
        html_file: Path to the HTML file containing flight connections
        
    Returns:
        List of (from_city, to_city) tuples representing direct flights
    """
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    connections = []
    
    # Find all table rows
    rows = soup.find_all('tr')
    
    for row in rows:
        cells = row.find_all('td')
        if len(cells) >= 2:
            from_city = cells[0].get_text(strip=True)
            to_city = cells[1].get_text(strip=True)
            if from_city and to_city:
                connections.append((from_city, to_city))
    
    return connections

def calculate_haversine_distance(coord1: Tuple[float, float], 
                               coord2: Tuple[float, float]) -> float:
    """
    Calculate the Haversine distance between two coordinates.
    
    Args:
        coord1: (latitude, longitude) of first point
        coord2: (latitude, longitude) of second point
        
    Returns:
        Distance in kilometers
    """
    return haversine(coord1, coord2, unit=Unit.KILOMETERS)

def build_flight_graph(coordinates: Dict[str, Tuple[float, float]], 
                      connections: List[Tuple[str, str]]) -> nx.Graph:
    """
    Build a weighted graph of flight connections.
    
    Args:
        coordinates: Dictionary of city coordinates
        connections: List of direct flight connections
        
    Returns:
        NetworkX graph with edge weights as Haversine distances
    """
    G = nx.Graph()
    
    # Add nodes for all cities with coordinates
    for city in coordinates:
        G.add_node(city)
    
    # Add edges for direct connections with Haversine distances as weights
    for from_city, to_city in connections:
        if from_city in coordinates and to_city in coordinates:
            distance = calculate_haversine_distance(
                coordinates[from_city], 
                coordinates[to_city]
            )
            G.add_edge(from_city, to_city, weight=distance)
    
    return G

def find_shortest_path(graph: nx.Graph, start: str, end: str) -> Tuple[List[str], float]:
    """
    Find the shortest path between two cities using Dijkstra's algorithm.
    
    Args:
        graph: NetworkX graph with weighted edges
        start: Starting city name
        end: Destination city name
        
    Returns:
        Tuple of (path as list of cities, total distance)
    """
    try:
        path = nx.shortest_path(graph, start, end, weight='weight')
        distance = nx.shortest_path_length(graph, start, end, weight='weight')
        return path, distance
    except nx.NetworkXNoPath:
        return [], float('inf')

def main():
    """
    Main function to find the shortest path from Chicago to Amsterdam.
    """
    start_city = "Chicago"
    end_city = "Amsterdam"
    
    print("World Courier Shortest Path Finder")
    print("=" * 40)
    print(f"Finding shortest path from {start_city} to {end_city}")
    
    # Parse city coordinates
    print("\\nParsing city coordinates...")
    coordinates = parse_city_coordinates('city-coordinates.html')
    print(f"Loaded coordinates for {len(coordinates)} cities")
    
    # Parse flight connections
    print("\\nParsing flight connections...")
    connections = parse_flight_connections('from-to.html')
    print(f"Loaded {len(connections)} direct flight connections")
    
    # Check if start and end cities exist
    if start_city not in coordinates:
        print(f"Error: {start_city} not found in coordinates")
        return
    if end_city not in coordinates:
        print(f"Error: {end_city} not found in coordinates")
        return
    
    print(f"\\n{start_city} coordinates: {coordinates[start_city]}")
    print(f"{end_city} coordinates: {coordinates[end_city]}")
    
    # Build the flight graph
    print("\\nBuilding flight network graph...")
    graph = build_flight_graph(coordinates, connections)
    print(f"Graph has {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges")
    
    # Find shortest path
    print("\\nFinding shortest path using Dijkstra's algorithm...")
    path, total_distance = find_shortest_path(graph, start_city, end_city)
    
    if not path:
        print(f"No path found between {start_city} and {end_city}")
        return
    
    print(f"\\nShortest path found!")
    print(f"Total distance: {total_distance:.2f} km")
    print(f"Number of stops: {len(path) - 1}")
    
    print("\\nPath details:")
    for i in range(len(path) - 1):
        from_city = path[i]
        to_city = path[i + 1]
        segment_distance = calculate_haversine_distance(
            coordinates[from_city], 
            coordinates[to_city]
        )
        print(f"  {i+1}. {from_city} → {to_city}: {segment_distance:.2f} km")
    
    # Output the final answer
    result = ','.join(path)
    print(f"\\nFinal Answer: {result}")
    
    return result

if __name__ == "__main__":
    main()
