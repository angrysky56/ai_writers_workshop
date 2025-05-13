"""
Knowledge Graph Manager for AI Writers Workshop

Provides integration with graph databases for advanced narrative analysis.
"""

import logging
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Union

logger = logging.getLogger("ai_writers_workshop.knowledge_graph")

class KnowledgeGraphManager:
    """
    Manages interactions with a knowledge graph for narrative analysis.
    
    This implementation provides a file-based fallback when Neo4j is not available.
    """
    
    def __init__(self, base_dir: Union[str, Path] = "output"):
        """
        Initialize the knowledge graph manager.
        
        Args:
            base_dir: Base directory for fallback file storage
        """
        self.base_dir = Path(base_dir)
        self.graph_dir = self.base_dir / "knowledge_graph"
        self.graph_dir.mkdir(exist_ok=True, parents=True)
        
        # Initialize Neo4j client if available
        self.neo4j_client = None
        try:
            # Import optional Neo4j dependencies
            from neo4j import GraphDatabase
            import os
            
            # Try to connect to Neo4j if credentials are provided
            neo4j_uri = os.environ.get("NEO4J_URI")
            neo4j_user = os.environ.get("NEO4J_USER")
            neo4j_password = os.environ.get("NEO4J_PASSWORD")
            
            if neo4j_uri and neo4j_user and neo4j_password:
                self.neo4j_client = GraphDatabase.driver(
                    neo4j_uri, auth=(neo4j_user, neo4j_password)
                )
                logger.info("Successfully connected to Neo4j database")
            else:
                logger.info("Neo4j credentials not found, using file-based fallback")
        except ImportError:
            logger.info("Neo4j driver not installed, using file-based fallback")
        except Exception as e:
            logger.error(f"Error connecting to Neo4j: {e}")
    
    def create_entity(self, entity_type: str, entity_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new entity in the knowledge graph.
        
        Args:
            entity_type: Type of entity (character, location, concept, etc.)
            entity_data: Entity data
            
        Returns:
            Dictionary with entity information
        """
        entity_id = entity_data.get("id", entity_data.get("name", "").lower().replace(" ", "_"))
        
        if self.neo4j_client:
            try:
                # Use Neo4j to create entity
                with self.neo4j_client.session() as session:
                    # Convert entity data to properties
                    properties = {k: v for k, v in entity_data.items() 
                                if not isinstance(v, (dict, list))}
                    
                    # Create node query
                    query = (
                        f"CREATE (e:{entity_type} {{id: $id, {', '.join([f'{k}: ${k}' for k in properties.keys()])}}}) "
                        f"RETURN e"
                    )
                    
                    # Execute query
                    result = session.run(query, id=entity_id, **properties)
                    created_node = result.single()
                    
                    if created_node:
                        return {**entity_data, "id": entity_id, "stored_in": "neo4j"}
            except Exception as e:
                logger.error(f"Error creating entity in Neo4j: {e}")
        
        # Fallback to file-based storage
        entity_file = self.graph_dir / f"{entity_type}_{entity_id}.json"
        with open(entity_file, "w") as f:
            json.dump(entity_data, f, indent=2)
        
        return {**entity_data, "id": entity_id, "stored_in": "file"}
    
    def create_relation(self, from_entity: str, relation_type: str, to_entity: str, 
                       properties: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a relation between entities in the knowledge graph.
        
        Args:
            from_entity: ID of the source entity
            relation_type: Type of relation
            to_entity: ID of the target entity
            properties: Optional relation properties
            
        Returns:
            Dictionary with relation information
        """
        properties = properties or {}
        
        if self.neo4j_client:
            try:
                # Use Neo4j to create relation
                with self.neo4j_client.session() as session:
                    # Create relation query
                    property_clause = ""
                    if properties:
                        property_clause = " {" + ", ".join([f"{k}: ${k}" for k in properties.keys()]) + "}"
                    
                    query = (
                        f"MATCH (a), (b) "
                        f"WHERE a.id = $from_id AND b.id = $to_id "
                        f"CREATE (a)-[r:{relation_type}{property_clause}]->(b) "
                        f"RETURN type(r) AS type"
                    )
                    
                    # Execute query
                    result = session.run(query, from_id=from_entity, to_id=to_entity, **properties)
                    created_rel = result.single()
                    
                    if created_rel:
                        return {
                            "from": from_entity,
                            "type": relation_type,
                            "to": to_entity,
                            "properties": properties,
                            "stored_in": "neo4j"
                        }
            except Exception as e:
                logger.error(f"Error creating relation in Neo4j: {e}")
        
        # Fallback to file-based storage
        relation_id = f"{from_entity}_{relation_type}_{to_entity}"
        relation_file = self.graph_dir / f"relation_{relation_id}.json"
        
        relation_data = {
            "from": from_entity,
            "type": relation_type,
            "to": to_entity,
            "properties": properties
        }
        
        with open(relation_file, "w") as f:
            json.dump(relation_data, f, indent=2)
        
        return {**relation_data, "stored_in": "file"}
    
    def search_nodes(self, query: str) -> Dict[str, Any]:
        """
        Search for nodes in the knowledge graph.
        
        Args:
            query: Search query string
            
        Returns:
            Dictionary with search results
        """
        results = []
        
        if self.neo4j_client:
            try:
                # Use Neo4j for search
                with self.neo4j_client.session() as session:
                    # Create search query
                    cypher_query = (
                        "MATCH (n) "
                        "WHERE n.name CONTAINS $query OR n.id CONTAINS $query "
                        "OR EXISTS(n.description) AND n.description CONTAINS $query "
                        "RETURN n.id AS id, labels(n) AS types, n AS properties "
                        "LIMIT 10"
                    )
                    
                    # Execute query
                    result = session.run(cypher_query, query=query)
                    
                    # Process results
                    for record in result:
                        results.append({
                            "id": record["id"],
                            "types": record["types"],
                            "properties": dict(record["properties"])
                        })
                    
                    return {"query": query, "results": results, "source": "neo4j"}
            except Exception as e:
                logger.error(f"Error searching in Neo4j: {e}")
        
        # Fallback to file-based search
        for file_path in self.graph_dir.glob("*.json"):
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)
                
                # Check if data matches query
                matches = False
                if isinstance(data, dict):
                    # Check name or id
                    if data.get("name", "").lower().find(query.lower()) >= 0:
                        matches = True
                    elif data.get("id", "").lower().find(query.lower()) >= 0:
                        matches = True
                    # Check description
                    elif data.get("description", "").lower().find(query.lower()) >= 0:
                        matches = True
                
                if matches:
                    # Get entity type from filename
                    parts = file_path.stem.split("_", 1)
                    entity_type = parts[0] if len(parts) > 1 else "unknown"
                    
                    results.append({
                        "id": data.get("id", file_path.stem),
                        "types": [entity_type],
                        "properties": data
                    })
            except Exception as e:
                logger.error(f"Error processing file {file_path}: {e}")
        
        return {"query": query, "results": results, "source": "file"}
    
    def open_nodes(self, names: List[str]) -> Dict[str, Any]:
        """
        Open specific nodes in the knowledge graph by their names.
        
        Args:
            names: List of node names/IDs to retrieve
            
        Returns:
            Dictionary with nodes keyed by name
        """
        nodes = {}
        
        if self.neo4j_client:
            try:
                # Use Neo4j to get nodes
                with self.neo4j_client.session() as session:
                    # Create query
                    query = (
                        "MATCH (n) "
                        "WHERE n.id IN $names OR n.name IN $names "
                        "RETURN n.id AS id, labels(n) AS types, n AS properties"
                    )
                    
                    # Execute query
                    result = session.run(query, names=names)
                    
                    # Process results
                    for record in result:
                        node_id = record["id"]
                        nodes[node_id] = {
                            "id": node_id,
                            "types": record["types"],
                            "properties": dict(record["properties"])
                        }
                    
                    # If all nodes found, return results
                    if len(nodes) == len(names):
                        return {"nodes": nodes, "source": "neo4j"}
            except Exception as e:
                logger.error(f"Error retrieving nodes from Neo4j: {e}")
        
        # Fallback to file-based retrieval or complement missing nodes
        for file_path in self.graph_dir.glob("*.json"):
            try:
                # Skip relation files
                if file_path.stem.startswith("relation_"):
                    continue
                
                # Get entity ID from filename
                parts = file_path.stem.split("_", 1)
                entity_id = parts[1] if len(parts) > 1 else file_path.stem
                
                # Check if this entity is in the requested names
                for name in names:
                    if name == entity_id or name == file_path.stem:
                        # Read file
                        with open(file_path, "r") as f:
                            data = json.load(f)
                        
                        # Get entity type from filename
                        entity_type = parts[0] if len(parts) > 1 else "unknown"
                        
                        # Add to results
                        nodes[name] = {
                            "id": data.get("id", entity_id),
                            "types": [entity_type],
                            "properties": data
                        }
            except Exception as e:
                logger.error(f"Error processing file {file_path}: {e}")
        
        return {"nodes": nodes, "source": "file"}
    
    def read_graph(self) -> Dict[str, Any]:
        """
        Read the entire knowledge graph.
        
        Returns:
            Dictionary with graph data
        """
        nodes = []
        relations = []
        
        if self.neo4j_client:
            try:
                # Use Neo4j to read graph
                with self.neo4j_client.session() as session:
                    # Get nodes
                    node_query = "MATCH (n) RETURN n.id AS id, labels(n) AS types, n AS properties"
                    node_result = session.run(node_query)
                    
                    for record in node_result:
                        nodes.append({
                            "id": record["id"],
                            "types": record["types"],
                            "properties": dict(record["properties"])
                        })
                    
                    # Get relations
                    rel_query = (
                        "MATCH (a)-[r]->(b) "
                        "RETURN a.id AS from, type(r) AS type, b.id AS to, properties(r) AS properties"
                    )
                    rel_result = session.run(rel_query)
                    
                    for record in rel_result:
                        relations.append({
                            "from": record["from"],
                            "type": record["type"],
                            "to": record["to"],
                            "properties": dict(record["properties"])
                        })
                    
                    return {"nodes": nodes, "relations": relations, "source": "neo4j"}
            except Exception as e:
                logger.error(f"Error reading graph from Neo4j: {e}")
        
        # Fallback to file-based reading
        # Read nodes
        for file_path in self.graph_dir.glob("*.json"):
            try:
                # Skip relation files
                if file_path.stem.startswith("relation_"):
                    continue
                
                # Read file
                with open(file_path, "r") as f:
                    data = json.load(f)
                
                # Get entity type from filename
                parts = file_path.stem.split("_", 1)
                entity_type = parts[0] if len(parts) > 1 else "unknown"
                entity_id = parts[1] if len(parts) > 1 else file_path.stem
                
                nodes.append({
                    "id": data.get("id", entity_id),
                    "types": [entity_type],
                    "properties": data
                })
            except Exception as e:
                logger.error(f"Error processing node file {file_path}: {e}")
        
        # Read relations
        for file_path in self.graph_dir.glob("relation_*.json"):
            try:
                # Read file
                with open(file_path, "r") as f:
                    data = json.load(f)
                
                relations.append({
                    "from": data.get("from", ""),
                    "type": data.get("type", ""),
                    "to": data.get("to", ""),
                    "properties": data.get("properties", {})
                })
            except Exception as e:
                logger.error(f"Error processing relation file {file_path}: {e}")
        
        return {"nodes": nodes, "relations": relations, "source": "file"}
