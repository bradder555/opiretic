uv run extract-openapi.py
uv run openapi-generator-cli generate -g typescript-fetch -i ./openapi.yaml -o ./openapi_client/ --additional-properties=supportsES6=true

cd ./openapi_client
#npm install 
#npm run build 

cd ..