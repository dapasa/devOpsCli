#!/bin/bash

# Function to compare two version strings
version_gt() {
    test "$(printf '%s\n' "$@" | sort -V | head -n 1)" != "$1"
}

set_venv() {
    echo "Creating python cli_env"
    $1 -m venv cli_env
    source "./cli_env/bin/activate"
    echo "Installing requirements"
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    echo .
    echo .
    echo "Enviroment set. To use it, active it with 'source ./cli_env/bin/activate'"
}

# Check if python3 is available
if command -v python3 &> /dev/null; then
    python_version=$(python3 --version 2>&1 | awk '{print $2}')
    echo "Python installed. Version: $python_version"

    # Check if Python 3 version is greater than 3.0
    if version_gt "$python_version" "3.0"; then
        echo "Python version is greater than 3.0."
        set_venv python3
    else
        echo "Python version is not greater than 3.0."
        echo "Aborting"
        exit
    fi
else
    # Check if python is available (for systems where python3 is not the default)
    if command -v python &> /dev/null; then
        python_version=$(python --version 2>&1 | awk '{print $2}')
        echo "Python installed. Version: $python_version"
        # Check if Python version is greater than 3.0
        if version_gt "$python_version" "3.0"; then
            echo "Python version is greater than 3.0."
            set_venv python3

        else
            echo "Python version is not greater than 3.0."
        fi
    else
        echo "Python version is not greater than 3.0."
        echo "Aborting"
        exit
    fi
fi
