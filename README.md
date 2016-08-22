# Simple TODO

A simple, yet powerful todo script for use within the terminal, written in python.

![Simple TODO](/../screenshots/screenshots/todo_main.png?raw=true "TODO Example")

### Features
- Simple, self-explanatory usage
- Highlight important tasks
- Add, delete, flag and check multiple tasks with one command
- Undo an edit easily

### Installation

Simple TODO requires python 2.7+ to run.

Then simply clone this repo to a safe directory.

```sh
$ cd ~/git
$ git clone https://github.com/stevebasher/todo
```

Finally, add the _todo_ alias to your `.bashrc` or `.zshrc` and source the file.

```sh
$ echo "todo=python ~/git/todo/main.py" >> ~/.bashrc
$ source ~/.bashrc
```

### Usage

Replace `#` with a list of numbers, seperated by a space, refering to the corresponding items in the todo list.

`todo` Print the current tasks in the todo list.

`todo add "Task 1" "Task 2" ...` Add the items given to the list. If no items are given, the add-item environment is started, which is better for adding more than a couple of items.

`todo edit #` Replace the text of the item.

`todo check #` Marks the items with [X].

`todo rm #` Removes the items from the list. Use `all` instead of number references to remove every item.

`todo important #` Makes the items important, highlighting them yellow and adding a (i) suffix.

`todo unimportant #` Reverts items to the non-important state.

`todo undo` Revert the previous action

`todo logs` Print the logs for the todo script (_Advanced users only_)
