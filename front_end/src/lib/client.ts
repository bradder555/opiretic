import { Configuration } from "./openapi_client"
import { DefaultApi } from "./openapi_client"

export const opiClient = new DefaultApi(
    new Configuration(
        {basePath: window.location.origin}
    )
)