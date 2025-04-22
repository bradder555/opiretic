uv sync

start_dir="$(pwd)"
fe_dir="./front_end"
out_dir="$fe_dir/src/lib/openapi_client"

echo "deleting '$out_dir'"
rm -rf $out_dir

echo "creating '$out_dir'"
mkdir $out_dir 

echo "exporting openapi file"
uv run extract-openapi.py

echo "running openapi generator, creating typescript client"
uv run openapi-generator-cli generate -g typescript-fetch \
-i ./openapi.yaml -o $out_dir --additional-properties=supportsES6=true

echo "cd to $fe_dir"
cd $fe_dir 

echo "running npm install"
npm install

echo "running npm build"
npm run build

echo "returning to start directory $start_dir"
cd $start_dir 
