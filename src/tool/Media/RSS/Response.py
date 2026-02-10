from App.Objects.Object import Object

class Response(Object):
    @classmethod
    async def download(cls, url: str) -> str:
        import aiohttp

        response_xml = None
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response_xml = await response.text()

        return response_xml
