import sys, os
from typing import List
from pypicgo.core.base.plugin import FinallyPlugin
from pypicgo.core.base.result import Result


class TyporaPlugin(FinallyPlugin):
    name = 'Typora'

    def execute(self, results: List[Result]):
        urls = []
        for result in results:
            if result.status:
                urls.append(result.remote_url)
        if len(urls) > 0:
            message = os.linesep.join(urls)
            sys.stdout.write(f'Upload Success:{os.linesep}message{os.linesep}')
            lines = [line for line in message.splitlines() if line.strip()]
            f =  open('url.txt', 'w')
            f.write('\n'.join(lines))
            f.close()
