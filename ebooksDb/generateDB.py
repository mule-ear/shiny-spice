#! /usr/bin/env python3

import os, sys, sqlite3, logging, logging.config

def generate_directories_table(baseDir, cur, log):
    # Populate dirs table 
    # CREATE TABLE directories (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR, path VARCHAR, full_path VARCHAR);
    # The idea being that the dir will have its own name, path is the parent, full_path is what I'll add 
    log.info("generating data for directories table")
    cur.execute("DROP TABLE IF EXISTS directories;")
    cur.execute("CREATE TABLE directories (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR, path VARCHAR, full_path VARCHAR);")

    listOfDirs = [x[0] for x in os.walk(baseDir)]

    for i in listOfDirs:
        # insertValues = (i.rsplit('/',1)[1] , i.rsplit('/',1)[0] , i)
        # sqCur1.execute("INSERT INTO directories (name, path, full_path) VALUES(?,?,?)", insertValues)
        cur.execute("INSERT INTO directories (name, path, full_path) VALUES(?,?,?)", (i.rsplit('/',1)[1]+'/' , i.rsplit('/',1)[0]+'/' , i+'/'))
            
def create_tables_for_books(cur, log):
    log.info("Creating Tables")
    # CREATE the tables needed for books
    #

    cur.execute("DROP TABLE IF EXISTS books;")
    cur.execute("DROP TABLE IF EXISTS files;")
    cur.execute("DROP TABLE IF EXISTS types;")
    cur.execute("DROP TABLE IF EXISTS authors;")
    cur.execute("DROP TABLE IF EXISTS tags;")
    cur.execute("DROP TABLE IF EXISTS categories;")
    cur.execute("DROP TABLE IF EXISTS books_tags;")
    cur.execute("DROP TABLE IF EXISTS books_categories;")

    cur.execute("CREATE TABLE types (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR, extension VARCHAR);")
    cur.execute("CREATE TABLE files (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR, path INTEGER, type INTEGER);")
    cur.execute("CREATE TABLE authors (id INTEGER PRIMARY KEY AUTOINCREMENT, first_name VARCHAR, last_name VARCHAR);")
    cur.execute("CREATE TABLE tags (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR);")
    cur.execute("CREATE TABLE categories (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR );")
    cur.execute("CREATE TABLE books_tags (book_id INTEGER, tags_id INTEGER, PRIMARY KEY (book_id, tags_id));")
    cur.execute("CREATE TABLE books_categories (book_id INTEGER, category_id INTEGER, PRIMARY KEY(book_id, category_id ));")
    cur.execute("CREATE TABLE books (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR, path INTEGER, type INTEGER, author INTEGER DEFAULT NULL, \
                    CONSTRAINT directories_id FOREIGN KEY (path) REFERENCES directories(id),\
                    CONSTRAINT type_id FOREIGN KEY (type) REFERENCES types(id), \
                    CONSTRAINT author_id FOREIGN KEY (author) REFERENCES authors(id));")

def does_type_exist(a_type, cur, log):
    a_type = a_type.lower()
    cur.execute("SELECT id FROM types WHERE extension = ?",(a_type,))
    result = cur.fetchone()
    if result is None:
        cur.execute("INSERT INTO types(name,extension) VALUES(NULL,?)", (a_type,))
        log.info("Adding type {} to types table".format(a_type))
    else:
        log.debug("type exists = {}".format(result))

def populate_files_table(cur, log):
    log.info("Populating files trable")
	# even though I could have gotten this from generate_directories_table() I thought it would be confusing
    listOfDirs = [x[0] for x in os.walk(basedir)]

    for dir1 in listOfDirs:

        for entry in os.listdir(dir1):
            log.debug("entry = " + entry)
            # make sure it's a file (and not a dir) and it has an extension
            if (os.path.isfile(os.path.join(dir1, entry)) and '.' in entry):
                log.debug("Is a file " + dir1+ '/' + entry)
                # make sure it has an extension
                log.debug("dir ="+ dir1)
                log.debug("full_name = " + entry)
                cur.execute("SELECT id FROM directories WHERE full_path = ?",(dir1 + '/',))
                result = sqCur1.fetchone()
                log.debug("result = " + str(result))
                name, ext = entry.rsplit('.',1)
                does_type_exist(ext, cur, log)
                query = "INSERT INTO files(name, path, type) VALUES(?,(SELECT id FROM directories WHERE full_path = ?) , (SELECT id FROM types WHERE extension = ?))"            
                log.debug("name = {0}, ext = {1}".format(name, ext))
                query_values = (name, dir1 + '/', ext)
                sqCur1.execute(query, query_values)
                
if __name__ == "__main__":
	
    logging.config.fileConfig('conf/logging.conf')
    logger = logging.getLogger('generateDB')
	
    #logging.basicConfig(filename='/tmp/generator.log',level=logging.DEBUG)

    sqCon = sqlite3.Connection(database="proj.db")
	# Going to start with 2 cursors
    sqCur1 = sqCon.cursor()
    sqCur2 = sqCon.cursor()
	
	# get basedir from command-line, conf file, or store preferences in sqlite3
	# but for now:
    basedir = '/mnt/Storage1/EBooks'

    generate_directories_table(basedir,sqCur1,logger)
    create_tables_for_books(sqCur1, logger)
    populate_files_table(sqCur1, logger)

    sqCon.commit()
    sqCon.close()

