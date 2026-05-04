import re
with open('custom_build/userdata/guisettings.xml', 'r') as f:
    content = f.read()
content = re.sub(r'\s*<setting id="window\.(width|height|top|left)"[^>]*>[^<]*</setting>', '', content)
with open('custom_build/userdata/guisettings.xml', 'w') as f:
    f.write(content)
print('Done')
