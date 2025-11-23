import httpx
from fastapi import Request, Response, HTTPException

async def forward_request(request: Request, base_url: str, path: str):
    """
    Reenvía la solicitud al microservicio correspondiente.
    """
    url = f"{base_url}{path}"
    method = request.method
    headers = dict(request.headers)
    try:
        async with httpx.AsyncClient(verify=False, timeout=30.0) as client:
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                content=await request.body()
            )
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.headers.get("content-type")
        )
    except httpx.RequestError as exc:
        raise HTTPException(status_code=503, detail=f"Error al conectar con {url}: {exc}")
