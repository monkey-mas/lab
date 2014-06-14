import contextlib
import mock
import ova
import tarfile
import tempfile
import unittest

class OVATest(unittest.TestCase):
    """Tests for OVA"""

    @mock.patch('httplib.HTTPConnection')
    def test_get_ovf_and_root_vmdk(self, fake_urllib2):
        fake_url = 'https://*/fake.ova'
        test_data = self.get_ova_content()
        ret_data = None

        with contextlib.nested(tempfile.NamedTemporaryFile(),
                               tempfile.NamedTemporaryFile(),
                               tempfile.NamedTemporaryFile()) \
            as (ovf, vmdk, ova_file):
                #create temporary tar file containing OVF and VMDK files
                ovf.write(test_data['ovf'])
                vmdk.write(test_data['vmdk'])

                ovf.seek(0)
                vmdk.seek(0)

                with tarfile.open(fileobj=ova_file, mode='w:') as f:
                     f.add(ovf.name, 'fake.ovf')
                     f.add(vmdk.name, 'fake.vmdk')

                ova_file.seek(0)

                #set up urllib2 mock
                fake_urllib2.urlopen = mock.Mock()
                fake_urllib2.urlopen.return_value = ova_file
                ova.urllib2.urlopen = fake_urllib2.urlopen

                ova_obj = ova.OVA()
                ret_data = ova_obj.get_ovf_and_root_vmdk(fake_url)

        for key in ret_data.keys():
            ret_value = ret_data[key]
            exp_value = test_data[key]
            self.assertEqual(ret_value, exp_value)

    def get_ova_content(self):
        return {'ovf': 'fake_ovf', 'vmdk': 'fake_vmdk'}

if __name__ == '__main__':
    unittest.main()