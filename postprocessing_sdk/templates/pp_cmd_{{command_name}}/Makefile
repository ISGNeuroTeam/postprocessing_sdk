#.SILENT:
SHELL = /bin/bash


all:
	echo -e "Required section:\n\
 build - build project into build directory, with configuration file and environment\n\
 clean - clean all addition file, build directory and output archive file\n\
 test - run all tests\n\
 pack - make output archive, file name format \"pp_cmd_{{command_name}}_vX.Y.Z_BRANCHNAME.tar.gz\"\n\
"

VERSION := "0.1.0"
BRANCH := $(shell git name-rev $$(git rev-parse HEAD) | cut -d\  -f2 | sed -re 's/^(remotes\/)?origin\///' | tr '/' '_')

CONDA = conda/miniconda/bin/conda
ENV_PYTHON = venv/bin/python3.9


conda/miniconda.sh:
	echo Download Miniconda
	mkdir -p conda
	wget https://repo.anaconda.com/miniconda/Miniconda3-py39_23.1.0-1-Linux-x86_64.sh -O conda/miniconda.sh; \

conda/miniconda: conda/miniconda.sh
	bash conda/miniconda.sh -b -p conda/miniconda; \

install_conda: conda/miniconda

conda/miniconda/bin/conda-pack: conda/miniconda
	conda/miniconda/bin/conda install conda-pack -c conda-forge  -y

install_conda_pack: conda/miniconda/bin/conda-pack

clean_conda:
	rm -rf ./conda

pack: make_build
	rm -f pp_cmd_{{command_name}}-*.tar.gz
	echo Create archive \"pp_cmd_{{command_name}}-$(VERSION)-$(BRANCH).tar.gz\"
	cd make_build; tar czf ../pp_cmd_{{command_name}}-$(VERSION)-$(BRANCH).tar.gz {{command_name}}

clean_pack:
	rm -f pp_cmd_{{command_name}}-*.tar.gz


pp_cmd_{{command_name}}.tar.gz: build
	cd make_build; tar czf ../pp_cmd_{{command_name}}.tar.gz {{command_name}} && rm -rf ../make_build

build: make_build

make_build:
	# required section
	echo make_build
	mkdir make_build
	cp -R ./{{command_name}} make_build
	cp *.md make_build/{{command_name}}/



clean_build:
	rm -rf make_build

venv: conda/miniconda
	$(CONDA) create --copy -p ./venv -y
	$(CONDA) install -p ./venv python==3.9.7 -y;
	$(ENV_PYTHON) -m pip  install --no-input  postprocessing_sdk --extra-index-url http://s.dev.isgneuro.com/repository/ot.platform/simple --trusted-host s.dev.isgneuro.com

clean_venv:
	rm -rf ./venv

dev: venv
	rm -rf ./venv/lib/python3.9/site-packages/postprocessing_sdk/pp_cmd/{{command_name}}
	./venv/bin/pp_sdk createcommandlinks
	cp ./venv/lib/python3.9/site-packages/postprocessing_sdk/pp_cmd/otl_v1/config.example.ini ./venv/lib/python3.9/site-packages/postprocessing_sdk/pp_cmd/otl_v1/config.ini
	cp ./venv/lib/python3.9/site-packages/postprocessing_sdk/pp_cmd/readFile/config.example.ini ./venv/lib/python3.9/site-packages/postprocessing_sdk/pp_cmd/readFile/config.ini

clean: clean_build clean_pack clean_test clean_venv

test:
	test:
	docker build --progress=plain --no-cache -t pp_cmd_{{command_name}}_test . && docker run -it pp_cmd_{{command_name}}_test

clean_test:
	@echo "Clean tests"
