import library.files as files
import settings.settings as settings

#lets compare a bucket in s3 with a bucket in GC
f = files.syncnow('GC',settings.gc_bucket,settings.gc_secrets_file,'S3',settings.s3_bucket)
file_list1 = f.get_files_list('GC')

file_list2 = f.get_files_list('S3')

file_diffs = f.compare_files_lists(file_list1,file_list2)
if len(file_diffs) > 0:

    sync_changes = f.sync_files('GC','S3',file_diffs,file_list1,file_list2)
    print('Sync finished')
else:
    print('Everything is synchronised, no data to transfer')

