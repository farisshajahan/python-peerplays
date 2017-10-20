import unittest
from peerplays import PeerPlays
from peerplays.asset import Asset
from peerplays.instance import set_shared_peerplays_instance
from peerplays.exceptions import AssetDoesNotExistsException


class Testcases(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ppy = PeerPlays(
            nobroadcast=True,
        )
        set_shared_peerplays_instance(self.ppy)

    def test_assert(self):
        with self.assertRaises(AssetDoesNotExistsException):
            Asset("FOObarNonExisting", full=False)

    def test_refresh(self):
        asset = Asset("1.3.0", full=False)
        asset.ensure_full()
        self.assertIn("dynamic_asset_data", asset)
        self.assertIn("flags", asset)
        self.assertIn("permissions", asset)
        self.assertIsInstance(asset["flags"], dict)
        self.assertIsInstance(asset["permissions"], dict)

    def test_properties(self):
        asset = Asset("1.3.0", full=False)
        self.assertIsInstance(asset.symbol, str)
        self.assertIsInstance(asset.precision, int)
        self.assertIsInstance(asset.is_bitasset, bool)
        self.assertIsInstance(asset.permissions, dict)
        self.assertEqual(asset.permissions, asset["permissions"])
        self.assertIsInstance(asset.flags, dict)
        self.assertEqual(asset.flags, asset["flags"])
