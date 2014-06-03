import contextlib
import tarfile
import urllib2

class OVA(object):

	def get_ovf_and_root_vmdk(self, ova):
 		"""Return OVF and root VMDK files

		Currently assuming path and format of OVA file is valid
		e.g) no missing fields
		
		:param ova: file path of OVA file
		"""
		with contextlib.closing(urllib2.urlopen(ova)) as ova_file:
			with tarfile.open(ova_file) as tar:
				found_ovf = False
				found_root_vmdk = False

				for tar_info in tar:
					if tar_info.name.endswith(('ovf')):
						yield tar.extractfile(tar_info)
						found_ovf = True
					if tar_info.name.endswith(('vmdk')):
						yield tar.extractfile(tar_info)
						found_root_vmdk = True

					if found_ovf and found_root_vmdk:
						break

			#finish downloading to avoid extract unnecessary files
			break
