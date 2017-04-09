#! /usr/bin/env python3

import os, sys, sqlite3, time
import logging, logging.config 
import configparser, argparse
import tarfile, zipfile

try:
    import magic

except Exception as e:
    raise Exception ("The 'magic' library is not installed - please install with sudo pip3 install python-magic")

'''generateDB.py

generateDB.py creates a catalog of all of the files in a directory that the user
has permission to see. If that directory is '/'(root), then it will catalog your
entire computer. I really just wanted something to display my eBooks.

It first walks the directory (as a line in main) - storing that in a list, as
well as the directories table in sqlite3. Then, it goes through each directory,
checking for files. If it finds a file, it will log the unique extension, and
then log the file name.

There is an accompanying sql table browser.
'''

def get_config_values():

    config = configparser.ConfigParser()
    config.read('conf/generateDB.conf')

    return (config['app']['log_level'],config['database']['name'],config['target']['dir'])

def get_cli_arguments(lvl,db,dir1):

    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--log-level", default=lvl,
                    help="Set log level (CRITICAL, ERROR, WARNING, INFO, DEBUG)")
    parser.add_argument("-d", "--directory", default=dir1,
                    help="Set base directory to search")
    parser.add_argument("-db", "--database", default=db,
                    help="Set the name of the database")
    args = parser.parse_args()
    
    return (args.log_level, args.directory, args.database)

def generate_directories_table(baseDir, cur, log, dirList):
    # Populate dirs table 
    # CREATE TABLE directories (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR, path VARCHAR, full_path VARCHAR);
    # The idea being that the dir will have its own name, path is the parent, full_path is what I'll add 
    log.info("generating data for directories table")
    cur.execute("DROP TABLE IF EXISTS directories;")
    cur.execute("CREATE TABLE directories (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR, path VARCHAR, full_path VARCHAR);")

    #listOfDirs = [x[0] for x in os.walk(baseDir)]

    for i in dirList:
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


def populate_files_table(cur, log, dirList):
    log.info("Populating files table")
    # even though I could have gotten this from generate_directories_table() I thought it would be confusing
    # See comment in main about this taking too long on really big volumes
    # listOfDirs = [x[0] for x in os.walk(basedir)]

    for dir1 in dirList:

        try:

            for entry in os.listdir(dir1):
                log.debug("entry = " + entry)
                # make sure it's a file (and not a dir) and it has an extension
                if (os.path.isfile(os.path.join(dir1, entry)) and '.' in entry):
                    log.debug("Is a file " + dir1+ '/' + entry + ", dir = " + dir1 +", full_name = "+ entry)
                    cur.execute("SELECT id FROM directories WHERE full_path = ?",(dir1 + '/',))
                    result = sqCur1.fetchone()
                    if result is None:
                        raise RuntimeError("'"+dir1 + "' not in database!")
                                           
                    log.debug("directories.id = " + str(result))
                    name, ext = entry.rsplit('.',1)
                    does_type_exist(ext, cur, log)

                    try:
                        query = "INSERT INTO files(name, path, type) VALUES(?,(SELECT id FROM directories WHERE full_path = ?) , (SELECT id FROM types WHERE extension = ?))"
                    except:
                        msg = "Could not insert row for name = "+ name + ", path = " + path+ ", type = " + ext + ", entry = " + entry
                        log.error(msg)
                        raise RuntimeError(msg)
                    else:
                        log.debug("name = {0}, ext = {1}".format(name, ext))
                        
                    query_values = (name, dir1 + '/', ext)
                    sqCur1.execute(query, query_values)
        except PermissionError as p:
            log.error("Could not access " + str(entry) + str(p))

        except Exception as e:
            log.error(str(e))
            log.error("Error details: entry = " + str(entry) + "dir1 = " + str(dir1))

        else:
            sqCon.commit()                
                
if __name__ == "__main__":
    
    logLvl, database, directory  = get_config_values()
    logLvl,basedir, db = get_cli_arguments(logLvl, database, directory)
    numeric_level = getattr(logging, logLvl.upper(), None)

    # Check the validity of the args
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % logLvl)
    
    if not os.path.isdir(basedir):
        raise ValueError("Directory doesn't exists: %s" % basedir)

    logging.config.fileConfig('conf/logging.conf')
    logger = logging.getLogger('generateDB')
    logger.setLevel(numeric_level)
    logger.info("Starting up... Using log level: "+ logLvl +", database: " + db + ", target directory: " + basedir)
    
    # logger pretty much straight out of the docs: https://docs.python.org/3.5/howto/logging.html

    # I just ran this on a 5TB external volume and it took a while - So, instead of running it twice - I'll run it onece
    # and pass it around as needed:
    # Seriously - According to the logs (Yay! for adding logging :)) it took 40 minutes on a 1/2 full 5TB volume
    logging.info("Getting list of directories from the base directory. This may take a while.")
    listOfDirs = [x[0] for x in os.walk(basedir)]
    logging.info("List collected.")
	
    sqCon = sqlite3.Connection(database=db)
    sqCon.isolation_level = None #Added for autocommit
    sqCur1 = sqCon.cursor()

    generate_directories_table(basedir,sqCur1,logger, listOfDirs)
    create_tables_for_books(sqCur1, logger)
    populate_files_table(sqCur1, logger, listOfDirs)

    sqCon.commit()
    sqCon.close()

