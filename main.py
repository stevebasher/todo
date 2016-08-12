import sys
import os
from subprocess import call
import copy
import datetime

TODO_PATH = os.path.dirname(__file__) + '/'
TODO_LOG_PATH = TODO_PATH + 'todo_items.log'
TODO_ITEMS_PATH = TODO_PATH + 'todo_items.txt'
TODO_PRINT_PATH = TODO_PATH + 'todo_print.txt'
TODO_PREVIOUS_PATH = TODO_PATH + 'todo_prev_items.txt'
EDITOR = os.environ.get('EDITOR', 'vim')

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	HIGHLIGHT = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

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
				add_items(args[1:])
			else:
				add_items()
		elif args[0] == 'rm':
			log('Remove: %s', str(args[1:]))
			remove_items(args[1:])
		elif args[0] == 'edit':
			log('Edit')
			if len(args) > 1:
				edit_item(args[1])
			else:
				edit_item(None)
		elif args[0] == 'check':
			if len(args) > 1:
				check_item(args[1:])
			else:
				check_item(None)
		elif args[0] == 'uncheck':
			if len(args) > 1:
				uncheck_item(args[1:])
			else:
				uncheck_item(None)
		elif args[0] == 'important':
			if len(args) > 1:
				highlight_items(args[1:])
			else:
				highlight_items(None)
		elif args[0] == 'unimportant':
			if len(args) > 1:
				undo_highlight_items(args[1:])
			else:
				undo_highlight_items(None)
		elif args[0] == 'undo':
			undo_items()
			log('Undo')
		elif args[0] == 'logs':
			log('Print logs')
			print_logs()
	else:
		show_todo()

def build_todo():
	with open(TODO_ITEMS_PATH, "r") as f_items, open(TODO_PRINT_PATH, "w+") as f_print:
		for i, line in enumerate(f_items):
			f_print.write('{}) {}'.format(i+1, line))
		log('Build')

def display_todo():
	if file_exists_not_empty(TODO_ITEMS_PATH):
		with open(TODO_PRINT_PATH, "r") as f_print:
			f_print_lines = f_print.readlines()
			print bcolors.OKBLUE + '\n-------------- TODO --------------' + bcolors.ENDC
			for line in f_print_lines:
				if line.strip():
					if len(line) > 3 and line.rstrip()[-3:] == "(i)":
						print bcolors.HIGHLIGHT + line.rstrip('\n') + bcolors.ENDC
					else:
						print line.rstrip('\n')
			print bcolors.OKBLUE + '----------------------------------\n' + bcolors.ENDC
		log('Display')
	else:
		print 'Todo is empty, use `todo add [items]`'
		log('Display', 'Empty')

def show_todo():
	build_todo()
	display_todo()

def write_item(f, item, **kwargs):
	write_str = item.rstrip('\n')

	# Check Prefix
	prefix = "[X] " if kwargs.get('checked') is True else "[ ] "
	if item[0] == "[" and item[2:4] == "] ":
		if kwargs.get('overwrite_prefix') is True:
			write_str = prefix + write_str[4:]
	else:
		write_str = prefix + item.rstrip('\n')

	# Important Postfix
	if kwargs.get('important') is True:
		if len(write_str) > 3 and write_str[-3:] != "(i)":
			write_str = write_str + " (i)"
	elif kwargs.get('important') is False:
		if len(write_str) > 3 and write_str[-3:] == "(i)":
			write_str = write_str[:-3]
	f.write(write_str+'\n')

def check_item(item_numbers):
	if item_numbers:
		with open(TODO_ITEMS_PATH, "r") as f:
			items = f.readlines()
		with open(TODO_ITEMS_PATH, "w") as f:
			for i, item in enumerate(items):
				if str(i+1) in item_numbers or item_numbers[0] == 'all':
					write_item(f, item, overwrite_prefix=True, checked=True)
				else:
					write_item(f, item)
		show_todo()
	else:
		print 'Please specify item(s) to check.'

