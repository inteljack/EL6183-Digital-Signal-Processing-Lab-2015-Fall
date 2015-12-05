############################################################
# for testing alternative underlying database mediums; 
# since the browse, submit, and index cgi scripts import
# dbase names from here only, they'll get whatever this 
# module loads; in other words, to switch mediums, simply
# change the import here; eventually we could remove this
# interface module altogether, and load the best medium's
# module directly, but the best may vary by use patterns;
############################################################

#
# one directory per dbase, one flat pickle file per submit
#

from dbfiles import DbaseErrata, DbaseComment


#
# one shelve per dbase, one key per submit, with mutex update locks
#

# from dbshelve import DbaseErrata, DbaseComment 

