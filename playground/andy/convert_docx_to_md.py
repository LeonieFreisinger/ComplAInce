from cleanup_md import clean_up

with open('test.md', 'r') as file:
    doc = file.readlines()

counter = 0
new_doc = []
for row in doc:
    if len(row) > 15000:
        continue
    new_doc.append(row)

new_doc = clean_up(new_doc)

with open('test_cleaned.md', 'w') as file:
    file.write(' '.join(new_doc))