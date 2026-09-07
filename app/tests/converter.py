from html_to_markdown import convert

html = "<html><body><h1>Hello</h1><p>This is a test.</p></body></html>"

result = convert(html)

print(type(result))
print(result)
print(dir(result))