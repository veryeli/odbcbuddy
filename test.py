import requests

from consts import URL

def send_query(query):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(f'{URL}/query', json={'query': query}, headers=headers)
    # Check if the request was successful
    print(f"Response status code: {response.status_code}")
    if response.status_code == 200:
        try:
            data = response.json()
            if data['status'] == 'success':
                results = data['results']
                return results
            else:
                print(f"Error: {data['message']}")
        except requests.exceptions.JSONDecodeError as e:
            print(f"Failed to parse JSON response: {e}")
            print(f"Response content: {response.content}")
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        print(f"Response content: {response.content}")


def test_count_query():
    query = 'select count(1) from case_reporting_view'
    res = send_query(query)


def test_bigger_query():
    query = "select [client], attorney from case_reporting_view where status LIKE 'Open/Active'"
    res = send_query(query)

def test_decode():
    query = "select * from case_reporting_view where [case type code] like '7M93'"
    res = send_query(query)
    

if __name__ == '__main__':
    test_count_query()
    test_bigger_query()
    test_decode()
