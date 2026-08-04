from pyvis.network import Network
from storage import store

def build_graph():
    results = store.collection.get(include=["documents", "metadatas"])
    if not results["ids"]:
        print("No mistakes stored yet.")
        return

    unique = {}
    for i, doc in enumerate(results["documents"]):
        if doc not in unique:
            unique[doc] = {
                "metadata": results["metadatas"][i],
                "id": results["ids"][i]
            }

    items = list(unique.items())
    n = len(items)
    print(f"Found {n} unique mistake nodes.")

    if n < 2:
        net = Network(height="600px", width="100%")
        net.add_node(0, label=items[0][0][:50], title=items[0][0], color="#5fb3a3")
        net.show("mistake_map.html", notebook=False)
        return

    net = Network(height="1000px", width="100%", bgcolor="#ffffff", font_color="black")
    net.set_options("""
    var options = {
      "nodes": {
        "shape": "dot",
        "size": 35,
        "font": { "size": 16, "face": "Arial", "strokeWidth": 3, "color": "black" }
      },
      "edges": {
        "width": 6,
        "color": { "color": "#ff8800", "opacity": 1.0, "highlight": "#ff0000" }
      },
      "physics": {
        "enabled": true,
        "stabilization": { "iterations": 250 },
        "repulsion": { "nodeDistance": 350 },
        "springLength": 200
      }
    }
    """)

    node_id_map = {}
    node_texts = {}
    for idx, (dp, data) in enumerate(items):
        label = dp[:40] + "..." if len(dp) > 40 else dp
        net.add_node(idx, label=label, title=dp, color="#5fb3a3")
        node_id_map[data["id"]] = idx
        node_texts[idx] = dp

    edge_count = 0
    for idx, (dp, data) in enumerate(items):
        similar = store.collection.query(
            query_texts=[dp],
            n_results=min(5, n)
        )
        for sid, dist in zip(similar["ids"][0], similar["distances"][0]):
            if sid == data["id"]:
                continue
            if sid in node_id_map:
                target_idx = node_id_map[sid]
                if idx < target_idx:
                    similarity = 1 - dist
                    if similarity > 0.4:
                        # Force thick orange edge
                        net.add_edge(
                            idx, target_idx,
                            color="#ff8800",
                            width=6,
                            value=similarity,
                            title=f"Similarity: {similarity:.2f}"
                        )
                        edge_count += 1

    print(f"\nEdges drawn: {edge_count}")
    print(f"Open 'mistake_map.html' in your browser. Press Ctrl+F5 if you still see an old version.")
    print("The edges are thick orange lines. Drag nodes apart to see them clearly.")

    net.show("mistake_map.html", notebook=False)

if __name__ == "__main__":
    build_graph()