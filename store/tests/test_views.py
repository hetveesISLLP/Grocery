from django import urls
import pytest

# client is instance of django client - a web browser which handles get/post requests
# function shld start with test_

@pytest.mark.parametrize('param', [
    ('login')
])
def test_render_views(client, param):
    temp_url = urls.reverse(param)
    response = client.get(temp_url)
    assert response.status_code == 200
