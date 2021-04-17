filename = 'gifts2'
with open(f'{filename}.md', 'r') as file:
    text = file.read()

text = text.split('**')
text = ''.join(text)
text = text.split('#')
text = [el.strip() for el in text]
text = ''.join(text)
text = text.split('|')
text = [el.strip() for el in text]
text = ''.join(text)
text = text.split('&39;')
text = ''.join(text)
text = text.split('&quot;')
text = ''.join(text)
text = text.split('_')
text = ''.join(text)

with open(f'{filename}_cleaned.md', 'w') as file:
    file.write(text)