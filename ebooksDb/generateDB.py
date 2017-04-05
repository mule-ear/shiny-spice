#! /usr/bin/env python3

import os, sys, sqlite3, logging

logging.basicConfig(filename='/tmp/generator.log',level=logging.DEBUG)

sqCon = sqlite3.Connection(database="proj.db")
# Going to start with 2 cursors
sqCur1 = sqCon.cursor()
sqCur2 = sqCon.cursor()

# get basedir from command-line, conf file, or store preferences in sqlite3
# but for now:
basedir = '/mnt/Storage1/EBooks'

def generate_directories_table():
    # Populate dirs table 
    # CREATE TABLE directories (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR, path VARCHAR, full_path VARCHAR);
    # The idea being that the dir will have its own name, path is the parent, full_path is what I'll add 

    sqCur1.execute("DROP TABLE IF EXISTS directories;")
    sqCur1.execute("CREATE TABLE directories (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR, path VARCHAR, full_path VARCHAR);")

    listOfDirs = [x[0] for x in os.walk(basedir)]

    for i in listOfDirs:
        # insertValues = (i.rsplit('/',1)[1] , i.rsplit('/',1)[0] , i)
        # sqCur1.execute("INSERT INTO directories (name, path, full_path) VALUES(?,?,?)", insertValues)
        sqCur1.execute("INSERT INTO directories (name, path, full_path) VALUES(?,?,?)", (i.rsplit('/',1)[1]+'/' , i.rsplit('/',1)[0]+'/' , i+'/'))
            
def create_tables_for_books():
    # CREATE the tables needed for books
    #

    sqCur1.execute("DROP TABLE IF EXISTS books;")
    sqCur1.execute("DROP TABLE IF EXISTS files;")
    sqCur1.execute("DROP TABLE IF EXISTS types;")
    sqCur1.execute("DROP TABLE IF EXISTS authors;")
    sqCur1.execute("DROP TABLE IF EXISTS tags;")
    sqCur1.execute("DROP TABLE IF EXISTS categories;")
    sqCur1.execute("DROP TABLE IF EXISTS books_tags;")
    sqCur1.execute("DROP TABLE IF EXISTS books_categories;")

    sqCur1.execute("CREATE TABLE types (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR, extension VARCHAR);")
    sqCur1.execute("CREATE TABLE files (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR, path INTEGER, type INTEGER);")
    sqCur1.execute("CREATE TABLE authors (id INTEGER PRIMARY KEY AUTOINCREMENT, first_name VARCHAR, last_name VARCHAR);")
    sqCur1.execute("CREATE TABLE tags (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR);")
    sqCur1.execute("CREATE TABLE categories (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR );")
    sqCur1.execute("CREATE TABLE books_tags (book_id INTEGER, tags_id INTEGER, PRIMARY KEY (book_id, tags_id));")
    sqCur1.execute("CREATE TABLE books_categories (book_id INTEGER, category_id INTEGER, PRIMARY KEY(book_id, category_id ));")
    sqCur1.execute("CREATE TABLE books (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR, path INTEGER, type INTEGER, author INTEGER DEFAULT NULL, \
                    CONSTRAINT directories_id FOREIGN KEY (path) REFERENCES directories(id),\
                    CONSTRAINT type_id FOREIGN KEY (type) REFERENCES types(id), \
                    CONSTRAINT author_id FOREIGN KEY (author) REFERENCES authors(id));")

def does_type_exist(a_type):
    a_type = a_type.lower()
    sqCur1.execute("SELECT id FROM types WHERE extension = ?",(a_type,))
    result = sqCur1.fetchone()
    if result is None:
        sqCur1.execute("INSERT INTO types(name,extension) VALUES(NULL,?)", (a_type,))
        logging.info("Adding type {} to types table".format(a_type))
    else:
        logging.debug("type exists = {}".format(result))

def populate_files_table():
	# even though I could have gotten this from generate_directories_table() I thought it would be confusing
    listOfDirs = [x[0] for x in os.walk(basedir)]

    for dir1 in listOfDirs:

        for entry in os.listdir(dir1):
            logging.debug("entry = " + entry)
            # make sure it's a file (and not a dir) and it has an extension
            if (os.path.isfile(os.path.join(dir1, entry)) and '.' in entry):
                logging.debug("Is a file " + dir1+ '/' + entry)
                # make sure it has an extension
                logging.debug("dir ="+ dir1)
                logging.debug("full_name = " + entry)
                sqCur1.execute("SELECT id FROM directories WHERE full_path = ?",(dir1 + '/',))
                result = sqCur1.fetchone()
                logging.debug("result = " + str(result))
                name, ext = entry.rsplit('.',1)
                does_type_exist(ext)
                query = "INSERT INTO files(name, path, type) VALUES(?,(SELECT id FROM directories WHERE full_path = ?) , (SELECT id FROM types WHERE extension = ?))"            
                logging.debug("name = {0}, ext = {1}".format(name, ext))
                query_values = (name, dir1 + '/', ext)
                sqCur1.execute(query, query_values)
                
if __name__ == "__main__":

    generate_directories_table()
    create_tables_for_books()
    populate_files_table()


            
sqCon.commit()
sqCon.close()

