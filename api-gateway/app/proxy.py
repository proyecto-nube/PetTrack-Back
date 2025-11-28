import httpx
from fastapi import Request, Response, HTTPException

async def forward_request(request: Request, base_url: str, path: str):
    """
    Reenvía la solicitud al microservicio correspondiente.
    """
    url = f"{base_url}{path}"
    method = request.method
    
    # Preparar headers, excluyendo algunos que no deben reenviarse
    headers = {}
    for key, value in request.headers.items():
        # Excluir headers de host y conexión que son específicos del gateway
        if key.lower() not in ['host', 'connection', 'content-length']:
            headers[key] = value
    
    # Asegurar que Content-Type esté presente si hay body
    body = await request.body()
    if body and 'content-type' not in headers:
        headers['content-type'] = 'application/json'
    
    try:
        async with httpx.AsyncClient(verify=False, timeout=30.0) as client:
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                content=body
            )
        
        # Preparar headers de respuesta, excluyendo algunos
        response_headers = {}
        for key, value in response.headers.items():
            # Excluir headers que pueden causar problemas
            if key.lower() not in ['content-encoding', 'transfer-encoding', 'connection']:
                response_headers[key] = value
        
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=response_headers,
            media_type=response.headers.get("content-type", "application/json")
        )
    except httpx.RequestError as exc:
        raise HTTPException(status_code=503, detail=f"Error al conectar con {url}: {exc}")
