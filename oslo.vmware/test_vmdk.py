from tempfile import NamedTemporaryFile
import unittest
import vmdk

class APITest(unittest.TestCase):
    """Tests for API"""

    def test_get_adapter_type(self):
        api = vmdk.API()
        self.vmdk_test_getFunc(api.get_adapter_type, 'adapter_type')

    def test_get_disk_type(self):
        api = vmdk.API()
        self.vmdk_test_getFunc(api.get_disk_type, 'disk_type')

    def test_get_virtual_size(self):
        api = vmdk.API()
        self.vmdk_test_getFunc(api.get_virtual_size, 'size')

    def vmdk_test_getFunc(self, get_func, param):
        """Create temporary vmdk files and test a get function
           which returns a particular parameter of the files

        The string data of a vmdk file is defined in get_*_vmdk()

        :param get_func: get function to be tested
        :param param: parameter defined in 'summary' of get_*_vmdk(...)
        """
        monolithicSparse_vmdk = self.get_monolithicSparse_vmdk()
        monolithicFlat_vmdk = self.get_monolithicFlat_vmdk()
        streamOptimized_vmdk = self.get_streamOptimized_vmdk()

        with NamedTemporaryFile() as monolithicSparse,\
             NamedTemporaryFile() as monolithicFlat,\
             NamedTemporaryFile() as streamOptimized:

            monolithicSparse.write(monolithicSparse_vmdk['vmdk'])
            monolithicFlat.write(monolithicFlat_vmdk['vmdk'])
            streamOptimized.write(streamOptimized_vmdk['vmdk'])

            monolithicSparse.seek(0)
            monolithicFlat.seek(0)
            streamOptimized.seek(0)

            test_cases = [{'vmdk': monolithicSparse.name,
                           'expected_result':
                                   monolithicSparse_vmdk['summary'][param]},
                          {'vmdk': monolithicFlat.name,
                           'expected_result':
                                   monolithicFlat_vmdk['summary'][param]},
                          {'vmdk': streamOptimized.name,
                           'expected_result':
                                   streamOptimized_vmdk['summary'][param]}]

            for test_case in test_cases:
                ret_value = get_func(test_case['vmdk'])
                self.assertEqual(ret_value, test_case['expected_result'])

    def get_monolithicSparse_vmdk(self):
        """Return string format of monolithicSparse vmdk
           and its corresponding summary as dictionary
           such as adapter_type, disk_type and virtual_size
        """
        monolithicSparse = '\n'.join(['# Disk DescriptorFile',
                                      'version=1',
                                      'CID=fffffffe',
                                      'parentCID=ffffffff',
                                      'createType="monolithicSparse"'
                                      '\n',
                                      '# Extent description',
                                      'RW 18432000 SPARSE "test.vmdk"'
                                      '\n',
                                      '# The Disk Data Base',
                                      '#DDB',
                                      'ddb.virtualHWVersion = "3"',
                                      'ddb.geometry.cylinders = "16383"',
                                      'ddb.geometry.heads = "16"',
                                      'ddb.geometry.sectors = "63"',
                                      'ddb.adapterType = "ide"'])

        summary = {'adapter_type': '"ide"',
                   'disk_type': '"monolithicSparse"',
                   'size': '18432000'}

        return {'vmdk': monolithicSparse, 'summary': summary}

    def get_monolithicFlat_vmdk(self):
        """Return string format of monolithicFlat vmdk
           and its corresponding summary as dictionary
           such as adapter_type, disk_type and virtual_size
        """
        monolithicFlat = '\n'.join(['# Disk DescriptorFile',
                                    'version=1',
                                    'CID=fffffffe',
                                    'parentCID=ffffffff',
                                    'createType="monolithicFlat"'
                                    '\n',
                                    '# Extent description',
                                    'RW 27648000 FLAT "test-flat.vmdk" 0'
                                    '\n',
                                    '# The Disk Data Base',
                                    '#DDB',
                                    'ddb.virtualHWVersion = "3"',
                                    'ddb.geometry.cylinders = "16383"',
                                    'ddb.geometry.heads = "16"',
                                    'ddb.geometry.sectors = "63"',
                                    'ddb.adapterType = "ide"'])

        summary = {'adapter_type': '"ide"',
                   'disk_type': '"monolithicFlat"',
                   'size': '27648000'}

        return {'vmdk': monolithicFlat, 'summary': summary}

    def get_streamOptimized_vmdk(self):
        """Return string format of streamOptimized vmdk
           and its corresponding summary as dictionary
           such as adapter_type, disk_type and virtual_size
        """
        streamOptimized = '\n'.join(['# Disk DescriptorFile',
                                    'version=1',
                                    'encoding="windows-1252"',
                                    'CID=f19b298e',
                                    'parentCID=ffffffff',
                                    'createType="streamOptimized"'
                                    '\n',
                                    '# Extent description',
                                    'RW 16777216 SPARSE "test.vmdk"'
                                    '\n',
                                    '# The Disk Data Base',
                                    '#DDB',
                                    'ddb.geometry.biosSectors = "63"',
                                    'ddb.geometry.biosHeads = "255"',
                                    'ddb.geometry.biosCylinders = "1044"',
                                    'ddb.adapterType = "lsilogic"',
                                    'ddb.geometry.sectors = "63"',
                                    'ddb.geometry.heads = "255"',
                                    'ddb.geometry.cylinders = "1044"',
                                    'ddb.uuid = "60 00 C2 9f 9b b0 9d 17'
                                                '-'
                                                '15 6c 54 9c 40 8d 33 71"',
                                    'ddb.virtualHWVersion = "7"',
                                    'ddb.toolsVersion = "0"'])

        summary = {'adapter_type': '"lsilogic"',
                   'disk_type': '"streamOptimized"',
                   'size': '16777216'}

        return {'vmdk': streamOptimized, 'summary': summary}

if __name__ == "__main__":
    unittest.main()
