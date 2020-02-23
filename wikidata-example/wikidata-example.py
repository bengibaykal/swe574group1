from wikidata.client import Client

client = Client()
entity = client.get('Q42', load=True)
print(entity.description)
# English writer and humorist
