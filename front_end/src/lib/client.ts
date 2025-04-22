import { Configuration } from "./openapi_client"
import { DefaultApi } from "./openapi_client"

var basePath = import.meta?.env?.DEV == true ? "http://localhost:8000" : window.location.origin;
console.log("windows.location.origin= " + window.location.origin)
console.log(import.meta.env)
console.log("creating client with basepath " + basePath)

export const opiClient = new DefaultApi(
    new Configuration(
        {basePath: basePath}
    )
)