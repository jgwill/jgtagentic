from jgtagentic.fdb_data_analyzer import FDBDataAnalyzer


def test_get_last_two_bars():
    analyzer = FDBDataAnalyzer()
    completed, current = analyzer.get_last_two_bars("EUR-USD", "H1")
    assert completed["Date"] <= current["Date"]


def test_analyze_latest():
    analyzer = FDBDataAnalyzer()
    result = analyzer.analyze_latest("EUR-USD", "H1")
    assert "fdb" in result
    assert result["instrument"] == "EUR-USD"
