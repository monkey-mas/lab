class API(object):

	def get_adapter_type(self, vmdk):
	    """Return adapater type of a vmdk file of type string

	    :param vmdk: file path of vmdk file

        Currently assuming format of vmdk is valid
        e.g) no missing fields
	    """
	    with open(vmdk, 'r') as f:
	        for line in f:
	            info = line.split()

	            if info == []:
	                continue
	            if info[0] == 'ddb.adapterType':
	                return info[2]

	def get_disk_type(self, vmdk):
	    """Return disk type of a vmdk file of type string

	    :param vmdk: file path of vmdk file

        Currently assuming format of vmdk is valid
        e.g) no missing fields
	    """
	    with open(vmdk, 'r') as f:
	        for line in f:
	            info = line.split('=')

	            if info == []:
	                continue
	            if info[0] == 'createType':
	            	createType_without_newline = info[1][:-1]
	                return createType_without_newline

	def get_virtual_size(self, vmdk):
	    """Return virtual size of a vmdk file of type string

	    :param vmdk: file path of vmdk file

        Currently assuming format of vmdk is valid
        e.g) no missing fields
	    """
	    with open(vmdk, 'r') as f:
	        for line in f:
	            if line == '# Extent description\n':
	                # description format => '<accesstype>[space]<size>[space]' 
	                description = f.next()
	                size        = description.split()[1]
	                return size
