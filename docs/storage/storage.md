So, we need a place to store Objects and their files. We has StorageItem class and Storage for listing them.

We have StorageUnit to store files and DBAdapter.

DBAdapter represents any type of db connection. By default it uses SQL adapter. Every adapter must implement object flushing, queries and linking
