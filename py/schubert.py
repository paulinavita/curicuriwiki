# docs : https://wikipedia.readthedocs.io/en/latest/code.html#api

import wikipedia
import re
wiki = wikipedia.page('Franz Schubert')

# Extract
text = wiki.content
text = re.sub(r'==.*?==+', '', text)
text = text.replace('\n', '')

print(text)