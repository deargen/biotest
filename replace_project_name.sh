# NOTE: Use this to replace all strings in the project template with the new project name,
# then delete this file.

# python-project-template-2024 -> new-ml-project
github_repo_name=new-project

# ml_project -> new_module_name
module_name=new_project

# ml-project -> new-package-name
package_name=new-project

# ML_PROJECT -> NEW_PROJECT
# e.g. ML_PROJECT_DATA_DIR -> NEW_PROJECT_DATA_DIR
envvar_name=NEW_PROJECT

# Python Project Template -> New Project
doc_title="New Project"
doc_url='https://deargen-ai.gitlab.io/new-project-docs'


if [[ "$OSTYPE" == "darwin"* ]]; then
    SED="gsed"
    if ! command -v gsed &> /dev/null; then
        echo "gsed is not installed. Please install it using 'brew install gnu-sed'"
        exit 1
    fi
else
    SED="sed"
fi

rg -g '!replace_project_name.sh' --files-with-matches -l python-project-template-2024 | xargs $SED -i "s/python-project-template-2024/$github_repo_name/g"
rg -g '!replace_project_name.sh' --files-with-matches -l ml_project | xargs $SED -i "s/ml_project/$module_name/g"
rg -g '!replace_project_name.sh' --files-with-matches -l ml-project | xargs $SED -i "s/ml-project/$package_name/g"
rg -g '!replace_project_name.sh' --files-with-matches -l ML_PROJECT | xargs $SED -i "s/ML_PROJECT/$envvar_name/g"
rg -g '!replace_project_name.sh' --files-with-matches -l "Python Project Template" | xargs $SED -i "s/Python Project Template/$doc_title/g"
rg -g '!replace_project_name.sh' --files-with-matches -l 'https://deargen-ai.gitlab.io/python-project-template-docs' | xargs $SED -i "s|https://deargen-ai.gitlab.io/python-project-template-docs|$doc_url|g"

mv src/ml_project src/$module_name