def uncheck_item(item_numbers):
	if item_numbers != 'all' and not isinstance(item_numbers, list):
		item_numbers = list(item_numbers)
	if item_numbers:
		with open(TODO_ITEMS_PATH, "r") as f:
			items = f.readlines()
		with open(TODO_ITEMS_PATH, "w") as f:
			for i, item in enumerate(items):
				if str(i+1) in item_numbers or item_numbers[0] == 'all':
					write_item(f, item, overwrite_prefix=True, checked=False)
				else:
					write_item(f, item)
		show_todo()
	else:
		print 'Please specify item(s) to uncheck.'

def add_items(items=None):
	backup_items()
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
			show_todo()
			break
		else:
			todo_item = raw_input("- ")
			if todo_item in ("q", "q\n"):
				f.close()
				show_todo()
				break

		if todo_item:
			write_item(f, todo_item)
			log('Write', todo_item)

		f.close()

def edit_item(item_number=None):
	backup_items()
	if item_number is not None:
		if item_number == 'vim':
			call([EDITOR, TODO_ITEMS_PATH])
		else:
			success = True
			with open(TODO_ITEMS_PATH,"r") as f:
				items = f.readlines()
			with open(TODO_ITEMS_PATH,"w") as f:
				for i, item in enumerate(items):
					if str(i+1) == item_number:
						print 'Editing Item %s:' % str(i+1)
						print 'Original: %s' % item[4:].rstrip('\n').rstrip(' (i)')
						new_item = raw_input('New: ')
						if new_item:
							# Handle Important Flag
							import ipdb; ipdb.set_trace()
							if len(item) > 3 and item.rstrip('\n')[-3:] == "(i)":
								i_flag = " (i)"
							else:
								i_flag = ""
							write_item(f, new_item.rstrip('\n')+i_flag)
						else:
							success = False
							print 'The new item cannot be empty. To remove an item use todo rm #.'
							write_item(f, item)
					else:
						write_item(f, item)
			if success:
				print 'Sucessfully edited %s \n' % item_number
				show_todo()
	else:
		print "Please specify an item to edit."

def remove_items(args=list()):
	if args:
		if args[0] == 'all':
			backup_items()
			del_all = raw_input("Are you sure you want to delete every item (y/N)? ")
			if del_all in 'yY':
				clear_file(TODO_ITEMS_PATH)
				print 'All cleared'
			else:
				print 'Aborted. Use todo rm # to remove a specific item.'
		else:
			backup_items()
			with open(TODO_ITEMS_PATH,"r") as f:
				items = f.readlines()
			with open(TODO_ITEMS_PATH,"w") as f:
				for i, item in enumerate(items):
					if str(i+1) not in args:
						write_item(f, item)
			print 'Sucessfully removed %s \n' % ', '.join(args)
			show_todo()
	else:
		print "Please specify an item to remove. Use 'all' to remove all."

def backup_items():
	with open(TODO_ITEMS_PATH,"r") as current, open(TODO_PREVIOUS_PATH,"w") as prev:
		current_items = current.readlines()
		for item in current_items:
			write_item(prev, item)

def undo_items():
	with open(TODO_ITEMS_PATH,"w") as current, open(TODO_PREVIOUS_PATH,"r") as prev:
		prev_items = prev.readlines()
		for item in prev_items:
			write_item(current, item)
	show_todo()

def highlight_items(item_numbers):
	if item_numbers:
		with open(TODO_ITEMS_PATH, "r") as f:
			items = f.readlines()
		with open(TODO_ITEMS_PATH, "w") as f:
			for i, item in enumerate(items):
				if str(i+1) in item_numbers or item_numbers[0] == 'all':
					write_item(f, item, important=True)
				else:
					write_item(f, item)
		show_todo()
	else:
		print 'Please specify item(s) to make important.'

def undo_highlight_items(item_numbers):
	if item_numbers:
		with open(TODO_ITEMS_PATH, "r") as f:
			items = f.readlines()
		with open(TODO_ITEMS_PATH, "w") as f:
			for i, item in enumerate(items):
				if str(i+1) in item_numbers or item_numbers[0] == 'all':
					write_item(f, item, important=False)
				else:
					write_item(f, item)
		show_todo()
	else:
		print 'Please specify item(s) to .'

if __name__ == "__main__":
   main(sys.argv[1:])
