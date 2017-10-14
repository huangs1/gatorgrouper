""" Parses the arguments provided on the command-line """

from random import shuffle
import argparse
import itertools
import sys
import logging
import grouping_method

#default values
from defaults import *
from read_student_file import read_student_file

def parse_gatorgrouper_arguments(args):

    gg_parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    gg_parser.add_argument(
        "-d", "--debug",
        help="Display diagnostic information",
        action="store_const", dest="logging_level", const=logging.DEBUG, default=logging.ERROR
    )

    gg_parser.add_argument(
        "-v", "--verbose",
        help="Display confirmation information",
        action="store_const", dest="logging_level", const=logging.INFO
    )

    gg_parser.add_argument(
        "--group-size",
        help="Number of students in a group",
        type=int,
        default=DEFAULT_TEAM_SIZE,
        required=False)

    gg_parser.add_argument(
        "--students-file",
        help="File containing last name of students",
        type=str,
        default=DEFAULT_STUDENT_FILE,
        required=False)

    gg_parser.add_argument(
        "--random",
        help="Use random grouping method",
        action="store_const", dest="grouping_method", const=grouping_method.RANDOM, default=grouping_method.RANDOM
    )

    gg_parser.add_argument(
        "--sudoku",
        help="Use sudoku grouping method",
        action="store_const", dest="grouping_method", const=grouping_method.SUDOKU
    )

    gg_parser.add_argument(
        "--round-robin",
        help="Use round-robin grouping method",
        action="store_const", dest="grouping_method", const=grouping_method.ROUND_ROBIN
    )

    gg_parser.add_argument(
        "--absentees",
        nargs="+",
        type=str
    )

    gg_arguments_finished = gg_parser.parse_args(args)

    logging.basicConfig(format="%(levelname)s:%(pathname)s: %(message)s", level=gg_arguments_finished.logging_level)

    if check_valid_group_size(gg_arguments_finished.group_size, read_student_file(gg_arguments_finished.students_file)) == False:
        quit()

    return gg_arguments_finished

def check_valid_group_size(group_size, students_list):
    students_list_length = len(students_list)
    if (group_size <= 1 or group_size > students_list_length / 2): # indicates invalid group size
        logging.error("Group size: " + str(group_size) + "\nNumber of students: " + str(students_list_length) + "\nGroup size must be greater than 1 and less than or equal to half of the number of students.")
        return False
    else:
        logging.info("Group size: " + str(group_size) + "\nNumber of students: " + str(students_list_length) + "\nValid group size.")
        return True
