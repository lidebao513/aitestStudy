import requests
import requests
def test_httpbin_status_code():
    url = 'https://httpbin.org/get'
    response = requests.get(url)
    assert response.status_code == 200,f"状态码错误，实际为{response.status_code}"
    json_data = response.json()
    assert "args" in json_data,f"args字段不存在"
    #assert "non_exist_key" in json_data,f"non_exist_key字段不存在"
    print("所有断言通过")


if __name__ == '__main__':
    test_httpbin_status_code()