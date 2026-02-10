location=$(pwd)
venv_name="venv"
tool_name="tool"
script_name="bin/activate"
do_update=true

venv_path="$location/$venv_name"
tool_path="$location/$tool_name"

pip --version

# termux maybe: python -m pip install pydantic-core --extra-index-url https://termux-user-repository.github.io/pypi/
# also it requires rust ??

if [ -d "$venv_path" ]; then
    echo "[Venv] An existing Python Virtual Environment found"
else
    echo "[Venv] Created new Python Virtual Environment"
    python -m venv $path    
fi

sh script_name

if $do_update; then
    pip install -e .
fi

cd $tool_path
