import sys
import os
from subprocess import call
import copy
import datetime

TODO_PATH = os.path.dirname(__file__) + '/'
TODO_LOG_PATH = TODO_PATH + 'todo_items.log'
TODO_ITEMS_PATH = TODO_PATH + 'todo_items.txt'
TODO_PRINT_PATH = TODO_PATH + 'todo_print.txt'
EDITOR = os.environ.get('EDITOR', 'vim')

def log(log_action, log_msg=''):
	with open(TODO_LOG_PATH, "a") as log_file:
		log_prefix = str(datetime.datetime.now())
		log_string = log_prefix + " [" + log_action + "] " + log_msg + "\n"
		log_file.write(log_string)

def print_logs():
	with open(TODO_LOG_PATH, "r") as log_file:
		print log_file.read()

def file_exists_not_empty(file_path):
	return os.path.isfile(file_path) and os.path.getsize(file_path) > 0

def clear_file(file_path):
	open(file_path, 'w').close()

def main(args):
	if args:
		if args[0] == 'add':
			if len(args) > 1:
				add_todo_items(args[1:])
			else:
				add_todo_items()
		elif args[0] == 'clear':
			log('Clear')
			clear_file(TODO_ITEMS_PATH)
		elif args[0] == 'edit':
			log('Edit')
			call([EDITOR, TODO_ITEMS_PATH])
		elif args[0] == 'logs':
			log('Print logs')
			print_logs()
	else:
		display_todo()

def display_todo():
	if file_exists_not_empty(TODO_ITEMS_PATH):
		f = open(TODO_ITEMS_PATH, "r")
		print '----------- TODO -----------'
		print f.read().rstrip('\n')
		print '----------------------------'
		log('Display')
	else:
		print 'Todo is empty, use `todo add [items]`'
		log('Display', 'Empty')

def add_todo_items(items=None):
	items_build = copy.copy(items)
	log('Add items', str(items))

	if items is None:
		print "Adding Todo Items (q to quit):"
	while 1:
		f = open(TODO_ITEMS_PATH, "a+")

		if items is not None and len(items) > 0:
			todo_item = items.pop(0)
		elif items_build is not None:
			f.close()
			display_todo()
			break
		else:
			todo_item = raw_input("- ")
			if todo_item in ("q", "q\n"):
				f.close()
				display_todo()
				break

		if todo_item:
			f.write(todo_item+"\n")
			log('Write', todo_item)

		f.close()

if __name__ == "__main__":
   main(sys.argv[1:])
