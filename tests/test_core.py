import unittest
from core import footprint, in_bound, overlap, total_weight, is_valid, objective

class TestFootPrint(unittest.TestCase):
    def setUp(self):
        self.vehicle = {"width":  3, "length": 4}

    def test_horizontal_di_origin(self):
        placement = {"x": 0, "y": 0, "orientation": "H"}
        hasil = footprint(self.vehicle, placement)
        self.assertEqual(hasil, (0,0,3,4))

    def test_vertikal_di_origin(self):
        placement = {"x": 0, "y": 0, "orientation": "V"}
        hasil = footprint(self.vehicle, placement)
        self.assertEqual(hasil, (0,0,4,3))

    def test_horizontal_dengan_offset(self):
        placement = {"x": 5, "y": 2, "orientation": "H"}
        hasil = footprint(self.vehicle, placement)
        self.assertEqual(hasil, (5,2,8,6))

    def test_vertikal_dengan_offset(self):
        placement = {"x": 5, "y": 2, "orientation": "V"}
        hasil = footprint(self.vehicle, placement)
        self.assertEqual(hasil, (5,2,9,5))

    def test_orientasi_tidak_dikenal(self):
        placement = {"x": 0, "y": 0, "orientation": "X"}
        with self.assertRaises(ValueError):
            footprint(self.vehicle, placement)

    def test_huruf_kecil_ditolak(self):
        placement = {"x": 0, "y": 0, "orientation": "h"}
        with self.assertRaises(ValueError):
            footprint(self.vehicle, placement)

class TestInBound(unittest.TestCase):
    def setUp(self):
        self.ship = {"width": 10, "length": 20}

    def test_pojok_kiri_atas(self):
        box = (0,0,3,4)
        hasil = in_bound(box, self.ship)
        self.assertTrue(hasil)
    def test_menempel_tepi_kanan(self):
        box = (7,0,10,4)
        hasil = in_bound(box, self.ship)
        self.assertTrue(hasil)
    def test_menempel_tepi_bawah(self):
        box = (0,16,3,20)
        hasil = in_bound(box, self.ship)
        self.assertTrue(hasil)
    def test_keluar_kanan_satu_sel(self):
        box = (8,0,11,4)
        hasil = in_bound(box, self.ship)
        self.assertFalse(hasil)
    def test_x_negatif(self):
        box = (-1,0,2,4)
        hasil = in_bound(box, self.ship)
        self.assertFalse(hasil)
    def test_lebih_lebar_dari_geladak(self):
        box = (0,0,11,4)
        hasil = in_bound(box, self.ship)
        self.assertFalse(hasil)

class TestOverlap(unittest.TestCase):

    def test_pojok_kiri_atas(self):
        box1 = (0,0,3,4)
        box2 = (1,1,4,5)
        hasil = overlap(box1, box2)
        self.assertTrue(hasil)

    def test_tidak_beririsan(self):
        box1 = (0,0,3,4)
        box2 = (4,5,7,9)
        hasil = overlap(box1, box2)
        self.assertFalse(hasil)

class TestTotalWeight(unittest.TestCase):
    def setUp(self):
        self.problem = {
            "vehicles": [
                {"weight": 10, "fee": 5},
                {"weight": 20, "fee": 10}
            ],
            "ship": {"max_capacity": 30}
        }
        self.state = [
            {"location": 0},
            {"location": 0}
        ]

    def test_total_weight(self):
        hasil = total_weight(self.state, self.problem)
        self.assertEqual(hasil, 30)

class TestIsValid(unittest.TestCase):
    def setUp(self):
        self.problem = {
            "vehicles": [
                {"weight": 10, "fee": 5, "width": 3, "length": 4},
                {"weight": 20, "fee": 10, "width": 2, "length": 5}
            ],
            "ship": {"max_capacity": 30, "width": 10, "length": 20}
        }
        self.state = [
            {"location": 0, "x": 0, "y": 0, "orientation": "H"},
            {"location": 0, "x": 4, "y": 0, "orientation": "H"}
        ]

    def test_is_valid(self):
        hasil = is_valid(self.state, self.problem)
        self.assertTrue(hasil)

    def test_overweight(self):
        self.problem["ship"]["max_capacity"] = 25
        hasil = is_valid(self.state, self.problem)
        self.assertFalse(hasil)

    def test_out_of_bounds(self):
        self.state[1]["x"] = 9
        hasil = is_valid(self.state, self.problem)
        self.assertFalse(hasil)

    def test_overlap(self):
        self.state[1]["x"] = 2
        hasil = is_valid(self.state, self.problem)
        self.assertFalse(hasil)

class TestObjective(unittest.TestCase):
    def setUp(self):
        self.problem = {
            "vehicles": [
                {"weight": 10, "fee": 5},
                {"weight": 20, "fee": 10}
            ],
            "ship": {"max_capacity": 30}
        }
        self.state = [
            {"location": 0},
            {"location": 0}
        ]

    def test_objective(self):
        hasil = objective(self.state, self.problem)
        self.assertEqual(hasil, 15)

    def test_semua_di_luar(self):
        self.state[0]["location"] = -1
        self.state[1]["location"] = -1
        hasil = objective(self.state, self.problem)
        self.assertEqual(hasil, 0)

    def test_hanya_kendaraan_kedua(self):
        self.state[0]["location"] = -1
        self.state[1]["location"] = 0
        hasil = objective(self.state, self.problem)
        self.assertEqual(hasil, 10)

if __name__ == "__main__":
    unittest.main()