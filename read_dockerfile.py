from pprint import pprint
from dockerfile_parse import DockerfileParser
import json
import datetime

msg = {'build': {'tag': '', 'ref': 'refs/heads/master', 'author': 'osallou', 'event': 'push', 'created': 1505231302, 'message': 'Update subdir', 'number': 25, 'started': 1505231302, 'branch': 'master', 'commit': 'c294672dc0586004d70efaa76c31b71f03337a1f', 'link': 'http://openstack-192-168-100-43.genouest.org/osallou/test1/25', 'status': 'success'}, 'repo': {'owner': 'osallou', 'name': 'test1'}}

'''
+ git init
+ git remote add origin https://github.com/osallou/test1.git
+ git fetch --no-tags origin +refs/heads/master:
+ git reset --hard -q c294672dc0586004d70efaa76c31b71f03337a1f
+ git submodule update --init --recursive
'''
container = msg['build']['message'].replace('Update ','')

content = None
with open('test1/'+container+'/Dockerfile', 'r') as content_file:
        content = content_file.read()

dfp = DockerfileParser()
dfp.content = content

print(str(dfp.labels))
'''
{'software': 'TPP', 'base.image': 'biocontainers:latest', 'version': '3', 'tags': 'Proteomics', 'toto': '1', 'website': 'http://tools.proteomecenter.org/wiki/index.php?title=Software:TPP', 'description': 'a collection of integrated tools for MS/MS proteomics', 'documentation': 'http://tools.proteomecenter.org/wiki/index.php?title=Software:TPP', 'license': 'http://tools.proteomecenter.org/wiki/index.php?title=Software:TPP', 'software.version': '5.0'}
'''
now = datetime.datetime.now()
post_date = str(now.year)+'-'+'{:02d}'.format(now.month)+'-'+'{:02d}'.format(now.day)
# create/update page for tool and versions from tags
with open('site/biocontainers/' + container + '.md', 'w') as contpage:
    contpage.write('---\nlayout: home\ntitle: '+container+'\n---\n')
    contpage.write('# '+container+'\n')
    contpage.write(' blabla \n')
    contpage.write('site.categories: '+container +'\n')
    contpage.write('<ul>')
    contpage.write('{% for post in site.categories.'+container+' %}')
    contpage.write('{% if post.url %}')
    contpage.write('<li><a href="{{ post.url }}">{{ post.title }}</a></li>')
    contpage.write('{% endif %}')
    contpage.write('{% endfor %}')
    contpage.write('</ul>')


with open('site/biocontainers/_posts/' + post_date + '-' + container + '_' + dfp.labels['software.version'] + '.md', 'w') as contpage:
    contpage.write('---\nlayout: post\ntitle: '+container+'_'+dfp.labels['software.version']+'\ncategories: container '+container+'\n---\n')
    contpage.write('# '+container+'\n')
    contpage.write(' blabla version '+dfp.labels['software.version']+'\n')
    contpage.write('## tags\n')
    if 'tags' in dfp.labels:
        tags = dfp.labels['tags'].split(',')
        for tag in tags:
            contpage.write('* '+tag.strip()+'\n')
