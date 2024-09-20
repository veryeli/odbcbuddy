import requests

from consts import URL

def send_query(query):
    response = requests.get(f'{URL}/query', params={'query': query})
    # Print the response status code and JSON content
    print(f'Status Code: {response.status_code}')
    if response.headers['Content-Type'] == 'application/json':
      print('Response JSON:')
      print(response.json())
    else:
      print('Response Text:')
      print(response.text)

def test_count_query():
    query = 'select count(1) from case_reporting_view'
    send_query(query)


def test_bigger_query():
    query = "select [client], attorney from case_reporting_view where status LIKE 'Open/Active'"
    send_query(query)


if __name__ == '__main__':
    test_count_query()
    test_bigger_query()
