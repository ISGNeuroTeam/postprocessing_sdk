#.SILENT:
SHELL = /bin/bash


all:
	echo -e "Required section:\n\
 build - build project into build directory, with configuration file and environment\n\
 clean - clean all addition file, build directory and output archive file\n\
 test - run all tests\n\
 pack - make output archive, file name format \"{{command_name}}_vX.Y.Z_BRANCHNAME.tar.gz\"\n\
"

VERSION := "0.0.1"
BRANCH := $(shell git name-rev $$(git rev-parse HEAD) | cut -d\  -f2 | sed -re 's/^(remotes\/)?origin\///' | tr '/' '_')

pack: make_build
	rm -f {{command_name}}-*.tar.gz
	echo Create archive \"{{command_name}}-$(VERSION)-$(BRANCH).tar.gz\"
	cd make_build; tar czf ../{{command_name}}-$(VERSION)-$(BRANCH).tar.gz {{command_name}}

clean_pack:
	rm -f {{command_name}}-*.tar.gz


{{command_name}}.tar.gz: build
	cd make_build; tar czf ../{{command_name}}.tar.gz {{command_name}} && rm -rf ../make_build

build: make_build

make_build:
	# required section
	echo make_build
	mkdir make_build
	cp -R ./{{command_name}} make_build
	cp *.md make_build/{{command_name}}/
	cp *.py make_build/{{command_name}}/


clean_build:
	rm -rf make_build

venv:
	echo Create venv;
	conda create --copy -p ./venv -y
	conda install -p ./venv python==3.9.7 -y
	./venv/bin/pip install --no-input  postprocessing_sdk @ git+ssh://git@github.com:ISGNeuroTeam/postprocessing_sdk.git@develop

pp_cmd: venv
	./venv/bin/python3/pp_sdk createcommandlinks

dev: pp_cmd
	ln -s -r ./{{command_name}} pp_cmd/{{command_name}}

clean: clean_build clean_pack clean_test

test:
	@echo "Testing..."

clean_test:
	@echo "Clean tests"
