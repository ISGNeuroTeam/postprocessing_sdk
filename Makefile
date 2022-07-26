ifndef VERBOSE
.SILENT:
endif

BRANCH := $(shell git name-rev $$(git rev-parse HEAD) | cut -d\  -f2 | sed -re 's/^(remotes\/)?origin\///' | tr '/' '_')
COMMIT_HASH := $(shell git rev-parse --short HEAD)

CONDA_FOLDER = ./conda
CONDA = $(CONDA_FOLDER)/miniconda/bin/conda
ENV_NAME = venv
ENV = ./$(ENV_NAME)
ENV_PYTHON = $(ENV)/bin/python3.9

DEV_STORAGE = https://storage.dev.isgneuro.com/repository/components
PP_STDLIB = pp_stdlib
PP_STDLIB_URL = $(DEV_STORAGE)/$(PP_STDLIB)/$(PP_STDLIB)-0.0.1-master-0002.tar.gz

$(CONDA_FOLDER)/miniconda.sh :
	echo Download Miniconda
	mkdir -p $(CONDA_FOLDER)
	wget https://repo.anaconda.com/miniconda/Miniconda3-py39_4.11.0-Linux-x86_64.sh -O $(CONDA_FOLDER)/miniconda.sh;


$(CONDA_FOLDER)/miniconda/: $(CONDA_FOLDER)/miniconda.sh
	echo Install Miniconda
	bash $(CONDA_FOLDER)/miniconda.sh -b -p $(CONDA_FOLDER)/miniconda;


install_conda_pack:
	$(CONDA) install conda-pack -c defaults -y

pp_stdlib:
	echo $(PP_STDLIB_URL)
	echo Downloading $(PP_STDLIB)...
	if ! [ -d ./$(PP_STDLIB) ];\
		mkdir -p ./$(PP_STDLIB);\
		then curl -# -Lk $(PP_STDLIB_URL) | tar -zx --strip 1 -C ./$(PP_STDLIB) && echo $(PP_STDLIB) downloaded.;\
		else echo $(PP_STDLIB) is already downloaded.;\
	fi

create_env: $(CONDA_FOLDER)/miniconda/ install_conda_pack
	echo Create environment
	$(CONDA) create -p $(ENV) -y
	$(CONDA) install -p $(ENV) python==3.9.7 -y
	$(ENV_PYTHON) -m pip install --no-input -r requirements.txt \
	--extra-index-url http://s.dev.isgneuro.com/repository/ot.platform/simple \
	--trusted-host s.dev.isgneuro.com

build: create_env pp_stdlib
	echo Build
	cp -fr ./$(PP_STDLIB)/* ./postprocessing_sdk/pp_cmd/

test:
	@echo 'Testing'

clean_dist:
	echo Clean dist folders
	rm -fr *.egg-info
	rm -fr build
	rm -fr dist
	rm -f $(ENV_NAME)-*.tar.gz venv.tar.gz

clean_conda:
	rm -rf $(ENV)

remove_conda:
	echo Remove Conda
	if [ -d $(CONDA_FOLDER) ]; then \
		rm -fr $(CONDA_FOLDER); \
  	fi;

clean: clean_conda remove_conda clean_dist

publish: build
ifeq ($(BRANCH), master)
	echo "Creating final distribution"
	sed "s/{{}}//g" setup_template.py > setup.py
else
	echo "Creating development distribution"
	sed "s/{{}}/$(COMMIT_HASH)-dev/g" setup_template.py > setup.py
endif
	( \
	. $(CONDA_FOLDER)/miniconda/bin/activate; \
	conda activate $(ENV_NAME); \
	python ./setup.py sdist; \
	)
	rm setup.py
