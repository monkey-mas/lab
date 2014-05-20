import unittest
import vmdk

class APITest(unittest.TestCase):
    """Tests for API"""

    def test_get_adapter_type(self):
        api = vmdk.API()
        test_cases = [{'vmdk': 'monosparse.txt',
                       'adapter_type': '"ide"'},
                      {'vmdk': 'monoflat.txt',
                       'adapter_type': '"ide"'},
                      {'vmdk': 'streamOptimized.txt',
                       'adapter_type': '"lsilogic"'}]

        for test_case in test_cases:
            adapter_type = api.get_adapter_type(test_case['vmdk'])
            self.assertEqual(adapter_type, test_case['adapter_type'])

    def test_get_disk_type(self):
        api = vmdk.API()
        test_cases = [{'vmdk': 'monosparse.txt',
                       'disk_type': '"monolithicSparse"'},
                      {'vmdk': 'monoflat.txt',
                       'disk_type': '"monolithicFlat"'},
                      {'vmdk': 'streamOptimized.txt',
                       'disk_type': '"streamOptimized"'}]

        for test_case in test_cases:
            disk_type = api.get_disk_type(test_case['vmdk'])
            self.assertEqual(disk_type, test_case['disk_type'])

    def test_get_virtual_size(self):
        api = vmdk.API()
        test_cases = [{'vmdk': 'monosparse.txt',
                       'size': '18432000'},
                      {'vmdk': 'monoflat.txt',
                       'size': '27648000'},
                      {'vmdk': 'streamOptimized.txt',
                       'size': '16777216'}]

        for test_case in test_cases:
            virtual_size = api.get_virtual_size(test_case['vmdk'])
            self.assertEqual(virtual_size, test_case['size'])

if __name__ == "__main__":
    unittest.main()
