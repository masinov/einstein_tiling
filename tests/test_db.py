import json

from einstein.polykites.database import ShapeDB, deserialize_cells, serialize_cells


def test_roundtrip_and_verdicts(tmp_path):
    db = ShapeDB(tmp_path / "t.sqlite")
    cells = ((0, 0, 0), (0, 0, 1))
    sid = db.add_shape(cells)
    assert db.add_shape(cells) == sid  # idempotent
    assert deserialize_cells(serialize_cells(cells)) == cells

    db.record_verdict(sid, "A1-torus", "periodic",
                      certificate={"index": 1}, budget={"k_max": 2})
    db.commit()
    v = db.latest_verdict(sid, "A1-torus")
    assert v["verdict"] == "periodic" and v["certificate"]["index"] == 1
    assert db.verdict_counts("A1-torus") == {"periodic": 1}
    db.close()


def test_read_only_mode_rejects_mutation(tmp_path):
    path = tmp_path / "fixture.sqlite"
    writable = ShapeDB(path)
    writable.add_shape(((0, 0, 0),))
    writable.commit()
    writable.close()

    fixture = ShapeDB(path, read_only=True)
    assert fixture.conn.execute("SELECT COUNT(*) FROM shapes").fetchone() == (1,)
    try:
        fixture.add_shape(((0, 0, 1),))
    except RuntimeError as error:
        assert "read-only" in str(error)
    else:
        raise AssertionError("read-only fixture accepted a mutation")
    fixture.close()
