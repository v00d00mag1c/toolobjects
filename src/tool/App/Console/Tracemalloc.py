from App.Executables.Act import Act
from App.Responses.AnyResponse import AnyResponse
import tracemalloc

class Tracemalloc(Act):
    async def implementation(self, i):
        stats = []

        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('lineno')
        for stat in top_stats[:20]:
            stats.append({
                'traceback': str(stat.traceback),
                'size': stat.size,
                'count': stat.count,
            })

        return AnyResponse(data = stats)
