from contextlib import closing
from urllib2 import urlopen
#from oslo.vmware import exceptions

class API(object):

    def get_adapter_type(self, vmdk):
        """Return string of adapater type defined in a VMDK file

        Param vmdk is handled properly for both local files and http sources.
        Currently assuming format of VMDK file is valid
        e.g) no missing fields

        :param vmdk: file path of VMDK file
        """
        adapter_type = None

        def extract_adapter_type(file):
            for line in file:
                info = line.split()
                if info == []:
                    continue
                if info[0] == 'ddb.adapterType':
                    #info format => ['ddb.adapterType','=',adapter_type]
                    return info[2]

        if vmdk.startswith(('http:')):
            with closing(urlopen(vmdk)) as page:
                adapter_type = extract_adapter_type(page)
        else:
            with open(vmdk, 'r') as f:
                adapter_type = extract_adapter_type(f)

        if not adapter_type:
            excep_msg = _("Could not extract adapter_type from VMDK file.")
            LOG.error(excep_msg)
            raise exceptions.VimException(excep_msg)

        return adapter_type

    def get_disk_type(self, vmdk):
        """Return string of disk type defined in a VMDK file

        Param vmdk is handled properly for both local files and http sources.
        Currently assuming format of VMDK file is valid
        e.g) no missing fields

        :param vmdk: file path of VMDK file
        """
        disk_type = None

        def extract_disk_type(file):
            for line in file:
                info = line.split('=')

                if info == []:
                    continue
                if info[0] == 'createType':
                    #info format => ['createTyel', disk_type'\n']
                    createType_without_newline = info[1][:-1]
                    return createType_without_newline

        if vmdk.startswith(('http:')):
            with closing(urlopen(vmdk)) as page:
                disk_type = extract_disk_type(page)
        else:
            with open(vmdk, 'r') as f:
                disk_type = extract_disk_type(f)

        if not disk_type:
            excep_msg = _("Could not extract disk_type from VMDK file.")
            LOG.error(excep_msg)
            raise exceptions.VimException(excep_msg)

        return disk_type

    def get_virtual_size(self, vmdk):
        """Return string of virtual size defined in a VMDK file

        Param vmdk is handled properly for both local files and http sources.
        Currently assuming format of VMDK file is valid
        e.g) no missing fields

        :param vmdk: file path of VMDK file
        """
        size = None

        def extract_virtual_size(file):
            for line in file:
                if line == '# Extent description\n':
                    # description format => '<accesstype>[space]<size>[space]' 
                    description = file.next()
                    size        = description.split()[1]
                    return size

        if vmdk.startswith(('http:')):
            with closing(urlopen(vmdk)) as page:
                size = extract_virtual_size(page)
        else:
            with open(vmdk, 'r') as f:
                size = extract_virtual_size(f)

        if not size:
            excep_msg = _("Could not extract virtual size from VMDK file.")
            LOG.error(excep_msg)
            raise exceptions.VimException(excep_msg)

        return size