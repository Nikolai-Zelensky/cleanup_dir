#!/usr/bin/python3

import os
import time
import logging
import logging.config
import configparser



def setconfig():
    try:
        script_full_path = os.path.realpath(__file__)
        script_name = os.path.basename(__file__)
        logging.config.fileConfig(script_full_path.replace(script_name, "log_config.ini"))
        config = configparser.ConfigParser()
        configfile = script_full_path.replace(script_name, "config.ini")
        logger_main = logging.getLogger("main")
        if os.path.exists(configfile):
            config.read(configfile)
            try:
                for section in config.sections():
                    config['DEFAULT']['default_day']
                    config[section]['folder']
                    config[section]['days']
                logger_main.info("The configuration file was found and successfully read.")
                return config
            except Exception as exp:
                logger_main.error("Error checking the configuration structure in the {} section. The parameter was not found or incorrectly composed. {}".format(section, exp))
                return exit()
        else:
            logger_main.error("The configuration file was not found. The script will be completed..")
            return exit()
    except Exception as exc:
        logger_main.error("The script configuration file cannot be parsed. Error:\t {}".format(exc))
        return exit()



def check(folder):
    try:
        folder = folder.split(',')
        logger_check = logging.getLogger("check")
        for runner in folder:
            if os.path.exists(runner) == False:
                logger_check.warning("Directory "+ runner + " not found.")
                return 1
    except Exception as exc:
        logger_check.error("Not possible to check the directories. Error:\t{}".format(exc))
        return exit()



def cleanup(default_day, folder, days):
    try:
        SEC_IN_DAY = 86400
        current_time = time.time()
        directories = folder.split(',')
        logger_cleanup = logging.getLogger("cleanup")
        if (days == "0") or (days == ""):
            logger_cleanup.info("The lifetime of the files in the {} directory is not specified. The default value of {} days will be applied.".format(folder, default_day))
            days = default_day
        for listFolder in directories:
            if check(listFolder) == 1:
                continue
            list_of_files = os.listdir(listFolder)
            logger_cleanup.info("Started working with the {} directory. Condition: files older than the {} day(s) will be deleted from this directory.".format(listFolder, days))
            if not list_of_files:
                logger_cleanup.info("There are no files in the {} directory. Work with this catalog has been discontinued.".format(listFolder))
                continue
            for files in list_of_files:
                file_location = os.path.join(listFolder, files)
                file_time = os.stat(file_location).st_mtime
                if(file_time < current_time - SEC_IN_DAY*int(days)):
                    try:
                        os.remove(file_location)
                        if os.path.isfile(file_location) == False:
                            logger_cleanup.info('File {} deleted successfully.'.format(folder+files))
                    except Exception as exc:
                        logger_cleanup.warning('The {} file has not been deleted. Error:\t{}'.format(files, exc))
                        continue
                else:
                    logger_cleanup.info("The {} file does not need to be deleted. Work with this file has been discontinued.".format(files))
    except Exception as exc:
        logger_cleanup.error("It is not possible to delete files. Error:\t{}".format(exc))
        return exit()



def main():
    os.environ['TZ'] = 'Europe/Moscow'
    time.tzset()
    logger_main = logging.getLogger("main")
    config = setconfig()
    logger_main.info('==== START script ====')

    for section in config.sections():
        default_day = config['DEFAULT']['default_day']
        folder = config[section]['folder']
        days = config[section]['days']
        cleanup(default_day, folder, days)

    logger_main.info('==== END script ====\n')
if __name__ == "__main__":
    main()
