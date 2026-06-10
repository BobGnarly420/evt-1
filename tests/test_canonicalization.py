from app.services.canonicalization import canonicalize


def test_canonicalization_product_id():
    pid, conf, _ = canonicalize("Sony Corporation", "WH1000XM6", "Black")
    assert pid == "urn:evt:product:sony-wh1000xm6-black"
    assert 0 <= conf <= 1
