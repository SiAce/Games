from lxml import etree

xml = '''
<stuff>
  <users>
    <user x="2">
      <id>001</id>
      <name>Chuck</name>
    </user>
    <user x="7">
      <id>009</id>
      <name>Brent</name>
    </user>
  </users>
</stuff>'''

tree = etree.XML(xml)
xpathselector = "/stuff/users/user"
data_list = tree.xpath(xpathselector)
for data in data_list:
    print(data)
