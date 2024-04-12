import dns.query

import dns.query
import dns.message

request = dns.message.make_query('google.com', dns.rdatatype.ANY)

response = dns.query.tls(request, '8.8.8.8')

print(response)
