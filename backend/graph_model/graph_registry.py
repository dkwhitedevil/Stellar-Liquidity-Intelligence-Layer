def validate_graph(G):
    for _, _, data in G.edges(data=True):
        assert "value" in data, f"Edge data missing 'value': {data}"
        assert isinstance(data["value"], float), f"Edge value must be float, got {type(data['value'])}"
